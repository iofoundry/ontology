"""Competency suites: discovery, offline import resolution, and the release tier check.

A suite is a directory etc/testing/competency/<tier>/<suite>/ where <tier> is release or
provisional. Its *.ttl / *.rdf files are the test ontologies; tests/*.shapes.ttl are SHACL
tests and tests/*.rq are SPARQL tests (each with a sibling .expected.csv).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ontology_closure import Closure, ClosureError, import_closure, load_catalog, ontology_iri

TIERS = ('release', 'provisional')
ONTOLOGY_SUFFIXES = ('.ttl', '.rdf')


class SuiteError(Exception):
    """A broken suite (not a test finding): always reported as an error."""


@dataclass
class Suite:
    name: str          # e.g. 'release/slots'
    tier: str
    root: Path
    ontology_files: list[Path]
    shapes_tests: list[Path]
    sparql_tests: list[Path]


def _suite(tier: str, root: Path) -> Suite:
    tests = root / 'tests'
    return Suite(
        name=f'{tier}/{root.name}', tier=tier, root=root,
        ontology_files=sorted(p for p in root.iterdir() if p.is_file() and p.suffix in ONTOLOGY_SUFFIXES),
        shapes_tests=sorted(tests.glob('*.shapes.ttl')) if tests.is_dir() else [],
        sparql_tests=sorted(tests.glob('*.rq')) if tests.is_dir() else [])


def discover_suites(base: Path, selectors: list[str]) -> list[Suite]:
    """All suites under base, or those named by selectors ('release' or 'release/slots')."""
    base = Path(base)
    suites = {}
    for tier in TIERS:
        if (base / tier).is_dir():
            for root in sorted(p for p in (base / tier).iterdir() if p.is_dir()):
                suite = _suite(tier, root)
                suites[suite.name] = suite
    if not selectors:
        return [suites[n] for n in sorted(suites)]
    chosen = {}
    for selector in selectors:
        selector = selector.strip('/')
        matches = [n for n in suites if n == selector or n.startswith(selector + '/')]
        if not matches:
            raise SuiteError(f'no competency suite or tier matches {selector!r} under {base}')
        chosen.update((n, suites[n]) for n in matches)
    return [chosen[n] for n in sorted(chosen)]


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
        raise SuiteError(f'{suite.name} has no *.ttl or *.rdf ontology files')
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
