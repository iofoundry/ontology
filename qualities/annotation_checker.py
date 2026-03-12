#!/usr/bin/env python3
"""
IOF Annotation Compliance Checker

Checks ontology terms in the qualities/ directory against IOF annotation
principles (annotation_principles.md). Generates a Markdown report listing
all violations grouped by file and term.

Usage:
    python annotation_checker.py [--directory PATH] [--output FILE] [--no-should]

Rules enforced:
  [MUST]   Absolute requirement (violation = non-compliant term)
  [MUST NOT] Absolute prohibition
  [SHOULD] Recommended; violations are flagged but lower priority
"""

import os
import re
import argparse
from collections import defaultdict
from rdflib import Graph, RDF, RDFS, OWL, URIRef, Literal, Namespace, BNode

# ---------------------------------------------------------------------------
# Namespace bindings
# ---------------------------------------------------------------------------
IOF_AV   = Namespace("https://spec.industrialontologies.org/ontology/annotation/")
SKOS     = Namespace("http://www.w3.org/2004/02/skos/core#")
DCTERMS  = Namespace("http://purl.org/dc/terms/")

ONTOLOGY_EXTENSIONS = ("*.owl", "*.ttl", "*.rdf")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def gather_files(directory):
    import glob as _glob
    files = []
    for pattern in ONTOLOGY_EXTENSIONS:
        files.extend(_glob.glob(os.path.join(directory, pattern)))
    return sorted(files)


def local_name(iri: str) -> str:
    if "#" in iri:
        return iri.rsplit("#", 1)[1]
    return iri.rsplit("/", 1)[-1]


def en_literals(g, subject, predicate):
    """Return string values for predicate on subject where lang starts with 'en'."""
    result = []
    for obj in g.objects(subject, predicate):
        if isinstance(obj, Literal) and obj.language and obj.language.lower().startswith("en"):
            result.append(str(obj))
    return result


def de_literals(g, subject, predicate):
    """Return string values for predicate on subject where lang starts with 'de'."""
    result = []
    for obj in g.objects(subject, predicate):
        if isinstance(obj, Literal) and obj.language and obj.language.lower().startswith("de"):
            result.append(str(obj))
    return result


def all_literals(g, subject, predicate):
    return [str(o) for o in g.objects(subject, predicate) if isinstance(o, Literal)]


def all_values(g, subject, predicate):
    return list(g.objects(subject, predicate))


def is_primitive(g, subject):
    """Return True/False/None (not set)."""
    for val in g.objects(subject, IOF_AV.isPrimitive):
        if isinstance(val, Literal):
            return str(val).strip().lower() == "true"
    return None


# ---------------------------------------------------------------------------
# Label format checks
# ---------------------------------------------------------------------------

# Words that are legitimately capitalised per the spec (proper names, acronyms in dictionaries)
_KNOWN_CAPS = {"DNA", "RNA", "RADAR", "LIDAR", "UV", "IR", "NMR", "XRD", "XRF",
               "CT", "MRI", "SEM", "TEM", "AFM", "STM", "ISO", "ASTM", "DIN",
               "IOF", "BFO", "OWL", "RDF", "IRI", "URI", "ID"}

_ARTICLE_RE = re.compile(r"^(the|a|an)\s", re.IGNORECASE)


def check_label_case(label: str):
    """
    Flag words that look like UpperCamelCase or wrongly capitalised.
    Returns a list of issue strings.
    """
    issues = []
    words = label.split()
    for word in words:
        clean = re.sub(r"[^A-Za-z]", "", word)
        if not clean:
            continue
        if clean.upper() in _KNOWN_CAPS:
            continue
        # Flag UpperCamelCase (starts uppercase, has subsequent lowercase) within a word
        if re.match(r"[A-Z][a-z]+[A-Z]", clean):
            issues.append(f"word '{word}' looks like UpperCamelCase")
        # Flag a single fully-capitalised word (not in known-caps) longer than 2 chars
        elif clean.isupper() and len(clean) > 2 and clean not in _KNOWN_CAPS:
            issues.append(f"word '{word}' is all-caps (acronym not in allowed list)")
        # Flag first letter uppercase when it's not the first word
        elif words.index(word) > 0 and clean[0].isupper():
            issues.append(f"word '{word}' is capitalised mid-label (use lowercase)")
    return issues


