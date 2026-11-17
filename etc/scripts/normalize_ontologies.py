#!/usr/bin/env python3
"""Normalize the IOF ontology files reachable from the AboutIOF packaging files.

For every IOF ontology transitively imported by ``AboutIOFDev.rdf`` /
``AboutIOFProd.rdf`` (imports resolved through ``catalog-v001.xml``) this:

  1. normalizes namespace prefixes to the canonical set in ``PREFIXES``
     (xmlns declarations, DOCTYPE ``<!ENTITY>`` declarations, ``&prefix;``
     references and ``prefix:`` element/attribute names);
  2. sets ``iof-av:copyright`` on the ``owl:Ontology`` header (adding it if missing);
  3. sets ``owl:versionIRI`` to ``.../ontology/<version>/<path>`` (adding it if missing);
  4. adds ``rdfs:isDefinedBy <ontology IRI>`` to IOF entities (owl:Class,
     ObjectProperty, DatatypeProperty, NamedIndividual, AnnotationProperty) that
     have none anywhere in the import closure, in the file that defines them
     (see ``plan_is_defined_by``);
  5. sets ``xml:lang="en-US"`` (upper-case ``US``) on natural-language annotations
     (labels, definitions, examples, notes … see ``ENGLISH_ANNOTATIONS``) that
     have no tag or an ``en`` / ``en-us`` tag.

Edits are made on the raw text (no RDF parse/serialize round trip), so the DOCTYPE
entities, comments, attribute quoting, ordering and indentation are preserved and
only the lines that need to change are touched. Running it twice is a no-op.
Cached third-party ontologies (``cache/``) and non-IOF ontologies are never touched.

Usage (from the repository root):

    python etc/scripts/normalize_ontologies.py 202603            # fix in place
    python etc/scripts/normalize_ontologies.py --check 202603    # report only; exit 1 if changes needed
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

IOF_BASE = "https://spec.industrialontologies.org/ontology/"
XSD = "http://www.w3.org/2001/XMLSchema#"
CATALOG_NS = "{urn:oasis:names:tc:entity:xmlns:xml:catalog}"
COPYRIGHT_HOLDER = "Open Applications Group"
FIRST_COPYRIGHT_YEAR = 2022

# Canonical prefix for each namespace (same table as correct_prefixes.rb).
# Extend here to normalize more namespaces.
PREFIXES: dict[str, str] = {
    "http://purl.obolibrary.org/obo/": "bfo",
    "http://purl.org/dc/elements/1.1/": "dc",
    "http://purl.org/dc/terms/": "dcterms",
    "http://www.w3.org/2002/07/owl#": "owl",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
    "http://www.w3.org/2004/02/skos/core#": "skos",
    XSD: "xsd",
    IOF_BASE + "annotation/": "iof-av",
    IOF_BASE + "construct/": "iof-constr",
    IOF_BASE + "individual/": "iof-ind",
}

VERSION_SEGMENT = re.compile(r"/\d{6}/")

# Top-level elements that declare an entity (same set update_annotations.rb used).
ENTITY_DECLARATIONS = {"owl:Class", "owl:ObjectProperty", "owl:DatatypeProperty",
                       "owl:NamedIndividual", "owl:AnnotationProperty"}
# Children that mark a declaration as the defining one rather than a re-declared stub.
DEFINING_CHILDREN = {"rdfs:label", "skos:prefLabel", "skos:definition"}

# Natural-language (American English) annotations: plain literals of these must
# carry xml:lang="en-US" (hygiene: testHygiene_labels / _annotations_language_tag).
# Deliberately excluded: FOL formulas, IRIs/citations (adaptedFrom, isDefinedBy),
# acronyms/abbreviations, contributor/creator names and the copyright statement.
LANGUAGE = "en-US"
ENGLISH_ANNOTATIONS = {
    "rdfs:label", "rdfs:comment",
    "skos:prefLabel", "skos:altLabel", "skos:definition", "skos:example",
    "skos:scopeNote", "skos:note", "skos:editorialNote", "skos:changeNote",
    "dcterms:title", "dcterms:abstract", "dcterms:description",
    "iof-av:naturalLanguageDefinition",
    "iof-av:semiFormalNaturalLanguageDefinition", "iof-av:semiFormalNaturalLanguageAxiom",
    "iof-av:explanatoryNote", "iof-av:usageNote", "iof-av:primitiveRationale",
    "iof-av:synonym", "iof-av:counterExample",
}
# Tags treated as a mis-spelling of en-US (compared lower-case); any other
# language (fr, de, …) is left alone.
ENGLISH_VARIANTS = {"", "en", "en-us"}

# --------------------------------------------------------------------------- #
# Minimal XML tag scanner (positions in the raw text, so we can splice edits)
# --------------------------------------------------------------------------- #

ATTR_RE = re.compile(r"""([^\s=/>]+)\s*=\s*("[^"]*"|'[^']*')""")
TAG_RE = re.compile(
    r"""<!--.*?-->"""                                  # comment
    r"""|<!\[CDATA\[.*?\]\]>"""                         # CDATA
    r"""|<\?.*?\?>"""                                   # processing instruction
    r"""|<!DOCTYPE(?:[^\[>]|\[.*?\])*>"""               # doctype incl. internal subset
    r"""|<(/?)([^\s/>!?]+)((?:\s+[^\s=/>]+\s*=\s*(?:"[^"]*"|'[^']*'))*)\s*(/?)>""",
    re.S,
)
ENTITY_DECL_RE = re.compile(r"""<!ENTITY\s+([^\s"']+)\s+(["'])(.*?)\2\s*>""")
XMLNS_RE = re.compile(r"""xmlns:([^\s=]+)\s*=\s*(["'])(.*?)\2""")


