"""Competency checks over a Dataset (entailed, or asserted only): SHACL shapes and SPARQL-vs-expected-CSV.

SHACL: <set>/<name>.shapes.ttl must conform. sh:Violation → failure, sh:Warning → warning,
sh:Info → info. pySHACL validates each named graph of a Dataset separately, so shapes are
always run against one merged Graph of every graph (asserted, plus inferred and closure when entailed).

SPARQL: <set>/<name>.rq is run by Oxigraph (pyoxigraph; rdflib's evaluator takes minutes on
joins that Oxigraph answers in milliseconds) on the same named graphs, the default graph
being their union, and compared with <set>/<name>.expected.csv (header row,
then one row per result) as an unordered multiset of rows; numeric cells are compared by
value. IRIs are written with the
query's own prefixes, literals by lexical form, unbound as an empty cell, blank nodes as
_:b. An ASK query has the single column 'ask' and the row 'true' or 'false'.
"""
from __future__ import annotations

import csv
import re
import threading
import weakref
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

import pyoxigraph as ox
from pyshacl import validate
from rdflib import BNode, Dataset, Graph, Literal, URIRef
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID
from rdflib.namespace import RDF, RDFS, SH

PREFIX_LINE = re.compile(r'^\s*PREFIX\s+([A-Za-z][\w.-]*)?:\s*<([^>]*)>', re.I | re.M)
LOCAL_NAME = re.compile(r'[A-Za-z0-9_.-]*')
KINDS = {SH.Violation: 'failure', SH.Warning: 'warning', SH.Info: 'info'}


@dataclass
class Finding:
    kind: str        # 'failure' | 'warning' | 'info' | 'broken'
    file: Path
    title: str
    message: str


def union_graph(ds: Dataset) -> Graph:
    graph = Graph()
    for s, p, o, _ in ds.quads((None, None, None, None)):
        graph.add((s, p, o))
    return graph


def run_shacl(shapes_path: Path, ds: Dataset) -> list[Finding]:
    title = Path(shapes_path).name.removesuffix('.shapes.ttl')
    try:
        shapes = Graph().parse(str(shapes_path), format='turtle')
    except Exception as e:  # noqa: BLE001 — any parse error means a broken test file
        return [Finding('broken', shapes_path, title, f'cannot parse shapes: {e}')]
    try:
        _, results, _ = validate(union_graph(ds), shacl_graph=shapes, advanced=True, inference='none',
                                 allow_warnings=True)
    except Exception as e:  # noqa: BLE001 — e.g. pySHACL ConstraintLoadError for an invalid constraint
        return [Finding('broken', shapes_path, title, f'cannot load shapes: {e}')]
    findings = []
    for result in results.subjects(RDF.type, SH.ValidationResult):
        source = results.value(result, SH.sourceShape)
        owner = next(shapes.subjects(SH.property, source), None)
        label = shapes.value(source, RDFS.label) or (owner is not None and shapes.value(owner, RDFS.label))
        focus = results.value(result, SH.focusNode)
        message = results.value(result, SH.resultMessage) or results.value(result, SH.sourceConstraintComponent)
        findings.append(Finding(KINDS.get(results.value(result, SH.resultSeverity), 'failure'), shapes_path,
                                str(label) if label else title, f'{focus}: {message}'))
    return sorted(findings, key=lambda f: (f.kind, f.message))


def query_prefixes(text: str) -> dict[str, str]:
    return {prefix or '': iri for prefix, iri in PREFIX_LINE.findall(text)}


def render_term(term, prefixes: dict[str, str]) -> str:
    if term is None:
        return ''
    if isinstance(term, BNode):
        return '_:b'
    if isinstance(term, Literal):
        return str(term)
    iri = str(term)
    for prefix, namespace in sorted(prefixes.items(), key=lambda kv: -len(kv[1])):
        if namespace and iri.startswith(namespace) and LOCAL_NAME.fullmatch(iri[len(namespace):]):
            return f'{prefix}:{iri[len(namespace):]}'
    return iri


_STORES: 'weakref.WeakKeyDictionary[Dataset, ox.Store]' = weakref.WeakKeyDictionary()
_STORES_LOCK = threading.Lock()


def _to_ox(term):
    if isinstance(term, URIRef):
        return ox.NamedNode(str(term))
    if isinstance(term, BNode):
        return ox.BlankNode(str(term))
    if term.language:
        return ox.Literal(str(term), language=term.language)
    if term.datatype:
        return ox.Literal(str(term), datatype=ox.NamedNode(str(term.datatype)))
    return ox.Literal(str(term))