def check_nld_start(nld: str):
    """Return issue string if NLD starts with a forbidden article."""
    stripped = nld.strip()
    m = _ARTICLE_RE.match(stripped)
    if m:
        return f"starts with article '{m.group(1)}'"
    return None


# ---------------------------------------------------------------------------
# Per-construct checks
# ---------------------------------------------------------------------------

def check_construct(g, term, construct_type, include_should=True):
    """
    Run all applicable annotation rules for a single construct.
    construct_type: 'class' | 'object_property' | 'data_property' | 'annotation_property'
    Returns list of (severity, message) tuples.
    """
    issues = []

    def must(msg):   issues.append(("MUST", msg))
    def mustnot(msg): issues.append(("MUST NOT", msg))
    def should(msg):
        if include_should:
            issues.append(("SHOULD", msg))

    # --- rdfs:label ---
    en_labels = en_literals(g, term, RDFS.label)
    de_labels = de_literals(g, term, RDFS.label)
    all_labels = all_values(g, term, RDFS.label)

    if not all_labels:
        must("Missing rdfs:label entirely")
    else:
        if not en_labels:
            must("Missing English rdfs:label (lang='en' or 'en-US')")
        elif len(en_labels) > 1:
            must(f"Multiple English rdfs:label ({len(en_labels)} found); exactly one required")
        else:
            for lbl in check_label_case(en_labels[0]):
                must(f"Label case: {lbl}")

        if include_should and not de_labels:
            should("Missing German rdfs:label (lang='de')")

    # --- rdfs:comment MUST NOT be used ---
    if all_values(g, term, RDFS.comment):
        mustnot("rdfs:comment used; replace with iof-av:explanatoryNote, "
                "iof-av:usageNote, or skos:scopeNote")

    # --- naturalLanguageDefinition ---
    en_nld = en_literals(g, term, IOF_AV.naturalLanguageDefinition)
    de_nld = de_literals(g, term, IOF_AV.naturalLanguageDefinition)
    all_nld = all_values(g, term, IOF_AV.naturalLanguageDefinition)

    if not all_nld:
        must("Missing iof-av:naturalLanguageDefinition")
    else:
        if not en_nld:
            must("Missing English iof-av:naturalLanguageDefinition")
        elif len(en_nld) > 1:
            must(f"Multiple English naturalLanguageDefinition ({len(en_nld)}); exactly one allowed")
        else:
            issue = check_nld_start(en_nld[0])
            if issue:
                must(f"naturalLanguageDefinition {issue}")

        if include_should and not de_nld:
            should("Missing German iof-av:naturalLanguageDefinition")

    # --- class-specific ---
    if construct_type == "class":
        prim = is_primitive(g, term)
        if prim is True:
            if not all_values(g, term, IOF_AV.primitiveRationale):
                must("isPrimitive=true but iof-av:primitiveRationale is missing")
        else:
            # non-primitive (false or not set): need FOL + SFNL definitions
            if not all_values(g, term, IOF_AV.firstOrderLogicDefinition):
                must("Non-primitive class missing iof-av:firstOrderLogicDefinition "
                     "(set iof-av:isPrimitive=true if necessary and sufficient "
                     "conditions cannot be provided)")
            if not all_values(g, term, IOF_AV.semiFormalNaturalLanguageDefinition):
                must("Non-primitive class missing iof-av:semiFormalNaturalLanguageDefinition")

    # --- property-specific ---
    if construct_type in ("object_property", "data_property"):
        should("Property missing skos:example" if not all_values(g, term, SKOS.example)
               else None)
        # Clean up None from conditional
        if issues and issues[-1] == ("SHOULD", None):
            issues.pop()
        if not all_values(g, term, SKOS.example):
            should("Missing skos:example")

    if construct_type == "data_property":
        for lbl in en_labels:
            if not (lbl.lower().startswith("is ") or lbl.lower().startswith("has ")):
                must(f"Data property label '{lbl}' must start with 'is' (boolean) "
                     "or 'has' (other)")

    return issues


