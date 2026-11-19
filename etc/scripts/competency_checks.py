"""Competency checks over an entailed Dataset: SHACL shapes and SPARQL-vs-expected-CSV.

SHACL: tests/<name>.shapes.ttl must conform. sh:Violation → failure, sh:Warning → warning,
sh:Info → info. pySHACL validates each named graph of a Dataset separately, so shapes are
always run against one merged Graph of every graph (asserted + inferred + closure).

SPARQL: tests/<name>.rq is run and compared with tests/<name>.expected.csv (header row,
then one row per result) as an unordered multiset of rows. IRIs are written with the
query's own prefixes, literals by lexical form, unbound as an empty cell, blank nodes as
_:b. An ASK query has the single column 'ask' and the row 'true' or 'false'.
"""
from __future__ import annotations

import csv
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from pyshacl import validate
from rdflib import BNode, Dataset, Graph, Literal, URIRef
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


def run_sparql(query_path: Path, ds: Dataset) -> tuple[list[str], list[tuple[str, ...]]]:
    """Header and rows; raises ValueError for a query that cannot be parsed or run."""
    text = Path(query_path).read_text()
    try:
        result = ds.query(text)
        if result.type == 'ASK':
            return ['ask'], [('true' if result.askAnswer else 'false',)]
        if result.type != 'SELECT':
            raise ValueError(f'{result.type} query: competency tests must be SELECT or ASK')
        prefixes = query_prefixes(text)
        header = [str(v) for v in result.vars]
        # rdflib evaluates lazily, so errors can surface while iterating: keep it inside the try
        return header, [tuple(render_term(row[v], prefixes) for v in result.vars) for row in result]
    except ValueError:
        raise
    except Exception as e:  # noqa: BLE001 — rdflib raises several parser/evaluation exception types
        raise ValueError(str(e)) from e


def compare_rows(expected: list[tuple], actual: list[tuple]) -> tuple[list[tuple], list[tuple]]:
    want, got = Counter(expected), Counter(actual)
    return sorted((want - got).elements()), sorted((got - want).elements())


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
    # Column order of SELECT * is not stable between runs in rdflib: follow the expected file's.
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
