#!/usr/bin/env python3
"""
IOF FOL Fixer

Resolves the two most common MUST violations found by annotation_checker.py:

  1. Classes with an existing owl:equivalentClass expression:
     → Translates the OWL axiom to iof-av:firstOrderLogicDefinition (FOL) and
       iof-av:semiFormalNaturalLanguageDefinition (SFNL).
     → Removes iof-av:isPrimitive / iof-av:primitiveRationale if present (an
       axiom supersedes the primitive flag — this is the "override" behaviour).

  2. Classes with only rdfs:subClassOf (no OWL restrictions, no FOL):
     → Sets iof-av:isPrimitive = true
     → Adds iof-av:primitiveRationale generated from the parent label.

  3. Classes already marked isPrimitive=true but missing primitiveRationale:
     → Adds the rationale.

The script is idempotent and re-entrant: run it again after adding an
owl:equivalentClass to a previously-primitive term and it will automatically
promote that term to formally defined.

Usage:
    python fol_fixer.py [--directory PATH] [--file FILE] [--apply]

    --directory  Directory of ontology files (default: current dir)
    --file       Process only this single file (for testing)
    --apply      Write changes to files (default: dry-run, print only)
"""

import os
import re
import sys
import glob
import argparse
from rdflib import Graph, RDF, RDFS, OWL, URIRef, Literal, Namespace, BNode
from rdflib.namespace import XSD
from rdflib.collection import Collection

# ---------------------------------------------------------------------------
# Namespaces
# ---------------------------------------------------------------------------
IOF_AV = Namespace("https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/")

ONTOLOGY_EXTENSIONS = ("*.owl", "*.ttl", "*.rdf")

# Variable letters to use for existential/universal quantifiers (skip a/A per spec)
_EXIST_VARS = iter("bcdefghijklmnopqrstuvwxyz".replace("a", "").replace("r", "").replace("s", "").replace("t", ""))


def _fresh_var():
    """Return the next available single-letter variable (skips a, r, s, t)."""
    return next(_EXIST_VARS)


def _reset_vars():
    global _EXIST_VARS
    _EXIST_VARS = iter("bcdefghijklmnopqstuvwxyz")  # skips a, r, s, t


# ---------------------------------------------------------------------------
# Label / name helpers
# ---------------------------------------------------------------------------

def _en_label(g: Graph, iri) -> str:
    """Return the English rdfs:label string for an IRI, or the local name."""
    for lbl in g.objects(iri, RDFS.label):
        if isinstance(lbl, Literal) and lbl.language and lbl.language.lower().startswith("en"):
            return str(lbl)
    # fallback to local name
    s = str(iri)
    return s.rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def _to_upper_camel(label: str) -> str:
    """'some quality label' → 'SomeQualityLabel'"""
    return "".join(w.capitalize() for w in re.split(r"[\s_\-]+", label))


def _to_lower_camel(label: str) -> str:
    """'has part at some time' → 'hasPartAtSomeTime'"""
    parts = re.split(r"[\s_\-]+", label)
    return parts[0].lower() + "".join(w.capitalize() for w in parts[1:])


def _local_name(iri: str) -> str:
    s = str(iri)
    if "#" in s:
        return s.rsplit("#", 1)[1]
    return s.rsplit("/", 1)[-1]


def _prefix_for(iri: str, g: Graph) -> str:
    """
    Return a qualified name like 'obo:BFO_0000057' using the graph's namespace bindings,
    or fall back to the bare local name.
    """
    for prefix, ns in g.namespaces():
        ns_str = str(ns)
        if str(iri).startswith(ns_str) and prefix:
            local = str(iri)[len(ns_str):]
            if local:
                return f"{prefix}:{local}"
    return _local_name(str(iri))