def _from_ox(term):
    if term is None:
        return None
    if isinstance(term, ox.NamedNode):
        return URIRef(term.value)
    if isinstance(term, ox.BlankNode):
        return BNode(term.value)
    return Literal(term.value)   # rendered by lexical form only


def _graph_name(context):
    name = getattr(context, 'identifier', context)    # a Graph or its identifier, by rdflib version
    if name is None or isinstance(name, BNode) or name == DATASET_DEFAULT_GRAPH_ID:
        return ox.DefaultGraph()
    return ox.NamedNode(str(name))


def oxigraph_store(ds: Dataset) -> ox.Store:
    """An in-memory Oxigraph copy of the Dataset's named graphs, built once per Dataset."""
    with _STORES_LOCK:
        store = _STORES.get(ds)
        if store is None:
            store = ox.Store()
            store.extend(ox.Quad(_to_ox(s), _to_ox(p), _to_ox(o), _graph_name(g))
                         for s, p, o, g in ds.quads((None, None, None, None)))
            _STORES[ds] = store
        return store


def run_sparql(query_path: Path, ds: Dataset) -> tuple[list[str], list[tuple[str, ...]]]:
    """Header and rows; raises ValueError for a query that cannot be parsed or run."""
    text = Path(query_path).read_text()
    try:
        result = oxigraph_store(ds).query(text, use_default_graph_as_union=True)
        if isinstance(result, ox.QueryBoolean):
            return ['ask'], [('true' if bool(result) else 'false',)]
        if not isinstance(result, ox.QuerySolutions):
            raise ValueError('CONSTRUCT or DESCRIBE query: competency tests must be SELECT or ASK')
        prefixes = query_prefixes(text)
        header = [v.value for v in result.variables]
        # evaluation is lazy, so errors can surface while iterating: keep it inside the try
        return header, [tuple(render_term(_from_ox(row[v]), prefixes) for v in header) for row in result]
    except ValueError:
        raise
    except Exception as e:  # noqa: BLE001 — pyoxigraph raises SyntaxError, OSError, ... for bad queries
        raise ValueError(str(e)) from e


NUMBER = re.compile(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')


def _cell_key(cell: str):
    """Numbers compare by value (engines write 25.0 as "25.0" or "25"); anything else by text."""
    return Decimal(cell) if NUMBER.fullmatch(cell) else cell


def compare_rows(expected: list[tuple], actual: list[tuple]) -> tuple[list[tuple], list[tuple]]:
    def keyed(rows):
        originals: dict[tuple, list[tuple]] = {}
        for row in rows:
            originals.setdefault(tuple(_cell_key(c) for c in row), []).append(row)
        return Counter({k: len(v) for k, v in originals.items()}), originals
    (want, want_rows), (got, got_rows) = keyed(expected), keyed(actual)
    missing = [want_rows[k][0] for k in (want - got).elements()]
    unexpected = [got_rows[k][0] for k in (got - want).elements()]
    return sorted(missing), sorted(unexpected)


def read_expected(path: Path) -> tuple[list[str], list[tuple[str, ...]]]:
    with open(path, newline='', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    rows = [r for r in rows if r]   # a trailing blank line is not a row (an unbound cell is written as "")
    return (rows[0] if rows else []), [tuple(r) for r in rows[1:]]


def write_expected(path: Path, header: list[str], rows: list[tuple]) -> None:
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(sorted(rows))


def check_sparql(query_path: Path, ds: Dataset, update: bool) -> list[Finding]:
    query_path = Path(query_path)
    title = query_path.stem
    expected_path = query_path.with_suffix('.expected.csv')
    try:
        header, rows = run_sparql(query_path, ds)
    except ValueError as e:
        return [Finding('broken', query_path, title, f'query failed: {e}')]
    expected_header, expected_rows = read_expected(expected_path) if expected_path.exists() else ([], [])
    # Follow the expected file's column order (SELECT * order is engine-dependent).
    if sorted(expected_header) == sorted(header) and expected_header != header:
        order = [header.index(column) for column in expected_header]
        header, rows = expected_header, [tuple(row[i] for i in order) for row in rows]
    if update:
        write_expected(expected_path, header, rows)
        return []
    if not expected_path.exists():
        return [Finding('broken', query_path, title,
                        f'no {expected_path.name}; create it with --update-expected and review it')]
    if expected_header != header:
        return [Finding('failure', expected_path, title,
                        f'columns {header} do not match expected {expected_header}')]
    missing, unexpected = compare_rows(expected_rows, rows)
    return ([Finding('failure', expected_path, title, 'missing row: ' + ', '.join(r)) for r in missing] +
            [Finding('failure', expected_path, title, 'unexpected row: ' + ', '.join(r)) for r in unexpected])
