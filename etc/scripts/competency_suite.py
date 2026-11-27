"""Competency suites: discovery, question metadata, offline import resolution, the tier check.

The questions live in the private iofoundry/ontology-questions repository, overlaid at
etc/testing/competency/ (a CI checkout, or a symlink locally). A suite is one dataset and
the question sets about it:

    <tier>/[<category>/...]      optional categories grouping suites (no data files)
    <tier>/.../<dataset>/        *.ttl / *.rdf: the data and its local ontology extensions,
                                 optional catalog-v001.xml overlay
    <tier>/.../<dataset>/<set>/  *.rq (+ *.expected.csv) and *.shapes.ttl: the questions

<tier> is release or provisional. Every question file starts with a comment header:

    # description: What the question checks (printed as the test runs).
    # reasoning: true            (false: the question sees only the asserted triples)
    # expect: inconsistent       (optional, with reasoning: true: passes iff HermiT finds the
                                 suite's data inconsistent; the body documents the conflict
                                 and is not run)

The suite's data is loaded once for all its sets; HermiT runs only if a question needs it.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from ontology_closure import Closure, ClosureError, import_closure, load_catalog, ontology_iri

TIERS = ('release', 'provisional')
ONTOLOGY_SUFFIXES = ('.ttl', '.rdf')
SHAPES_SUFFIX = '.shapes.ttl'
METADATA_KEYS = ('description', 'reasoning')
EXPECTATIONS = ('consistent', 'inconsistent')
BOOLEANS = {'true': True, 'yes': True, 'false': False, 'no': False}
HEADER_KEY = re.compile(r'^#\s*([A-Za-z]+)\s*:\s*(.*?)\s*$')
DECLARATION = re.compile(r'^\s*(@?prefix|@?base)\b', re.I)


class SuiteError(Exception):
    """A broken suite (not a test finding): always reported as an error."""


class QuestionError(Exception):
    """A broken question file (e.g. missing metadata): an error; the other questions still run."""


@dataclass
class Question:
    path: Path
    kind: str                       # 'sparql' | 'shacl'
    description: str | None
    reasoning: bool | None
    error: str | None = None        # set when the metadata header is missing or invalid
    expect_inconsistent: bool = False

    @property
    def name(self) -> str:
        return self.path.name.removesuffix(SHAPES_SUFFIX).removesuffix('.rq')


@dataclass
class QuestionSet:
    name: str
    root: Path
    tests: list[Question]


@dataclass
class Suite:
    name: str          # e.g. 'provisional/fasteners'
    tier: str
    root: Path
    ontology_files: list[Path]
    sets: list[QuestionSet] = field(default_factory=list)

    @property
    def tests(self) -> list[Question]:
        return [t for s in self.sets for t in s.tests]

    @property
    def needs_reasoning(self) -> bool:
        return any(t.reasoning for t in self.tests)

    @property
    def expects_inconsistent(self) -> bool:
        """Every reasoning question expects HermiT to find the data inconsistent."""
        reasoning = [t for t in self.tests if t.reasoning]
        return bool(reasoning) and all(t.expect_inconsistent for t in reasoning)

    @property
    def needs_asserted(self) -> bool:
        return any(t.reasoning is False for t in self.tests)


def _header(path: Path) -> dict[str, str]:
    """The header keys from the comments before the first statement; prefix and base
    declarations and blank lines may come before or among them."""
    found = {}
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        stripped = line.strip()
        if not stripped or DECLARATION.match(stripped):
            continue
        if not stripped.startswith('#'):
            break
        match = HEADER_KEY.match(stripped)
        if match and match.group(1).lower() in METADATA_KEYS + ('expect',):
            found.setdefault(match.group(1).lower(), match.group(2))
    return found


def read_metadata(path: Path) -> tuple[str, bool]:
    """(description, reasoning) from the question's leading comment header."""
    found = _header(path)
    missing = [k for k in METADATA_KEYS if not found.get(k)]
    if missing:
        raise QuestionError(f'{Path(path).name}: header comment is missing '
                            + ', '.join(f'"# {k}: …"' for k in missing))
    value = found['reasoning'].lower()
    if value not in BOOLEANS:
        raise QuestionError(f'{Path(path).name}: "# reasoning: {found["reasoning"]}" must be true or false')
    return found['description'], BOOLEANS[value]


def read_expect_inconsistent(path: Path, reasoning: bool) -> bool:
    """True for '# expect: inconsistent' (only meaningful with reasoning: true)."""
    value = _header(path).get('expect', 'consistent').lower()
    if value not in EXPECTATIONS:
        raise QuestionError(f'{Path(path).name}: "# expect: {value}" must be consistent or inconsistent')
    if value == 'inconsistent' and not reasoning:
        raise QuestionError(f'{Path(path).name}: "# expect: inconsistent" needs "# reasoning: true"')
    return value == 'inconsistent'


def _question(path: Path, kind: str) -> Question:
    try:
        description, reasoning = read_metadata(path)
        return Question(path, kind, description, reasoning,
                        expect_inconsistent=read_expect_inconsistent(path, reasoning))
    except (QuestionError, OSError, UnicodeDecodeError) as e:
        return Question(path, kind, None, None, str(e))


def _is_question(path: Path) -> bool:
    return path.suffix == '.rq' or path.name.endswith(SHAPES_SUFFIX)