@dataclass
class Element:
    name: str
    attrs: dict[str, str]
    start: int            # offset of '<' of the open tag
    open_end: int         # offset just past the open tag's '>'
    end: int = -1         # offset just past the close tag (== open_end if empty)
    close_start: int = -1  # offset of '</' (== -1 for empty elements)
    empty: bool = False
    children: list["Element"] = field(default_factory=list)
    text: str = ""


def parse(text: str) -> Element | None:
    """Return the document element (rdf:RDF) with its child tree."""
    stack: list[Element] = []
    root = None
    for m in TAG_RE.finditer(text):
        if m.group(2) is None:          # comment / PI / doctype / CDATA
            continue
        closing, name, attr_text, selfclose = m.group(1), m.group(2), m.group(3), m.group(4)
        if closing:
            el = stack.pop()
            el.close_start, el.end = m.start(), m.end()
            el.text = text[el.open_end:el.close_start]
            continue
        attrs = {k: v[1:-1] for k, v in ATTR_RE.findall(attr_text)}
        el = Element(name, attrs, m.start(), m.end())
        if stack:
            stack[-1].children.append(el)
        else:
            root = el
        if selfclose:
            el.empty, el.end = True, m.end()
        else:
            stack.append(el)
    return root


def entities(text: str) -> dict[str, str]:
    return {name: value for name, _, value in ENTITY_DECL_RE.findall(text)}


def namespaces(text: str) -> list[tuple[str, str]]:
    root_open = re.search(r"<rdf:RDF\b[^>]*>", text, re.S)
    return [(p, uri) for p, _, uri in XMLNS_RE.findall(root_open.group(0))] if root_open else []


def expand(value: str, ents: dict[str, str]) -> str:
    value = re.sub(r"&([^;\s&]+);", lambda m: ents.get(m.group(1), m.group(0)), value)
    return (value.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
            .replace("&apos;", "'").replace("&amp;", "&"))


def line_indent(text: str, pos: int) -> str:
    line_start = text.rfind("\n", 0, pos) + 1
    return re.match(r"[ \t]*", text[line_start:]).group(0)


