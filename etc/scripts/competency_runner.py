"""Run the IOF competency questions and report them as GitHub Actions annotations.

    ./competency                                     # every suite
    ./competency provisional                         # one tier
    ./competency provisional/fasteners               # one suite (a dataset and its question sets)
    ./competency provisional/fasteners/bolt-types    # one question set
    ./competency provisional/fasteners --no-cache    # force HermiT
    ./competency provisional/fasteners --update-expected
    ./competency --list                              # suite names as JSON (CI matrix)
    ./competency --redact                            # public CI: hide data in the log

The questions live in the private iofoundry/ontology-questions repository, overlaid at
etc/testing/competency/ (see etc/scripts/COMPETENCY.md); without it there is nothing to
run and the runner exits 0. Each suite's data is loaded with only its own import closure
(resolved through catalog-v001.xml, never the web) once for all its question sets. Each
question's '# reasoning:' header says whether it is asked of the HermiT-entailed graph
(cached in build/competency/ by input hash) or of the asserted triples alone; HermiT
runs only if some question needs it.

Failures are errors in release/ suites and warnings in provisional/ suites; a broken
suite or question (unresolved import, unparseable file, missing header or expected
results, a release suite importing a provisional module) is an error in both. Exit
status 1 iff any error.

With --redact (the public ontology repository's CI), nothing taken from the data or the
questions' results is printed: only question names, descriptions and counts.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from rdflib import Dataset

from competency_checks import Finding, check_sparql, run_shacl
from competency_entail import EntailResult, asserted_dataset, entail
from competency_suite import Question, Suite, SuiteError, discover_suites, resolve_suite, tier_violations

REPO_ROOT = Path(__file__).resolve().parents[2]
QUESTIONS_REPO = 'iofoundry/ontology-questions'
HIDDEN = 'details hidden (--redact); run locally to see them'


def annotation_level(tier: str, kind: str) -> str:
    if kind == 'broken':
        return '::error'
    if kind == 'failure':
        return '::error' if tier == 'release' else '::warning'
    if kind == 'warning':
        return '::warning'
    return '::notice'


@dataclass
class Message:
    level: str
    title: str
    summary: str             # safe to print in a public log
    detail: str | None       # taken from the data or results: hidden with --redact
    file: Path | None = None


class Reporter:
    def __init__(self, redact: bool):
        self.errors = 0
        self.redact = redact

    def emit(self, m: Message) -> None:
        if m.level == '::error':
            self.errors += 1
        location = 'file=' + os.path.relpath(m.file, REPO_ROOT) + ',' if m.file else ''
        if m.detail is None:
            text = m.summary
        elif self.redact:
            text = f'{m.summary} — {HIDDEN}'
        else:
            text = f'{m.summary}: {m.detail}'
        print(f'{m.level} {location}title={m.title}::{text}'.replace('\n', ' '))


@dataclass
class Loaded:
    files: list[Path] | None             # the import closure; None if the suite is broken
    messages: list[Message]
    entailed: EntailResult | None = None
    asserted: Dataset | None = None


def _prepare(suite: Suite, args) -> Loaded:
    """Resolve imports and check the tier."""
    try:
        closure = resolve_suite(suite, args.catalog)
    except SuiteError as e:
        return Loaded(None, [Message('::error', 'Imports', f'{suite.name}: cannot resolve imports', str(e),
                                     suite.root)])
    except Exception as e:  # noqa: BLE001 — unparseable ontology, catalog entry to a missing file, ...
        return Loaded(None, [Message('::error', 'Imports', f'{suite.name}: cannot load the data',
                                     f'{type(e).__name__}: {e}', suite.root)])
    # IOF module IRIs are public: shown even with --redact
    messages = [Message('::error', 'Tier', f'release suite {suite.name} depends on provisional module {iri} '
                        '— move the suite to provisional/', None, suite.root)
                for iri in tier_violations(suite, closure, args.prod_about, args.catalog)]
    return Loaded(closure.files, messages)


def _load(suite: Suite, loaded: Loaded, args) -> Loaded:
    """The graphs the suite's questions need: entailed (HermiT, cached) and/or asserted."""
    if suite.needs_reasoning:
        try:
            loaded.entailed = entail(loaded.files, Path(args.build_dir) / suite.name,
                                     timeout=args.reasoner_timeout, memory=args.reasoner_memory,
                                     use_cache=not args.no_cache)
        except Exception as e:  # noqa: BLE001 — e.g. a corrupt cached entailed.nq; this suite only
            loaded.entailed = EntailResult(None, [], f'error: {type(e).__name__}: {e} (try --no-cache)', 0.0, False)
    if suite.needs_asserted:
        try:
            loaded.asserted = asserted_dataset(loaded.files)
        except Exception as e:  # noqa: BLE001
            loaded.messages.append(Message('::error', 'Imports', f'{suite.name}: cannot load the data',
                                           f'{type(e).__name__}: {e}', suite.root))
    return loaded


def _reasoner_messages(suite: Suite, result: EntailResult) -> list[Message]:
    failure = annotation_level(suite.tier, 'failure')
    if result.failure:
        kind, _, detail = result.failure.partition(': ')
        return [Message(failure, 'Reasoner', f'{suite.name}: HermiT {kind} after {result.seconds:.0f} s; '
                        'questions that need reasoning not run', detail or None, suite.root)]
    how = 'loaded from cache' if result.cached else f'HermiT took {result.seconds:.0f} s'
    messages = [Message('::notice', 'Reasoner', f'{suite.name}: entailed ({how})', None)]
    if result.unsatisfiable:
        messages.append(Message(failure, 'Reasoner', f'{len(result.unsatisfiable)} unsatisfiable classes '
                                '(equivalent to owl:Nothing)', ', '.join(result.unsatisfiable), suite.root))
    return messages