def _class_name(g: Graph, node) -> str:
    """
    Return a name for a class IRI suitable for FOL use.
    - If the graph has an English label, convert it to UpperCamelCase.
    - If the local name already looks like UpperCamelCase (or is a BFO code), use prefix:LocalName.
    """
    if isinstance(node, BNode):
        return "?"
    iri_str = str(node)
    # Try English label first
    for lbl in g.objects(node, RDFS.label):
        if isinstance(lbl, Literal) and lbl.language and lbl.language.lower().startswith("en"):
            return _to_upper_camel(str(lbl))
    # Fallback: use prefix:LocalName for external IRIs
    local = _local_name(iri_str)
    # If local name already looks like CamelCase or an OBO code, keep as-is with prefix
    if re.match(r"^[A-Z]", local) or re.match(r"^[A-Z]+_\d+", local):
        return _prefix_for(iri_str, g)
    return _to_upper_camel(local)


def _prop_name(g: Graph, node) -> str:
    """
    Return a name for a property IRI suitable for FOL use (lowerCamelCase).
    - If the graph has an English label, convert it to lowerCamelCase.
    - If the local name already looks like lowerCamelCase, use it directly.
    - For external IRIs, use prefix:LocalName.
    """
    if isinstance(node, BNode):
        return "?"
    iri_str = str(node)
    # Try English label first
    for lbl in g.objects(node, RDFS.label):
        if isinstance(lbl, Literal) and lbl.language and lbl.language.lower().startswith("en"):
            return _to_lower_camel(str(lbl))
    # Fallback: check local name
    local = _local_name(iri_str)
    # If local name starts lowercase and has mixed case, it's already lowerCamelCase
    if re.match(r"^[a-z][a-zA-Z0-9]*$", local):
        return local
    # OBO code or other external — use prefix:LocalName
    return _prefix_for(iri_str, g)


# ---------------------------------------------------------------------------
# OWL class expression → FOL
# ---------------------------------------------------------------------------

def _collect_list(g: Graph, head) -> list:
    """Collect rdf:List items from a BNode head."""
    try:
        return list(Collection(g, head))
    except Exception:
        return []


def _owl_to_fol(node, g: Graph, var: str = "x", depth: int = 0) -> str:
    """
    Recursively translate an OWL class expression to a FOL string.
    `var` is the variable representing the current subject.
    Returns the FOL fragment (without the leading 'T(x) ↔' part).
    """
    if isinstance(node, URIRef):
        return f"{_class_name(g, node)}({var})"

    if not isinstance(node, BNode):
        return f"?({var})"

    # owl:intersectionOf
    lst = g.value(node, OWL.intersectionOf)
    if lst is not None:
        items = _collect_list(g, lst)
        parts = [_owl_to_fol(item, g, var, depth + 1) for item in items]
        inner = " ∧ ".join(parts)
        return f"({inner})" if len(parts) > 1 else inner

    # owl:unionOf
    lst = g.value(node, OWL.unionOf)
    if lst is not None:
        items = _collect_list(g, lst)
        parts = [_owl_to_fol(item, g, var, depth + 1) for item in items]
        inner = " ∨ ".join(parts)
        return f"({inner})" if len(parts) > 1 else inner

    # owl:complementOf
    complement = g.value(node, OWL.complementOf)
    if complement is not None:
        return f"¬{_owl_to_fol(complement, g, var, depth + 1)}"

    # owl:Restriction
    on_prop = g.value(node, OWL.onProperty)
    if on_prop is None:
        return f"?({var})"

    prop_name = _prop_name(g, on_prop)

    # someValuesFrom
    filler = g.value(node, OWL.someValuesFrom)
    if filler is not None:
        ev = _fresh_var()
        filler_fol = _owl_to_fol(filler, g, ev, depth + 1)
        return f"∃{ev} ({filler_fol} ∧ {prop_name}({var}, {ev}))"

    # allValuesFrom
    filler = g.value(node, OWL.allValuesFrom)
    if filler is not None:
        ev = _fresh_var()
        filler_fol = _owl_to_fol(filler, g, ev, depth + 1)
        return f"∀{ev} ({prop_name}({var}, {ev}) → {filler_fol})"

    # hasValue
    value = g.value(node, OWL.hasValue)
    if value is not None:
        val_str = _class_name(g, value) if isinstance(value, URIRef) else str(value)
        return f"{prop_name}({var}, {val_str})"

    # exact / min / max cardinality — simplified
    for card_pred, card_sym in [
        (OWL.exactCardinality, "="),
        (OWL.minCardinality, "≥"),
        (OWL.maxCardinality, "≤"),
        (OWL.qualifiedCardinality, "="),
    ]:
        card_val = g.value(node, card_pred)
        if card_val is not None:
            on_class = g.value(node, OWL.onClass) or g.value(node, OWL.onDataRange)
            class_part = f" {_class_name(g, on_class)}" if on_class else ""
            return f"|{{{ev}: {prop_name}({var}, {ev}){class_part}}}| {card_sym} {card_val}"

    return f"?({var})"


