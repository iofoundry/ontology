"""Run the IOF competency tests and report them as GitHub Actions annotations.

    ./competency                                # every suite
    ./competency release                        # one tier
    ./competency release/slots --no-cache       # one suite, force HermiT
    ./competency release/slots --update-expected
    ./competency --list                         # suite names as JSON (CI matrix)

Each suite in etc/testing/competency/<tier>/<suite>/ is loaded with only its own import
closure (resolved through catalog-v001.xml, never the web), entailed with HermiT (cached
in build/competency/ by input hash), then checked with its tests/*.shapes.ttl (SHACL) and
tests/*.rq + *.expected.csv (SPARQL). See etc/testing/competency/README.md.

Failures are errors in release/ suites and warnings in provisional/ suites; a broken
suite or test (unresolved import, unparseable file, missing expected results, a release
suite importing a provisional module) is an error in both. Exit status 1 iff any error.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from competency_checks import Finding, check_sparql, run_shacl
from competency_entail import EntailResult, entail
from competency_suite import Suite, SuiteError, discover_suites, resolve_suite, tier_violations

REPO_ROOT = Path(__file__).resolve().parents[2]


def annotation_level(tier: str, kind: str) -> str:
    if kind == 'broken':
        return '::error'
    if kind == 'failure':
        return '::error' if tier == 'release' else '::warning'
    if kind == 'warning':
        return '::warning'
    return '::notice'


class Reporter:
    def __init__(self):
        self.errors = 0

    def emit(self, level: str, title: str, message: str, file: Path | None = None) -> None:
        if level == '::error':
            self.errors += 1
        location = 'file=' + os.path.relpath(file, REPO_ROOT) + ',' if file else ''
        print(f'{level} {location}title={title}::{message}'.replace('\n', ' '))


def _prepare(suite: Suite, args, report: list) -> list[Path] | None:
    """Resolve imports and check the tier; returns the closure files, or None if broken."""
    try:
        closure = resolve_suite(suite, args.catalog)
    except SuiteError as e:
        report.append(('::error', 'Imports', str(e), suite.root))
        return None
    for iri in tier_violations(suite, closure, args.prod_about, args.catalog):
        report.append(('::error', 'Tier', f'release suite {suite.name} depends on provisional module {iri} '
                                          '— move the suite to provisional/', suite.root))
    return closure.files


def _entail(suite: Suite, files: list[Path], args) -> EntailResult:
    return entail(files, Path(args.build_dir) / suite.name, timeout=args.reasoner_timeout,
                  memory=args.reasoner_memory, use_cache=not args.no_cache)


def _report_suite(suite: Suite, prepared: list, result: EntailResult | None, args, out: Reporter) -> None:
    print('::group::' + suite.name)
    errors_before = out.errors
    for level, title, message, file in prepared:
        out.emit(level, title, message, file)
    findings: list[Finding] = []
    if result is not None:
        failure = annotation_level(suite.tier, 'failure')
        if result.failure:
            out.emit(failure, 'Reasoner', f'{suite.name}: HermiT {result.failure} '
                     f'after {result.seconds:.0f} s; tests not run', suite.root)
        else:
            how = 'loaded from cache' if result.cached else f'HermiT took {result.seconds:.0f} s'
            out.emit('::notice', 'Reasoner', f'{suite.name}: entailed ({how})')
            for iri in result.unsatisfiable:
                out.emit(failure, 'Reasoner', f'class {iri} is unsatisfiable (equivalent to owl:Nothing)', suite.root)
            for shapes in suite.shapes_tests:
                findings += run_shacl(shapes, result.dataset)
            for query in suite.sparql_tests:
                findings += check_sparql(query, result.dataset, update=args.update_expected)
    for f in findings:
        out.emit(annotation_level(suite.tier, f.kind), f.title, f.message, f.file)
    print('::endgroup::')
    clean = out.errors == errors_before and not any(f.kind == 'failure' for f in findings) \
        and result is not None and result.failure is None
    print(f'::notice title={suite.name}::{suite.name} {"passed" if clean else "failed"}')


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Run the IOF competency tests')
    parser.add_argument('selectors', nargs='*', metavar='SUITE',
                        help="tier ('release') or suite ('release/slots'); default: all")
    parser.add_argument('--list', action='store_true',
                        help='print the selected suite names as a JSON array (for a CI matrix) and exit')
    parser.add_argument('--no-cache', action='store_true', help='re-run HermiT even if inputs are unchanged')
    parser.add_argument('--update-expected', action='store_true',
                        help='(re)write each tests/*.expected.csv from the current results')
    parser.add_argument('--jobs', type=int, default=1, help='suites to entail in parallel (default 1)')
    parser.add_argument('--reasoner-timeout', type=float, default=3600, metavar='SECONDS',
                        help='HermiT time limit per suite (default 3600)')
    parser.add_argument('--reasoner-memory', default='4g', metavar='SIZE', help='Java heap (default 4g)')
    parser.add_argument('--base', default=REPO_ROOT / 'etc/testing/competency', type=Path)
    parser.add_argument('--catalog', default=REPO_ROOT / 'catalog-v001.xml', type=Path)
    parser.add_argument('--prod-about', default=REPO_ROOT / 'AboutIOFProd.rdf', type=Path)
    parser.add_argument('--build-dir', default=REPO_ROOT / 'build/competency', type=Path)
    args = parser.parse_args(argv)

    out = Reporter()
    try:
        suites = discover_suites(args.base, args.selectors)
    except SuiteError as e:
        out.emit('::error', 'Competency Tests', str(e))
        return 1
    if args.list:
        print(json.dumps([s.name for s in suites]))
        return 0
    if not suites:
        out.emit('::warning', 'Competency Tests', f'no competency suites under {args.base}')
        return 0

    prepared = {s.name: [] for s in suites}
    files = {s.name: _prepare(s, args, prepared[s.name]) for s in suites}
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = {s.name: pool.submit(_entail, s, files[s.name], args)
                   for s in suites if files[s.name] is not None}
        for suite in suites:
            result = futures[suite.name].result() if suite.name in futures else None
            _report_suite(suite, prepared[suite.name], result, args, out)

    if out.errors:
        print('::error title=Competency Tests::some competency tests failed.')
        return 1
    print('::notice title=Competency Tests::all competency tests passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
