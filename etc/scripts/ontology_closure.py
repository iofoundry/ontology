"""Shared helpers for loading IOF ontologies offline: catalog resolution, import closure,
merging, and the HermiT input file. Used by hygiene_runner.py and the competency runner.

Nothing here fetches from the web: an owl:imports IRI is resolved only through a catalog
(or a mapping the caller adds), and anything else is reported as missing.
"""
from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

import owlready2
from rdflib import Graph
from rdflib.namespace import OWL, RDF

CATALOG_NS = '{urn:oasis:names:tc:entity:xmlns:xml:catalog}'

HERMIT_DIR = os.path.join(os.path.dirname(owlready2.__file__), 'hermit')
HERMIT_CLASSPATH = os.pathsep.join([HERMIT_DIR, os.path.join(HERMIT_DIR, 'HermiT.jar')])


class ClosureError(Exception):
    pass


@dataclass
class Closure:
    iris: set[str] = field(default_factory=set)
    files: list[Path] = field(default_factory=list)
    missing: list[tuple[str, Path]] = field(default_factory=list)   # (import IRI, importing file)


def load_catalog(path: Path) -> dict[str, Path]:
    """Map every catalog <uri> name to its file, as an absolute path."""
    path = Path(path).resolve()
    return {uri.attrib['name']: (path.parent / uri.attrib['uri']).resolve()
            for uri in ET.parse(path).getroot().iter(CATALOG_NS + 'uri')}


def ontology_iri(path: Path) -> str:
    """The IRI of the single owl:Ontology declared in a file."""
    iris = {str(s) for s in Graph().parse(source=str(path)).subjects(RDF.type, OWL.Ontology)}
    if len(iris) != 1:
        raise ClosureError(f'{path} declares {len(iris)} owl:Ontology headers; expected exactly 1')
    return iris.pop()


def import_closure(root_iris: list[str], resolution: dict[str, Path]) -> Closure:
    """Walk owl:imports transitively from root_iris, resolving IRIs only via resolution."""
    closure = Closure()
    pending = [(iri, None) for iri in reversed(root_iris)]
    parsed: set[Path] = set()
    while pending:
        iri, importer = pending.pop()
        if iri in closure.iris:
            continue
        if iri not in resolution:
            closure.missing.append((iri, importer))
            continue
        closure.iris.add(iri)
        file = resolution[iri]
        if file in parsed:
            continue
        parsed.add(file)
        closure.files.append(file)
        graph = Graph().parse(source=str(file))
        imports = [str(o) for s in graph.subjects(RDF.type, OWL.Ontology)
                   for o in graph.objects(s, OWL.imports)]
        pending.extend((i, file) for i in reversed(imports))
    return closure


def merge(files: list[Path]) -> Graph:
    data = Graph()
    for file in files:
        data.parse(source=str(file))
    return data


def reasoner_input(data: Graph, path) -> None:
    """Write the merged closure as one self-contained ontology for HermiT.

    owl:imports are dropped (everything they name is already merged in, and HermiT
    would otherwise fetch them from the web). rdf:langString is replaced by
    rdf:PlainLiteral: HermiT only accepts the OWL 2 datatype map, which lacks
    rdf:langString, and the Commons Text datatype is defined as
    xsd:string or rdf:langString -- the same value space as rdf:PlainLiteral.
    """
    graph = Graph()
    for s, p, o in data:
        if p == OWL.imports:
            continue
        graph.add((RDF.PlainLiteral if s == RDF.langString else s, p,
                   RDF.PlainLiteral if o == RDF.langString else o))
    graph.serialize(str(path), format='nt', encoding='utf-8')