# ---------------------------------------------------------------------------
# OWL class expression → semi-formal natural language
# ---------------------------------------------------------------------------

def _owl_to_sfnl(node, g: Graph, subject_label: str = None) -> str:
    """
    Translate an OWL class expression to semi-formal natural language following
    the IOF format: "every instance of 'label' is defined as exactly ..."
    """
    inner = _sfnl_fragment(node, g)
    if subject_label:
        return f"every instance of '{subject_label}' is defined as exactly {inner}"
    return inner


def _sfnl_fragment(node, g: Graph) -> str:
    """Recursively build the SFNL fragment for a class expression node."""
    if isinstance(node, URIRef):
        lbl = _en_label(g, node)
        return f"an instance of '{lbl}'"

    if not isinstance(node, BNode):
        return "an unknown entity"

    # owl:intersectionOf
    lst = g.value(node, OWL.intersectionOf)
    if lst is not None:
        items = _collect_list(g, lst)
        parts = [_sfnl_fragment(item, g) for item in items]
        if len(parts) == 1:
            return parts[0]
        return " and ".join(parts[:-1]) + f" and {parts[-1]}"

    # owl:unionOf
    lst = g.value(node, OWL.unionOf)
    if lst is not None:
        items = _collect_list(g, lst)
        parts = [_en_label(g, item) if isinstance(item, URIRef) else _sfnl_fragment(item, g)
                 for item in items]
        quoted = [f"'{p}'" for p in parts]
        if len(quoted) == 1:
            return f"an instance of {quoted[0]}"
        return "an instance of " + ", ".join(quoted[:-1]) + f" or {quoted[-1]}"

    # owl:complementOf
    complement = g.value(node, OWL.complementOf)
    if complement is not None:
        return f"not {_sfnl_fragment(complement, g)}"

    # owl:Restriction
    on_prop = g.value(node, OWL.onProperty)
    if on_prop is None:
        return "an unknown restriction"

    prop_lbl = f"'{_prop_name(g, on_prop)}'"

    # someValuesFrom
    filler = g.value(node, OWL.someValuesFrom)
    if filler is not None:
        filler_lbl = (f"'{_en_label(g, filler)}'" if isinstance(filler, URIRef)
                      else _sfnl_fragment(filler, g))
        return f"that {prop_lbl} some {filler_lbl}"

    # allValuesFrom
    filler = g.value(node, OWL.allValuesFrom)
    if filler is not None:
        filler_lbl = (f"'{_en_label(g, filler)}'" if isinstance(filler, URIRef)
                      else _sfnl_fragment(filler, g))
        return f"where whenever {prop_lbl} y then y must be {filler_lbl}"

    # hasValue
    value = g.value(node, OWL.hasValue)
    if value is not None:
        val_str = (f"'{_en_label(g, value)}'" if isinstance(value, URIRef) else str(value))
        return f"where {prop_lbl} is {val_str}"

    # cardinality
    for card_pred, card_word in [
        (OWL.exactCardinality, "exactly"),
        (OWL.qualifiedCardinality, "exactly"),
        (OWL.minCardinality, "at least"),
        (OWL.maxCardinality, "at most"),
    ]:
        card_val = g.value(node, card_pred)
        if card_val is not None:
            on_class = g.value(node, OWL.onClass)
            class_part = (f" '{_en_label(g, on_class)}'" if on_class else "")
            return f"that {prop_lbl} {card_word} {card_val}{class_part}"

    return "an unknown restriction"