# ---------------------------------------------------------------------------
# Ontology-level checks
# ---------------------------------------------------------------------------

def check_ontology(g):
    """Check annotations on the owl:Ontology node itself."""
    issues = []

    def must(msg): issues.append(("MUST", msg))

    ont_nodes = list(g.subjects(RDF.type, OWL.Ontology))
    if not ont_nodes:
        must("No owl:Ontology declaration found")
        return issues

    ont = ont_nodes[0]

    checks = [
        (RDFS.label,        "rdfs:label"),
        (DCTERMS.abstract,  "dcterms:abstract"),
        (DCTERMS.title,     "dcterms:title"),
        (IOF_AV.maturity,   "iof-av:maturity"),
        (IOF_AV.copyright,  "iof-av:copyright"),
        (DCTERMS.license,   "dcterms:license"),
        (OWL.versionInfo,   "owl:versionInfo"),
    ]
    for pred, name in checks:
        if not all_values(g, ont, pred):
            must(f"Ontology missing {name}")

    return issues


# ---------------------------------------------------------------------------
# Main analysis per file
# ---------------------------------------------------------------------------

def analyse_file(file_path, include_should=True):
    """
    Parse one ontology file and return:
      {
        'ontology_iri': str or None,
        'ontology_issues': [(severity, msg), ...],
        'construct_issues': {iri_str: {'type': str, 'label': str, 'issues': [...]}},
        'stats': {'classes': int, 'obj_props': int, 'data_props': int, 'ann_props': int,
                  'terms_checked': int, 'terms_with_issues': int}
      }
    """
    g = Graph()
    try:
        g.parse(file_path)
    except Exception as exc:
        return {"error": str(exc)}

    # Determine ontology IRI / namespace
    ont_nodes = list(g.subjects(RDF.type, OWL.Ontology))
    ont_ns = str(ont_nodes[0]) if ont_nodes else ""

    # Collect typed constructs (URIRef only, no blank nodes)
    classes     = {s for s in g.subjects(RDF.type, OWL.Class)            if isinstance(s, URIRef)}
    obj_props   = {s for s in g.subjects(RDF.type, OWL.ObjectProperty)   if isinstance(s, URIRef)}
    data_props  = {s for s in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(s, URIRef)}
    ann_props   = {s for s in g.subjects(RDF.type, OWL.AnnotationProperty) if isinstance(s, URIRef)}

    # For annotation properties: only check those in the ontology's own namespace
    # (others are just re-declarations of imported AP for tooling purposes)
    own_ann_props = {s for s in ann_props if ont_ns and str(s).startswith(ont_ns)}

    constructs_to_check = (
        [(s, "class")               for s in sorted(classes,    key=str)] +
        [(s, "object_property")     for s in sorted(obj_props,  key=str)] +
        [(s, "data_property")       for s in sorted(data_props, key=str)] +
        [(s, "annotation_property") for s in sorted(own_ann_props, key=str)]
    )

    ont_issues = check_ontology(g)

    construct_issues = {}
    for term, ctype in constructs_to_check:
        issues = check_construct(g, term, ctype, include_should=include_should)
        if issues:
            en_lbl = en_literals(g, term, RDFS.label)
            label_str = en_lbl[0] if en_lbl else local_name(str(term))
            construct_issues[str(term)] = {
                "type":   ctype,
                "label":  label_str,
                "issues": issues,
            }

    stats = {
        "classes":           len(classes),
        "obj_props":         len(obj_props),
        "data_props":        len(data_props),
        "ann_props":         len(own_ann_props),
        "terms_checked":     len(constructs_to_check),
        "terms_with_issues": len(construct_issues),
    }

    return {
        "ontology_iri":    ont_ns,
        "ontology_issues": ont_issues,
        "construct_issues": construct_issues,
        "stats":           stats,
    }


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

