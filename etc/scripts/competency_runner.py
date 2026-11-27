"""Run the IOF competency questions and report them as GitHub Actions annotations.

    ./competency                                     # every suite
    ./competency provisional                         # one tier
    ./competency provisional/slots                   # one category of suites
    ./competency provisional/slots/fasteners         # one suite (a dataset and its question sets)
    ./competency provisional/slots/fasteners/bolt-types   # one question set
    ./competency provisional/slots/fasteners --no-cache   # force HermiT
    ./competency provisional/slots/fasteners --update-expected
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
from dataclasses import asdict, dataclass
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
class Tally:
    """How a suite's questions went: counts and suite names only, safe for the public log."""
    suite: str
    tier: str
    passed: int = 0
    failed: int = 0
    broken: int = 0
    not_run: int = 0
    clean: bool = True

    @property
    def questions(self) -> int:
        return self.passed + self.failed + self.broken + self.not_run

    def add(self, outcome: str) -> None:
        setattr(self, outcome, getattr(self, outcome) + 1)
        print('  ' + outcome.replace('_', ' '))


OUTCOMES = ('passed', 'failed', 'broken', 'not_run')


def summary_table(tallies: list) -> str:
    """A Markdown table of the tallies with a total row (for $GITHUB_STEP_SUMMARY)."""
    def total(key):
        return sum(t[key] if isinstance(t, dict) else getattr(t, key) for t in tallies)
    rows = ['| Suite | Tier | Questions | Passed | Failed | Broken | Not run | Result |',
            '|---|---|--:|--:|--:|--:|--:|---|']
    for t in sorted((t if isinstance(t, dict) else asdict(t) for t in tallies), key=lambda t: t['suite']):
        n = sum(t[k] for k in OUTCOMES)
        rows.append(f"| {t['suite']} | {t['tier']} | {n} | {t['passed']} | {t['failed']} | {t['broken']} | "
                    f"{t['not_run']} | {'✅ passed' if t['clean'] else '❌ failed'} |")
    n = sum(total(k) for k in OUTCOMES)
    rows.append(f'| **Total ({len(tallies)} suite{"" if len(tallies) == 1 else "s"})** | | **{n}** | **{total("passed")}** | **{total("failed")}** | '
                f'**{total("broken")}** | **{total("not_run")}** | {total("clean")} of {len(tallies)} passed |')
    return '\n'.join(rows) + '\n'


def tally_line(tallies: list) -> str:
    def total(key):
        return sum(t[key] if isinstance(t, dict) else getattr(t, key) for t in tallies)
    n = sum(total(k) for k in OUTCOMES)
    parts = [f'{total(k)} {k.replace("_", " ")}' for k in OUTCOMES if total(k)]
    suites = f'{len(tallies)} suite' + ('' if len(tallies) == 1 else 's')
    return f'{n} questions in {suites}: ' + ', '.join(parts or ['none run'])


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


def _check_inconsistent(suite: Suite, question: Question, entailed: EntailResult | None, out: Reporter) -> bool:
    """A '# expect: inconsistent' question: True (bad) unless HermiT found the data inconsistent."""
    if entailed is not None and entailed.failure == 'inconsistent':
        return False
    if entailed is None or entailed.failure is not None:
        return True             # HermiT timed out or failed: reported with the reasoner messages
    out.emit(Message(annotation_level(suite.tier, 'failure'), question.name,
                     'expected HermiT to find the data inconsistent, but it is consistent', None, question.path))
    return True


def _report_suite(suite: Suite, loaded: Loaded, args, out: Reporter) -> Tally:
    """Print the suite's results and count them."""
    tally = Tally(suite.name, suite.tier)
    print('::group::' + suite.name)
    errors_before = out.errors
    failed = loaded.files is None
    for m in loaded.messages:
        out.emit(m)
    entailed = loaded.entailed
    # an inconsistency every reasoning question expects is the result, not a reasoner failure
    expected_inconsistency = (entailed is not None and entailed.failure == 'inconsistent'
                              and suite.expects_inconsistent)
    if expected_inconsistency:
        out.emit(Message('::notice', 'Reasoner', f'{suite.name}: inconsistent, as its questions expect '
                         f'(HermiT took {entailed.seconds:.0f} s)', None))
    elif entailed is not None:
        for m in _reasoner_messages(suite, entailed):
            out.emit(m)
        failed |= entailed.failure is not None
    for qset in suite.sets:
        for question in qset.tests:
            how = '' if question.reasoning is None else ' (reasoning)' if question.reasoning else ' (no reasoning)'
            print(f'▶ {qset.name}/{question.name}{how}: {question.description or "(no description)"}')
            if question.error:
                out.emit(Message('::error', question.name, 'broken question', question.error, question.path))
                tally.add('broken')
                failed = True
                continue
            if question.expect_inconsistent:
                bad = _check_inconsistent(suite, question, entailed, out)
                failed |= bad
                tally.add('failed' if bad else 'passed')
                continue
            ds = (loaded.entailed.dataset if loaded.entailed else None) if question.reasoning else loaded.asserted
            if ds is None:
                tally.add('not_run')
                failed = True
                continue
            findings = _ask(question, ds, args)
            for m in _findings_messages(suite, question, findings, out.redact):
                out.emit(m)
            failed |= any(f.kind in ('failure', 'broken') for f in findings)
            tally.add('broken' if any(f.kind == 'broken' for f in findings)
                      else 'failed' if any(f.kind == 'failure' for f in findings) else 'passed')
    print('::endgroup::')
    tally.clean = not failed and out.errors == errors_before
    print(f'::notice title={suite.name}::{suite.name} {"passed" if tally.clean else "failed"}: '
          + tally_line([tally]).replace(' in 1 suite', ''))
    return tally


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Run the IOF competency questions')
    parser.add_argument('selectors', nargs='*', metavar='SUITE',
                        help="tier ('release'), category ('release/slots'), suite ('release/slots/fasteners') "
                             "or question set ('release/slots/fasteners/bolt-types'); default: all")
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
    parser.add_argument('--summary-json', type=Path, metavar='FILE',
                        help='also write the per-suite question counts as JSON (for a CI total)')
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
    tallies: list[Tally] = []
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        futures = {s.name: pool.submit(_load, s, prepared[s.name], args)
                   for s in suites if prepared[s.name].files is not None}
        for suite in suites:
            loaded = futures[suite.name].result() if suite.name in futures else prepared[suite.name]
            tallies.append(_report_suite(suite, loaded, args, out))
    write_summaries(tallies, args.summary_json)
    counts = tally_line(tallies)
    failed = [t.suite for t in tallies if not t.clean]

    if out.errors:
        print(f'::error title=Competency Tests::some competency questions failed. {counts}')
        return 1
    if failed:
        print(f'::warning title=Competency Tests::provisional suites failed (warnings only): {", ".join(failed)}. {counts}')
        return 0
    print(f'::notice title=Competency Tests::all competency questions passed. {counts}')
    return 0


def write_summaries(tallies: list[Tally], json_path: Path | None) -> None:
    """The counts as a Markdown job summary (under GitHub Actions) and, if asked, as JSON."""
    step_summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if step_summary:
        with open(step_summary, 'a', encoding='utf-8') as f:
            f.write('### Competency questions\n\n' + summary_table(tallies))
    if json_path:
        Path(json_path).write_text(json.dumps([asdict(t) for t in tallies], indent=1))

if __name__ == '__main__':
    sys.exit(main())
