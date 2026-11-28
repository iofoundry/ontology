#!/usr/bin/env python3
"""Check ontology IRIs and rdfs:isDefinedBy across the IOF modules (report only, for CI).

For every IOF module transitively imported by ``AboutIOFDev.rdf`` (imports resolved
through ``catalog-v001.xml``; cached third-party ontologies are skipped) this checks that:

  1. the ``owl:Ontology`` IRI matches the module's path, e.g.
     ``core/meta/AnnotationVocabulary.rdf`` → ``.../ontology/core/meta/AnnotationVocabulary/``;
  2. every IOF class, property and individual has an ``rdfs:isDefinedBy`` naming the
     module that defines it.

Which module defines an entity is decided by ``normalize_ontologies.plan_is_defined_by``,
so this reports exactly what ``normalize_ontologies.py`` would correct. Nothing is
written. Problems are printed as GitHub Actions annotations (and, under GitHub Actions,
listed on the job's summary page); the exit status is 1 if any error is found.

Usage (from the repository root):

    python etc/scripts/check_module_iris.py
    python etc/scripts/normalize_ontologies.py <version>    # to correct what it reports
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import job_summary
from normalize_ontologies import (defined_by_value, discover, load, module_iri, plan_is_defined_by,
                                  subject_iri)


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def main() -> int:
    with job_summary.recording() as findings:
        code, modules = check()
    rollup = 'Module IRIs'          # the closing count, not a problem of its own
    problems = [f for f in findings if f['title'] != rollup]
    job_summary.append(job_summary.section(f'Module IRIs: {modules} modules', problems))
    return code


def check() -> tuple[int, int]:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--about", nargs="+", default=["AboutIOFDev.rdf"],
                    help="root packaging files (default: AboutIOFDev.rdf)")
    ap.add_argument("--repo", default=".", help="ontology repository root (default: .)")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    files = discover([repo / a for a in args.about], repo)
    plan = plan_is_defined_by(files, repo)
    errors = 0

    for path in files:
        of = load(path)
        rel = path.relative_to(repo)
        expected = module_iri(path, repo)

        if of.iri != expected:
            errors += 1
            print(f"::error file={rel},line={line_of(of.text, of.onto.start)},title=Ontology IRI::"
                  f"Ontology IRI <{of.iri}> does not match the module path; expected <{expected}>")

        correct, add = plan.correct.get(path, set()), plan.add.get(path, set())
        reported: set[str] = set()
        for el in of.root.children:
            iri = subject_iri(el, of)
            if iri in reported or iri not in correct | add:
                continue
            current = next((c for c in el.children if c.name == "rdfs:isDefinedBy"), None)
            if iri in correct and current is not None:
                errors += 1
                reported.add(iri)
                print(f"::error file={rel},line={line_of(of.text, current.start)},title=rdfs:isDefinedBy::"
                      f"{el.name} <{iri}> has rdfs:isDefinedBy <{defined_by_value(current, of)}>; "
                      f"expected <{expected}>")
            elif iri in add and current is None:
                errors += 1
                reported.add(iri)
                print(f"::error file={rel},line={line_of(of.text, el.start)},title=rdfs:isDefinedBy::"
                      f"{el.name} <{iri}> has no rdfs:isDefinedBy; expected <{expected}>")

    for warning in plan.warnings:
        print(warning)

    summary = f"{len(files)} modules: {errors} error(s), {len(plan.warnings)} warning(s)"
    if errors:
        print(f"::error title=Module IRIs::{summary}. Run etc/scripts/normalize_ontologies.py to correct them.")
        return 1, len(files)
    print(f"::notice title=Module IRIs::{summary}")
    return 0, len(files)


if __name__ == "__main__":
    sys.exit(main())