_SEVERITY_ORDER = {"MUST": 0, "MUST NOT": 1, "SHOULD": 2}
_SEVERITY_ICON  = {"MUST": "🔴", "MUST NOT": "🚫", "SHOULD": "🟡"}


def severity_label(sev):
    return f"**[{sev}]**"


def _violation_breakdown(file_results):
    """
    Count how many times each violation message pattern appears across all files.
    Returns a list of (count, message_fragment) sorted descending by count.
    """
    from collections import Counter
    counts = Counter()
    for r in file_results.values():
        if "construct_issues" not in r:
            continue
        for d in r["construct_issues"].values():
            for sev, msg in d["issues"]:
                # Normalise to a short key
                key = f"[{sev}] {msg}"
                counts[key] += 1
    return counts.most_common()


def generate_report(file_results, include_should=True):
    lines = []
    lines.append("# IOF Annotation Compliance Report\n")

    # Summary table
    total_terms       = sum(r["stats"]["terms_checked"]     for r in file_results.values() if "stats" in r)
    total_with_issues = sum(r["stats"]["terms_with_issues"] for r in file_results.values() if "stats" in r)
    total_ont_issues  = sum(len(r.get("ontology_issues", [])) for r in file_results.values())

    lines.append("## Summary\n")
    lines.append(f"| File | Terms checked | Terms with issues | Ontology-level issues |")
    lines.append(f"|------|:---:|:---:|:---:|")
    for fname, r in file_results.items():
        if "error" in r:
            lines.append(f"| {os.path.basename(fname)} | — | ERROR | — |")
        else:
            s = r["stats"]
            anchor = os.path.basename(fname).replace(".", "").lower()
            lines.append(
                f"| [{os.path.basename(fname)}](#{anchor}) "
                f"| {s['terms_checked']} | {s['terms_with_issues']} "
                f"| {len(r.get('ontology_issues', []))} |"
            )
    lines.append(f"\n**Total terms checked:** {total_terms}  ")
    lines.append(f"**Total terms with issues:** {total_with_issues}  ")
    lines.append(f"**Total ontology-level issues:** {total_ont_issues}\n")

    # Violation breakdown
    breakdown = _violation_breakdown(file_results)
    if breakdown:
        lines.append("## Violation Breakdown (all files)\n")
        lines.append("Ranked by frequency — use this to prioritise your work.\n")
        lines.append("| # | Violation | Occurrences |")
        lines.append("|---|-----------|:-----------:|")
        for i, (msg, cnt) in enumerate(breakdown, 1):
            lines.append(f"| {i} | {msg} | {cnt} |")
        lines.append("")

    lines.append("---\n")

    # Per-file details
    for fname, r in sorted(file_results.items()):
        basename = os.path.basename(fname)
        lines.append(f"## {basename}\n")

        if "error" in r:
            lines.append(f"> **Parse error:** {r['error']}\n")
            continue

        lines.append(f"**Ontology IRI:** `{r['ontology_iri']}`  ")
        s = r["stats"]
        lines.append(
            f"**Constructs:** {s['classes']} classes, {s['obj_props']} object properties, "
            f"{s['data_props']} data properties, {s['ann_props']} annotation properties (own namespace)  "
        )
        lines.append(f"**Terms checked:** {s['terms_checked']} | "
                     f"**Terms with issues:** {s['terms_with_issues']}\n")

        # Ontology-level issues
        if r["ontology_issues"]:
            lines.append("### Ontology-level annotations\n")
            for sev, msg in sorted(r["ontology_issues"], key=lambda x: _SEVERITY_ORDER.get(x[0], 9)):
                lines.append(f"- {severity_label(sev)} {msg}")
            lines.append("")

        # Construct issues
        if r["construct_issues"]:
            lines.append("### Construct violations\n")

            # Group by severity to give a quick sense of priority
            must_count   = sum(1 for d in r["construct_issues"].values()
                               for sev, _ in d["issues"] if sev in ("MUST", "MUST NOT"))
            should_count = sum(1 for d in r["construct_issues"].values()
                               for sev, _ in d["issues"] if sev == "SHOULD")
            lines.append(f"MUST/MUST-NOT violations: **{must_count}** | "
                         f"SHOULD violations: **{should_count}**\n")

            for iri, d in sorted(r["construct_issues"].items()):
                lname = local_name(iri)
                ctype_display = d["type"].replace("_", " ")
                lines.append(f"#### `{d['label']}` ({ctype_display})")
                lines.append(f"IRI: `{iri}`\n")
                sorted_issues = sorted(d["issues"], key=lambda x: _SEVERITY_ORDER.get(x[0], 9))
                for sev, msg in sorted_issues:
                    lines.append(f"- {severity_label(sev)} {msg}")
                lines.append("")
        else:
            lines.append("_No construct violations found._\n")

        lines.append("---\n")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Check IOF ontology terms against annotation principles."
    )
    parser.add_argument(
        "--directory", "-d", default=".",
        help="Directory containing ontology files (default: current directory)"
    )
    parser.add_argument(
        "--output", "-o", default="annotation_report.md",
        help="Output Markdown report file (default: annotation_report.md)"
    )
    parser.add_argument(
        "--no-should", action="store_true",
        help="Suppress SHOULD-level warnings; report only MUST violations"
    )
    args = parser.parse_args()

    files = gather_files(args.directory)
    if not files:
        print(f"No ontology files found in '{args.directory}'.")
        return 1

    include_should = not args.no_should

    file_results = {}
    for f in files:
        print(f"  Checking {os.path.basename(f)} ...", end=" ", flush=True)
        result = analyse_file(f, include_should=include_should)
        file_results[f] = result
        if "error" in result:
            print("ERROR:", result["error"])
        else:
            s = result["stats"]
            must_count = sum(
                1 for d in result["construct_issues"].values()
                for sev, _ in d["issues"] if sev in ("MUST", "MUST NOT")
            )
            should_count = sum(
                1 for d in result["construct_issues"].values()
                for sev, _ in d["issues"] if sev == "SHOULD"
            )
            parts = [f"{s['terms_checked']} terms"]
            if must_count:
                parts.append(f"{must_count} MUST violation(s)")
            if should_count and include_should:
                parts.append(f"{should_count} SHOULD warning(s)")
            if not must_count and not (should_count and include_should):
                parts.append("OK")
            print(", ".join(parts))

    report = generate_report(file_results, include_should=include_should)

    with open(args.output, "w", encoding="utf-8") as fh:
        fh.write(report)

    # Console summary
    total_terms = sum(r["stats"]["terms_checked"] for r in file_results.values() if "stats" in r)
    total_must = sum(
        1 for r in file_results.values() if "construct_issues" in r
        for d in r["construct_issues"].values()
        for sev, _ in d["issues"] if sev in ("MUST", "MUST NOT")
    )
    total_should = sum(
        1 for r in file_results.values() if "construct_issues" in r
        for d in r["construct_issues"].values()
        for sev, _ in d["issues"] if sev == "SHOULD"
    )
    total_ont_issues = sum(len(r.get("ontology_issues", [])) for r in file_results.values())

    print()
    print("=" * 60)
    print(f"  Terms checked  : {total_terms}")
    print(f"  MUST violations: {total_must}")
    if include_should:
        print(f"  SHOULD warnings: {total_should}")
    if total_ont_issues:
        print(f"  Ontology-level : {total_ont_issues}")
    print("=" * 60)
    if total_must:
        print("  RESULT: FAIL  (MUST violations present)")
    else:
        print("  RESULT: PASS  (no MUST violations)")
    print("=" * 60)
    print(f"\nFull report: {args.output}")

    return 1 if total_must else 0


if __name__ == "__main__":
    raise SystemExit(main())