def _findings_messages(suite: Suite, question: Question, findings: list[Finding], redact: bool) -> list[Message]:
    if not redact:
        return [Message(annotation_level(suite.tier, f.kind), f.title, f.message, None, f.file) for f in findings]
    counts = Counter(f.kind for f in findings)
    return [Message(annotation_level(suite.tier, kind), question.name,
                    f'{n} {kind}{"s" if n > 1 else ""}', '', question.path)
            for kind, n in sorted(counts.items())]


def _ask(question: Question, ds: Dataset, args) -> list[Finding]:
    if question.kind == 'shacl':
        return run_shacl(question.path, ds)
    return check_sparql(question.path, ds, update=args.update_expected)


def _report_suite(suite: Suite, loaded: Loaded, args, out: Reporter) -> bool:
    """Print the suite's results; True if every question passed."""
    print('::group::' + suite.name)
    errors_before = out.errors
    failed = loaded.files is None
    for m in loaded.messages:
        out.emit(m)
    if loaded.entailed is not None:
        for m in _reasoner_messages(suite, loaded.entailed):
            out.emit(m)
        failed |= loaded.entailed.failure is not None
    for qset in suite.sets:
        for question in qset.tests:
            how = '' if question.reasoning is None else ' (reasoning)' if question.reasoning else ' (no reasoning)'
            print(f'▶ {qset.name}/{question.name}{how}: {question.description or "(no description)"}')
            if question.error:
                out.emit(Message('::error', question.name, 'broken question', question.error, question.path))
                print('  broken')
                failed = True
                continue
            ds = (loaded.entailed.dataset if loaded.entailed else None) if question.reasoning else loaded.asserted
            if ds is None:
                print('  not run')
                failed = True
                continue
            findings = _ask(question, ds, args)
            for m in _findings_messages(suite, question, findings, out.redact):
                out.emit(m)
            bad = any(f.kind in ('failure', 'broken') for f in findings)
            failed |= bad
            print('  failed' if bad else '  passed')
    print('::endgroup::')
    clean = not failed and out.errors == errors_before
    print(f'::notice title={suite.name}::{suite.name} {"passed" if clean else "failed"}')
    return clean


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Run the IOF competency questions')
    parser.add_argument('selectors', nargs='*', metavar='SUITE',
                        help="tier ('release'), suite ('release/fasteners') or question set "
                             "('release/fasteners/bolt-types'); default: all")
    parser.add_argument('--list', action='store_true',
                        help='print the selected suite names as a JSON array (for a CI matrix) and exit')
    parser.add_argument('--no-cache', action='store_true', help='re-run HermiT even if inputs are unchanged')
    parser.add_argument('--update-expected', action='store_true',
                        help='(re)write each *.expected.csv from the current results')
    parser.add_argument('--redact', action='store_true',
                        help='print nothing taken from the data or results (for public CI logs)')
    parser.add_argument('--jobs', type=int, default=1, help='suites to load in parallel (default 1)')
    parser.add_argument('--reasoner-timeout', type=float, default=3600, metavar='SECONDS',
                        help='HermiT time limit per suite (default 3600)')
    parser.add_argument('--reasoner-memory', default='4g', metavar='SIZE', help='Java heap (default 4g)')
    parser.add_argument('--base', default=REPO_ROOT / 'etc/testing/competency', type=Path,
                        help=f'the {QUESTIONS_REPO} checkout (default etc/testing/competency)')
    parser.add_argument('--catalog', default=REPO_ROOT / 'catalog-v001.xml', type=Path)
    parser.add_argument('--prod-about', default=REPO_ROOT / 'AboutIOFProd.rdf', type=Path)
    parser.add_argument('--build-dir', default=REPO_ROOT / 'build/competency', type=Path)
    args = parser.parse_args(argv)

    out = Reporter(args.redact)
    if not Path(args.base).is_dir():
        if args.list:
            print('[]')
        else:
            print(f'::notice title=Competency Tests::no competency questions: {QUESTIONS_REPO} is not '
                  f'checked out at {os.path.relpath(args.base, REPO_ROOT)}; nothing to run.')
        return 0
    try:
        suites = discover_suites(args.base, args.selectors)
    except SuiteError as e:
        out.emit(Message('::error', 'Competency Tests', 'cannot read the competency suites', str(e)))
        return 1
    if args.list:
        print(json.dumps([s.name for s in suites]))
        return 0
    if not suites:
        out.emit(Message('::warning', 'Competency Tests', f'no competency suites under {args.base}', None))
        return 0

    prepared = {s.name: _prepare(s, args) for s in suites}
    failed: list[str] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = {s.name: pool.submit(_load, s, prepared[s.name], args)
                   for s in suites if prepared[s.name].files is not None}
        for suite in suites:
            loaded = futures[suite.name].result() if suite.name in futures else prepared[suite.name]
            if not _report_suite(suite, loaded, args, out):
                failed.append(suite.name)

    if out.errors:
        print('::error title=Competency Tests::some competency questions failed.')
        return 1
    if failed:
        print('::warning title=Competency Tests::provisional suites failed (warnings only): ' + ', '.join(failed))
        return 0
    print('::notice title=Competency Tests::all competency questions passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