def newline_of(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


# --------------------------------------------------------------------------- #
# Discovery: AboutIOF* → transitive imports via the catalog
# --------------------------------------------------------------------------- #

def read_catalog(path: Path) -> dict[str, Path]:
    if not path.exists():
        return {}
    out = {}
    for uri in ET.parse(path).getroot().iter(CATALOG_NS + "uri"):
        out[uri.attrib["name"]] = (path.parent / uri.attrib["uri"]).resolve()
    return out


@dataclass
class OntologyFile:
    path: Path
    text: str
    root: Element
    onto: Element
    iri: str
    ents: dict[str, str]
    base: str


def load(path: Path) -> OntologyFile | None:
    text = path.read_text(encoding="utf-8")
    root = parse(text)
    if root is None:
        return None
    ents = entities(text)
    base = expand(root.attrs.get("xml:base", ""), ents)
    onto = next((c for c in root.children if c.name == "owl:Ontology"), None)
    if onto is None:
        return None
    iri = urljoin(base, expand(onto.attrs.get("rdf:about", ""), ents))
    return OntologyFile(path, text, root, onto, iri, ents, base)


def imports_of(of: OntologyFile) -> list[str]:
    return [expand(c.attrs["rdf:resource"], of.ents)
            for c in of.onto.children if c.name == "owl:imports" and "rdf:resource" in c.attrs]


def resolve(iri: str, catalogs: list[dict[str, Path]]) -> Path | None:
    candidates = [iri, VERSION_SEGMENT.sub("/", iri, count=1)]
    candidates += [c.rstrip("/") for c in candidates] + [c + "/" for c in candidates if not c.endswith("/")]
    hits = [cat[c] for cat in catalogs for c in candidates if c in cat]
    return next((p for p in hits if p.exists()), hits[0] if hits else None)


def discover(roots: list[Path], repo: Path) -> list[Path]:
    """Return the IOF ontology files reachable from ``roots``, in visit order."""
    root_catalog = read_catalog(repo / "catalog-v001.xml")
    seen: dict[Path, None] = {}
    pending = [p.resolve() for p in roots]
    while pending:
        path = pending.pop(0)
        if path in seen:
            continue
        seen[path] = None
        of = load(path)
        if of is None:
            print(f"::warning file={path}::no owl:Ontology header, skipping its imports")
            continue
        catalogs = [read_catalog(path.parent / "catalog-v001.xml"), root_catalog]
        for iri in imports_of(of):
            target = resolve(iri, catalogs)
            if target is None:
                print(f"::warning file={path.relative_to(repo)}::unresolved import <{iri}>")
            elif not target.exists():
                print(f"::warning file={path.relative_to(repo)}::catalog maps <{iri}> to missing {target}")
            else:
                pending.append(target)
    return [p for p in seen if is_iof_file(p, repo)]


def is_iof_file(path: Path, repo: Path) -> bool:
    rel = path.relative_to(repo) if path.is_relative_to(repo) else None
    if rel is None or "cache" in rel.parts:
        return False
    of = load(path)
    return of is not None and of.iri.startswith(IOF_BASE) and not of.iri.startswith(IOF_BASE + "cache/")


# --------------------------------------------------------------------------- #
# Fixes — each takes the text and returns (new_text, messages)
# --------------------------------------------------------------------------- #

def fix_prefixes(text: str) -> tuple[str, list[str]]:
    msgs: list[str] = []
    decls = namespaces(text)
    bound = {p: uri for p, uri in decls}
    ents = entities(text)
    renames: dict[str, str] = {}
    drop_xmlns: set[str] = set()
    for prefix, uri in decls:
        canon = PREFIXES.get(uri)
        if canon is None or prefix == canon:
            continue
        if canon in bound and bound[canon] != uri:
            msgs.append(f"::warning::cannot rename {prefix}: → {canon}: ({canon}: is bound to <{bound[canon]}>)")
            continue
        renames[prefix] = canon
        if canon in bound:
            drop_xmlns.add(prefix)          # canonical one already declared → just drop the alias
        msgs.append(f"prefix {prefix}: → {canon}: <{uri}>")
    if not renames:
        return text, msgs

    # xmlns declarations
    def xmlns_sub(m: re.Match) -> str:
        p = m.group(2)
        if p in drop_xmlns:
            return ""
        return m.group(1) + "xmlns:" + renames.get(p, p) + m.group(3)
    text = re.sub(r"""(\s+)xmlns:([^\s=]+)(\s*=\s*(?:"[^"]*"|'[^']*'))""", xmlns_sub, text)

    # DOCTYPE entity declarations: rename, or drop when the canonical one exists
    def entity_sub(m: re.Match) -> str:
        name = m.group(3)
        if name not in renames:
            return m.group(0)
        if renames[name] in ents:
            return ""
        return m.group(1) + m.group(2) + renames[name] + m.group(4)
    text = re.sub(r"""([ \t]*)(<!ENTITY\s+)([^\s"']+)(\s+(["']).*?\5\s*>(?:[ \t]*\r?\n)?)""",
                  entity_sub, text)

    # entity references
    for old, new in renames.items():
        text = text.replace(f"&{old};", f"&{new};")

    # element and attribute names
    names = "|".join(re.escape(o) for o in renames)
    def tag_sub(m: re.Match) -> str:
        if m.group(2) is None:
            return m.group(0)
        tag = m.group(0)
        tag = re.sub(rf"^(</?)({names}):", lambda t: t.group(1) + renames[t.group(2)] + ":", tag)
        tag = re.sub(rf"(\s)({names}):(?=[^\s=/>]+\s*=)", lambda t: t.group(1) + renames[t.group(2)] + ":", tag)
        return tag
    text = TAG_RE.sub(tag_sub, text)
    return text, msgs


def ensure_namespace(text: str, prefix: str, uri: str) -> str:
    """Declare ``prefix`` (xmlns + DOCTYPE entity, when there is a DOCTYPE) if absent."""
    if prefix not in dict(namespaces(text)):
        decls = list(XMLNS_RE.finditer(text))
        last = decls[-1]
        indent = line_indent(text, last.start())
        text = text[:last.end()] + f'{newline_of(text)}{indent}xmlns:{prefix}="{uri}"' + text[last.end():]
    if "<!DOCTYPE" in text and prefix not in entities(text):
        decls = list(ENTITY_DECL_RE.finditer(text))
        if decls:
            last = decls[-1]
            indent = line_indent(text, last.start())
            text = text[:last.end()] + f'{newline_of(text)}{indent}<!ENTITY {prefix} "{uri}">' + text[last.end():]
    return text


def insert_child(text: str, el: Element, child: str, at_end: bool = True) -> str:
    """Insert ``child`` (one line of markup) into ``el`` keeping the file's indentation."""
    nl = newline_of(text)
    indent = line_indent(text, el.start)
    if el.children:
        child_indent = line_indent(text, el.children[0].start)
    else:
        child_indent = indent + ("\t" if "\t" in indent or not indent else "  ")
    if el.empty:
        open_tag = text[el.start:el.end]
        new = re.sub(r"\s*/>$", ">", open_tag) + f"{nl}{child_indent}{child}{nl}{indent}</{el.name}>"
        return text[:el.start] + new + text[el.end:]
    if at_end:
        # put it after the last child's line, before the close tag line
        anchor = el.children[-1].end if el.children else el.open_end
        return text[:anchor] + f"{nl}{child_indent}{child}" + text[anchor:]
    return text[:el.open_end] + f"{nl}{child_indent}{child}" + text[el.open_end:]


def fix_header(text: str, version: str, copyright_text: str) -> tuple[str, list[str]]:
    msgs: list[str] = []
    for _ in range(2):  # re-parse after each structural insert
        of = _reparse(text)
        onto = of.onto
        version_iri = IOF_BASE + version + "/" + of.iri[len(IOF_BASE):]

        # versionIRI
        vi = [c for c in onto.children if c.name == "owl:versionIRI"]
        if not vi:
            msgs.append(f"add owl:versionIRI <{version_iri}>")
            text = insert_child(text, onto, f'<owl:versionIRI rdf:resource="{version_iri}"/>')
            continue
        current = expand(vi[0].attrs.get("rdf:resource", ""), of.ents)
        if current != version_iri:
            msgs.append(f"versionIRI <{current}> → <{version_iri}>")
            tag = text[vi[0].start:vi[0].open_end]
            new_tag = re.sub(r"""(rdf:resource\s*=\s*)(["']).*?\2""", lambda m: f'{m.group(1)}{m.group(2)}{version_iri}{m.group(2)}', tag)
            text = text[:vi[0].start] + new_tag + text[vi[0].open_end:]
            of = _reparse(text)
            onto = of.onto

        # copyright
        cr = [c for c in onto.children if c.name == "iof-av:copyright"]
        if not cr:
            msgs.append("add iof-av:copyright")
            text = ensure_namespace(text, "iof-av", IOF_BASE + "annotation/")
            of = _reparse(text)
            text = insert_child(text, of.onto, f"<iof-av:copyright>{copyright_text}</iof-av:copyright>")
            continue
        for c in cr:
            if c.empty or c.text.strip() != copyright_text:
                msgs.append(f"copyright '{c.text.strip()}' → '{copyright_text}'")
                new = f"<iof-av:copyright>{copyright_text}</iof-av:copyright>"
                text = text[:c.start] + new + text[c.end:]
                break  # offsets moved: loop re-parses
        else:
            break
    return text, msgs


def _reparse(text: str) -> OntologyFile:
    root = parse(text)
    ents = entities(text)
    base = expand(root.attrs.get("xml:base", ""), ents)
    onto = next(c for c in root.children if c.name == "owl:Ontology")
    iri = urljoin(base, expand(onto.attrs.get("rdf:about", ""), ents))
    return OntologyFile(Path(), text, root, onto, iri, ents, base)


LANG_ATTR_RE = re.compile(r"""(\sxml:lang\s*=\s*)(["'])(.*?)\2""")


def fix_language(text: str) -> tuple[str, list[str]]:
    """Give every plain-literal natural-language annotation xml:lang="en-US"."""
    msgs: list[str] = []
    root = parse(text)
    edits: list[Element] = []
    typed = 0

    def walk(el: Element, inherited: str) -> None:
        nonlocal typed
        lang = el.attrs.get("xml:lang", inherited)
        if (el.name in ENGLISH_ANNOTATIONS and not el.empty and not el.children
                and not {"rdf:resource", "rdf:parseType", "rdf:nodeID"} & el.attrs.keys()):
            if "rdf:datatype" in el.attrs:
                typed += 1
            elif lang != LANGUAGE and lang.lower() in ENGLISH_VARIANTS:
                edits.append(el)
        for c in el.children:
            walk(c, lang)

    walk(root, "")
    for el in sorted(edits, key=lambda e: e.start, reverse=True):
        tag = text[el.start:el.open_end]
        if LANG_ATTR_RE.search(tag):
            new_tag = LANG_ATTR_RE.sub(lambda m: f"{m.group(1)}{m.group(2)}{LANGUAGE}{m.group(2)}", tag, count=1)
        else:
            new_tag = tag[:1 + len(el.name)] + f' xml:lang="{LANGUAGE}"' + tag[1 + len(el.name):]
        text = text[:el.start] + new_tag + text[el.open_end:]
    if edits:
        counts: dict[tuple[str, str], int] = {}
        for el in edits:
            key = (el.name, el.attrs.get("xml:lang", "none"))
            counts[key] = counts.get(key, 0) + 1
        for (name, was), n in sorted(counts.items()):
            msgs.append(f"xml:lang {was} → {LANGUAGE} on {n} {name}")
    if typed:
        msgs.append(f"::warning::{typed} natural-language annotation(s) are typed literals (rdf:datatype), not en-US strings; left unchanged")
    return text, msgs


def subject_iri(el: Element, of: OntologyFile) -> str | None:
    if "rdf:about" in el.attrs:
        return urljoin(of.base, expand(el.attrs["rdf:about"], of.ents))
    if "rdf:ID" in el.attrs:
        return of.base.split("#")[0] + "#" + el.attrs["rdf:ID"]
    return None


def is_defining(el: Element) -> bool:
    """A declaration that actually defines the entity, not an empty re-declaration stub."""
    return any(c.name in DEFINING_CHILDREN for c in el.children)


def plan_is_defined_by(files: list[Path]) -> tuple[dict[Path, set[str]], list[str]]:
    """Decide, across the whole import closure, which file should get an
    ``rdfs:isDefinedBy`` for which entity.

    IOF entities live in shared namespaces (``construct/``, ``annotation/``, …),
    not under their module's IRI, and modules re-declare each other's entities
    as empty stubs. So an entity only gets an ``isDefinedBy`` when it has none
    anywhere in the closure, and only in the one file that defines it (the sole
    declaration, or the sole declaration carrying a label/definition).
    """
    have: set[str] = set()
    decls: dict[str, list[tuple[Path, bool]]] = {}
    for path in files:
        of = load(path)
        for el in of.root.children:
            iri = subject_iri(el, of)
            if iri is None:
                continue
            if any(c.name == "rdfs:isDefinedBy" for c in el.children):
                have.add(iri)
            if el.name in ENTITY_DECLARATIONS and iri.startswith(IOF_BASE):
                decls.setdefault(iri, []).append((path, is_defining(el)))

    plan: dict[Path, set[str]] = {}
    warnings: list[str] = []
    for iri, ds in decls.items():
        if iri in have:
            continue
        owners = {p for p, _ in ds}
        if len(owners) > 1:
            owners = {p for p, defining in ds if defining}
        if len(owners) == 1:
            plan.setdefault(owners.pop(), set()).add(iri)
        else:
            where = ", ".join(sorted(str(p) for p, _ in ds))
            warnings.append(f"::warning::<{iri}> has no rdfs:isDefinedBy and no single defining file ({where}); add it by hand")
    return plan, warnings


def fix_is_defined_by(text: str, iris: set[str]) -> tuple[str, list[str]]:
    msgs: list[str] = []
    if not iris:
        return text, msgs
    of = _reparse(text)
    targets: dict[str, Element] = {}
    for el in of.root.children:
        iri = subject_iri(el, of)
        if iri in iris and el.name in ENTITY_DECLARATIONS and iri not in targets:
            if any(c.name == "rdfs:isDefinedBy" for c in el.children):
                iris = iris - {iri}
            else:
                targets[iri] = el
    xsd_ref = "&xsd;" if entities(text).get("xsd") == XSD else XSD
    child = f'<rdfs:isDefinedBy rdf:datatype="{xsd_ref}anyURI">{of.iri}</rdfs:isDefinedBy>'
    # splice from the end of the file backwards so earlier offsets stay valid
    for iri, el in sorted(targets.items(), key=lambda x: x[1].start, reverse=True):
        msgs.append(f"add rdfs:isDefinedBy to {el.name} <{iri}>")
        text = insert_child(text, el, child)
    msgs.reverse()
    return text, msgs


# --------------------------------------------------------------------------- #

def normalize(path: Path, version: str, copyright_text: str, defined_here: set[str]) -> tuple[str, str, list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        original = f.read()
    text, msgs = original, []
    for step in (fix_prefixes,
                 lambda t: fix_header(t, version, copyright_text),
                 fix_language,
                 lambda t: fix_is_defined_by(t, defined_here)):
        text, m = step(text)
        msgs += m
    return original, text, msgs


def default_copyright(version: str) -> str:
    last = int(version[:4]) if re.fullmatch(r"\d{6}", version) else date.today().year
    years = ", ".join(str(y) for y in range(FIRST_COPYRIGHT_YEAR, last + 1))
    return f"Copyright (c) {years} {COPYRIGHT_HOLDER}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("version", help="release version for owl:versionIRI, e.g. 202603")
    ap.add_argument("--about", nargs="+", default=["AboutIOFDev.rdf", "AboutIOFProd.rdf"],
                    help="root packaging files (default: AboutIOFDev.rdf AboutIOFProd.rdf)")
    ap.add_argument("--repo", default=".", help="ontology repository root (default: .)")
    ap.add_argument("--copyright", help="copyright text (default: 'Copyright (c) 2022, …, <version year> "
                    f"{COPYRIGHT_HOLDER}')")
    ap.add_argument("--check", action="store_true", help="report what would change; write nothing; exit 1 if anything would")
    ap.add_argument("-q", "--quiet", action="store_true", help="only print files that change")
    args = ap.parse_args()

    if not re.fullmatch(r"\d{6}", args.version):
        ap.error("version must be six digits, e.g. 202603")
    repo = Path(args.repo).resolve()
    copyright_text = args.copyright or default_copyright(args.version)

    files = discover([repo / a for a in args.about], repo)
    plan, warnings = plan_is_defined_by(files)
    for w in warnings:
        print(w)
    changed = 0
    for path in files:
        rel = path.relative_to(repo)
        original, text, msgs = normalize(path, args.version, copyright_text, plan.get(path, set()))
        if text == original:
            if not args.quiet:
                print(f"ok      {rel}")
            continue
        changed += 1
        print(f"{'would fix' if args.check else 'fixed'}  {rel}")
        for m in msgs:
            print(f"    {m}")
        if not args.check:
            with path.open("w", encoding="utf-8", newline="") as f:
                f.write(text)
    print(f"\n{len(files)} ontologies, {changed} {'need changes' if args.check else 'changed'}")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    sys.exit(main())