# ---------------------------------------------------------------------------
# Rationale generation
# ---------------------------------------------------------------------------

def _make_rationale(g: Graph, term: URIRef) -> str:
    label = _en_label(g, term)

    # Get first parent class label
    parents = [o for o in g.objects(term, RDFS.subClassOf) if isinstance(o, URIRef)]
    parent_label = _en_label(g, parents[0]) if parents else "a more general quality"

    rationale = (
        f"Necessary and sufficient conditions for '{label}' have not yet been formalized. "
        f"The term is defined as a specific subtype of '{parent_label}'. "
        f"Distinguishing criteria are domain-specific and depend on measurement conventions "
        f"or source terminology not yet expressed as OWL restrictions."
    )

    # If adaptedFrom exists, mention the source
    adapted = list(g.objects(term, IOF_AV.adaptedFrom))
    if adapted:
        sources = ", ".join(str(s) for s in adapted[:2])
        rationale += f" The definition is adapted from: {sources}."

    return rationale


# ---------------------------------------------------------------------------
# Term analysis
# ---------------------------------------------------------------------------

def analyse_term(g: Graph, term: URIRef):
    """
    Determine what action is needed for this term.

    Returns a dict:
      {
        'action': 'GENERATE_FOL' | 'CLEAR_PRIMITIVE' | 'SET_PRIMITIVE'
                  | 'ADD_RATIONALE' | 'OK',
        'fol': str or None,       # only for GENERATE_FOL
        'sfnl': str or None,      # only for GENERATE_FOL
        'rationale': str or None, # only for SET_PRIMITIVE / ADD_RATIONALE
      }
    """
    has_equiv = bool(list(g.objects(term, OWL.equivalentClass)))
    has_fol   = bool(list(g.objects(term, IOF_AV.firstOrderLogicDefinition)))
    has_sfnl  = bool(list(g.objects(term, IOF_AV.semiFormalNaturalLanguageDefinition)))
    prim_vals = list(g.objects(term, IOF_AV.isPrimitive))
    is_prim   = any(str(v).lower() == "true" for v in prim_vals if isinstance(v, Literal))
    has_rat   = bool(list(g.objects(term, IOF_AV.primitiveRationale)))

    # Term has OWL equivalentClass → should be formally defined
    if has_equiv:
        if is_prim:
            # Has axiom AND is marked primitive — the axiom wins
            return {"action": "CLEAR_PRIMITIVE", "fol": None, "sfnl": None, "rationale": None}
        if not (has_fol and has_sfnl):
            _reset_vars()
            fol_str, sfnl_str = _generate_fol_sfnl(g, term)
            return {"action": "GENERATE_FOL", "fol": fol_str, "sfnl": sfnl_str, "rationale": None}
        return {"action": "OK", "fol": None, "sfnl": None, "rationale": None}

    # No equivalentClass: term should be primitive
    if not has_fol:
        if not is_prim:
            rat = _make_rationale(g, term)
            return {"action": "SET_PRIMITIVE", "fol": None, "sfnl": None, "rationale": rat}
        if not has_rat:
            rat = _make_rationale(g, term)
            return {"action": "ADD_RATIONALE", "fol": None, "sfnl": None, "rationale": rat}

    return {"action": "OK", "fol": None, "sfnl": None, "rationale": None}