def _question_set(root: Path) -> QuestionSet:
    files = sorted(p for p in root.iterdir() if p.is_file())
    return QuestionSet(root.name, root, [_question(p, 'sparql' if p.suffix == '.rq' else 'shacl')
                                         for p in files if _is_question(p)])


def _visible_dirs(path: Path) -> list[Path]:
    return sorted(p for p in path.iterdir() if p.is_dir() and not p.name.startswith('.'))


def _is_suite_dir(path: Path) -> bool:
    """A directory holding data (*.ttl / *.rdf) is a suite; any other is a category of suites."""
    return any(p.is_file() and p.suffix in ONTOLOGY_SUFFIXES for p in path.iterdir())


def _suite_roots(base: Path) -> dict[str, tuple[str, Path]]:
    """Every suite under base by name ('provisional/slots/fasteners'), however deep its categories."""
    roots: dict[str, tuple[str, Path]] = {}

    def walk(tier: str, path: Path, name: str) -> None:
        for d in _visible_dirs(path):
            if _is_suite_dir(d):
                roots[f'{name}/{d.name}'] = (tier, d)
                continue
            stray = [p.name for p in d.iterdir() if p.is_file() and _is_question(p)]
            if stray:
                raise SuiteError(f'{name}/{d.name} has no data files, so it is a category of suites; '
                                 f'questions must be in a question set of a suite: {", ".join(sorted(stray))}')
            walk(tier, d, f'{name}/{d.name}')

    for tier in TIERS:
        if (base / tier).is_dir():
            walk(tier, base / tier, tier)
    return roots


def _suite(tier: str, root: Path, name: str) -> Suite:
    files = sorted(p for p in root.iterdir() if p.is_file())
    stray = [p.name for p in files if _is_question(p)]
    if stray:
        raise SuiteError(f'{name}: questions must be in a question-set directory, '
                         f'not next to the data: {", ".join(stray)}')
    return Suite(name=name, tier=tier, root=root,
                 ontology_files=[p for p in files if p.suffix in ONTOLOGY_SUFFIXES],
                 sets=[_question_set(p) for p in _visible_dirs(root)])


def discover_suites(base: Path, selectors: list[str]) -> list[Suite]:
    """Suites under base, or those named by selectors: a tier ('release'), a category
    ('release/slots'), a suite ('release/slots/fasteners') or one question set
    ('release/slots/fasteners/bolt-types'). A suite is a directory with data files;
    directories between the tier and a suite are categories. A missing base (the
    questions are not checked out) has no suites."""
    base = Path(base)
    roots = _suite_roots(base)
    if not selectors:
        return [_suite(*roots[n], n) for n in sorted(roots)]
    chosen: dict[str, set[str] | None] = {}    # suite name -> question-set names (None = all)
    for selector in selectors:
        selector = selector.strip('/')
        matches = [n for n in roots if n == selector or n.startswith(selector + '/')]
        if matches:
            chosen.update((n, None) for n in matches)
            continue
        name, _, qset = selector.rpartition('/')
        if name in roots:
            if not (roots[name][1] / qset).is_dir():
                raise SuiteError(f'no competency question set {selector!r} under {base}')
            if chosen.get(name, set()) is not None:
                chosen.setdefault(name, set()).add(qset)
            continue
        raise SuiteError(f'no competency suite, category or tier matches {selector!r} under {base}')
    suites = []
    for name in sorted(chosen):
        suite = _suite(*roots[name], name)
        if chosen[name] is not None:
            suite.sets = [s for s in suite.sets if s.name in chosen[name]]
        suites.append(suite)
    return suites


def _resolution(suite: Suite, root_catalog: Path) -> dict[str, Path]:
    resolution = load_catalog(root_catalog)
    overlay = suite.root / 'catalog-v001.xml'
    if overlay.exists():
        resolution.update(load_catalog(overlay))
    return resolution


def suite_iris(suite: Suite) -> dict[str, Path]:
    try:
        return {ontology_iri(f): f.resolve() for f in suite.ontology_files}
    except ClosureError as e:
        raise SuiteError(str(e)) from e


def resolve_suite(suite: Suite, root_catalog: Path) -> Closure:
    """The suite's import closure, resolved only through the catalogs and its own files."""
    if not suite.ontology_files:
        raise SuiteError(f'{suite.name} has no *.ttl or *.rdf data files')
    own = suite_iris(suite)
    resolution = _resolution(suite, root_catalog)
    resolution.update(own)
    closure = import_closure(list(own), resolution)
    if closure.missing:
        raise SuiteError('imports not in the catalog (never fetched from the web): ' + '; '.join(
            f'{iri} (imported by {importer.name if importer else "?"})' for iri, importer in closure.missing))
    return closure


def tier_violations(suite: Suite, closure: Closure, prod_about: Path, root_catalog: Path) -> list[str]:
    """IRIs a release suite imports that are not part of the production (About) closure."""
    if suite.tier != 'release':
        return []
    resolution = load_catalog(root_catalog)
    prod_iri = ontology_iri(prod_about)
    resolution[prod_iri] = Path(prod_about).resolve()
    prod = import_closure([prod_iri], resolution)
    own = set(suite_iris(suite))
    prod_files = set(prod.files)
    return sorted(iri for iri in closure.iris
                  if iri not in own and iri not in prod.iris
                  and resolution.get(iri) not in prod_files)