def _generate_fol_sfnl(g: Graph, term: URIRef):
    """Build FOL and SFNL strings from the term's owl:equivalentClass expressions."""
    equiv_nodes = list(g.objects(term, OWL.equivalentClass))
    term_label = _en_label(g, term)
    class_name = _to_upper_camel(term_label)

    fol_parts  = []
    sfnl_parts = []

    for eq_node in equiv_nodes:
        if isinstance(eq_node, URIRef):
            fol_parts.append(f"{_class_name(g, eq_node)}(x)")
            sfnl_parts.append(f"an instance of '{_en_label(g, eq_node)}'")
        elif isinstance(eq_node, BNode):
            fol_parts.append(_owl_to_fol(eq_node, g, var="x"))
            sfnl_parts.append(_sfnl_fragment(eq_node, g))

    if len(fol_parts) == 1:
        fol = f"{class_name}(x) ↔ {fol_parts[0]}"
        sfnl = f"every instance of '{term_label}' is defined as exactly {sfnl_parts[0]}"
    else:
        fol_joined = " ∧ ".join(fol_parts)
        fol = f"{class_name}(x) ↔ {fol_joined}"
        sfnl_joined = " and ".join(sfnl_parts)
        sfnl = f"every instance of '{term_label}' is defined as exactly {sfnl_joined}"

    return fol, sfnl


# ---------------------------------------------------------------------------
# Graph modification
# ---------------------------------------------------------------------------

def apply_changes(g: Graph, term: URIRef, info: dict) -> list:
    """
    Modify the graph in-place according to the action in `info`.
    Returns a list of human-readable change descriptions.
    """
    action = info["action"]
    changes = []

    if action == "OK":
        return changes

    if action == "GENERATE_FOL":
        # Remove existing FOL/SFNL if any (replace mode)
        for p in (IOF_AV.firstOrderLogicDefinition, IOF_AV.semiFormalNaturalLanguageDefinition):
            for o in list(g.objects(term, p)):
                g.remove((term, p, o))
        # Remove isPrimitive / primitiveRationale if somehow set
        _remove_primitive_annotations(g, term)

        g.add((term, IOF_AV.firstOrderLogicDefinition,
               Literal(info["fol"], lang="en")))
        g.add((term, IOF_AV.semiFormalNaturalLanguageDefinition,
               Literal(info["sfnl"], lang="en")))
        changes.append(f"  + firstOrderLogicDefinition: {info['fol']}")
        changes.append(f"  + semiFormalNaturalLanguageDefinition: {info['sfnl']}")

    elif action == "CLEAR_PRIMITIVE":
        removed = _remove_primitive_annotations(g, term)
        if removed:
            changes.append(f"  - Removed isPrimitive=true and primitiveRationale "
                            f"(OWL equivalentClass present)")

    elif action == "SET_PRIMITIVE":
        g.add((term, IOF_AV.isPrimitive,
               Literal("true", datatype=XSD.boolean)))
        g.add((term, IOF_AV.primitiveRationale,
               Literal(info["rationale"], lang="en")))
        changes.append("  + isPrimitive = true")
        changes.append(f"  + primitiveRationale: {info['rationale'][:80]}…")

    elif action == "ADD_RATIONALE":
        g.add((term, IOF_AV.primitiveRationale,
               Literal(info["rationale"], lang="en")))
        changes.append(f"  + primitiveRationale: {info['rationale'][:80]}…")

    return changes


def _remove_primitive_annotations(g: Graph, term: URIRef) -> bool:
    """Remove isPrimitive and primitiveRationale triples. Returns True if anything removed."""
    removed = False
    for p in (IOF_AV.isPrimitive, IOF_AV.primitiveRationale):
        for o in list(g.objects(term, p)):
            g.remove((term, p, o))
            removed = True
    return removed


# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------

def process_file(file_path: str, apply: bool) -> dict:
    """
    Analyse and optionally fix one ontology file.
    Returns a summary dict.
    """
    g = Graph()
    try:
        g.parse(file_path)
    except Exception as exc:
        return {"error": str(exc), "file": file_path}

    classes = [s for s in g.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)]

    results = {}
    for term in sorted(classes, key=str):
        info = analyse_term(g, term)
        if info["action"] != "OK":
            label = _en_label(g, term)
            results[str(term)] = {"label": label, "info": info}

    if apply and results:
        for term_iri, data in results.items():
            apply_changes(g, URIRef(term_iri), data["info"])
        # Re-bind the IOF_AV namespace so it serialises with the right prefix
        g.bind("iof-av", IOF_AV)
        g.serialize(destination=file_path, format="xml")

    return {
        "file": file_path,
        "total_classes": len(classes),
        "changes": results,
        "applied": apply,
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

_ACTION_LABEL = {
    "GENERATE_FOL":   "Generate FOL+SFNL from OWL axiom",
    "CLEAR_PRIMITIVE":"Remove isPrimitive (OWL axiom overrides)",
    "SET_PRIMITIVE":  "Set isPrimitive=true + rationale",
    "ADD_RATIONALE":  "Add missing primitiveRationale",
}


def print_report(file_results: list, apply: bool):
    mode = "APPLIED" if apply else "DRY RUN"
    print(f"\n{'='*70}")
    print(f"  IOF FOL Fixer  [{mode}]")
    print(f"{'='*70}\n")

    total_changes = 0
    action_counts = {}

    for r in file_results:
        if "error" in r:
            print(f"ERROR  {r['file']}: {r['error']}\n")
            continue

        fname = os.path.basename(r["file"])
        n = len(r["changes"])
        total_changes += n
        print(f"{'─'*60}")
        print(f"  {fname}  ({r['total_classes']} classes, {n} to fix)")
        print(f"{'─'*60}")

        if not r["changes"]:
            print("  (no changes needed)\n")
            continue

        for iri, data in sorted(r["changes"].items(), key=lambda x: x[1]["label"]):
            action = data["info"]["action"]
            action_counts[action] = action_counts.get(action, 0) + 1
            tag = _ACTION_LABEL.get(action, action)
            print(f"  [{action}] '{data['label']}'")
            print(f"    {tag}")
            # Show preview of generated content
            if action == "GENERATE_FOL":
                fol = data["info"]["fol"]
                sfnl = data["info"]["sfnl"]
                print(f"    FOL:  {fol[:100]}{'…' if len(fol) > 100 else ''}")
                print(f"    SFNL: {sfnl[:100]}{'…' if len(sfnl) > 100 else ''}")
            elif action in ("SET_PRIMITIVE", "ADD_RATIONALE"):
                rat = data["info"]["rationale"]
                print(f"    Rationale: {rat[:100]}{'…' if len(rat) > 100 else ''}")
        print()

    print(f"{'='*70}")
    print(f"  Summary: {total_changes} terms would be {'changed' if not apply else 'changed'}")
    for action, cnt in sorted(action_counts.items()):
        print(f"    {_ACTION_LABEL.get(action, action)}: {cnt}")
    if not apply:
        print("\n  Run with --apply to write changes to files.")
    print(f"{'='*70}\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def gather_files(directory):
    files = []
    for pattern in ONTOLOGY_EXTENSIONS:
        files.extend(glob.glob(os.path.join(directory, pattern)))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(
        description="Fix missing FOL definitions and isPrimitive annotations in IOF ontologies."
    )
    parser.add_argument(
        "--directory", "-d", default=".",
        help="Directory of ontology files (default: current dir)"
    )
    parser.add_argument(
        "--file", "-f", default=None,
        help="Process only this single file (overrides --directory)"
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Write changes to files (default: dry-run)"
    )
    args = parser.parse_args()

    if args.file:
        files = [args.file]
    else:
        files = gather_files(args.directory)
        if not files:
            print(f"No ontology files found in '{args.directory}'.")
            return 1

    results = []
    for f in files:
        print(f"  Processing {os.path.basename(f)} …", flush=True)
        results.append(process_file(f, apply=args.apply))

    print_report(results, apply=args.apply)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
