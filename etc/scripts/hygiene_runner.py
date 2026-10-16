"""Run the IOF hygiene tests: validate ontologies against the SHACL shapes in
etc/testing/hygiene_shapes and report the results as GitHub Actions annotations.

    python etc/scripts/hygiene_runner.py AboutIOFDev.rdf AboutIOFProd.rdf

Each About file is resolved through the catalog next to it into the set of ontology
files it imports; those are validated together with pySHACL (SHACL Core, SHACL-SPARQL
and the SHACL-AF rules that classify constructs). See the header of
etc/testing/hygiene_shapes/common.ttl for the conventions the shapes follow.
"""
import argparse
import contextlib
import functools
import os
import re
import sys
import xml.etree.ElementTree as ET

from pyshacl import validate
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import OWL, RDF, RDFS, SH
from rdflib.plugins.sparql import prepareQuery

IOF_H = Namespace('https://spec.industrialontologies.org/ontology/hygiene/')
IOF_AV = Namespace('https://spec.industrialontologies.org/ontology/annotation/')
INDIVIDUAL_PREFIX = 'https://spec.industrialontologies.org/ontology/individual/'


def parse_catalog(catalog_file_path: str) -> dict:
    """Map ontology IRIs to their .rdf files (relative to the catalog's folder)."""
    resolution = dict()
    print('::notice file=' + catalog_file_path + ',title=Parse Catalog::Parsing file', catalog_file_path)
    catalog = ET.parse(catalog_file_path)
    for uri in catalog.getroot().findall('{urn:oasis:names:tc:entity:xmlns:xml:catalog}uri'):
        ontology_path = uri.attrib['uri']
        if ontology_path.endswith('.rdf'):
            resolution[uri.attrib['name']] = ontology_path
    return resolution


def find_imports(iri: str, resolution: dict, found_iris: set):
    if iri in found_iris:
        return
    found_iris.add(iri)
    if iri not in resolution:
        print('::warning file=' + iri + ',title=Find Imports::Could not find ontology for IRI:', iri)
        return
    print('::notice file=' + resolution[iri] + ',title=Find Imports::Getting imports from file:', resolution[iri])
    graph = Graph()
    graph.parse(source=resolution[iri])
    for ontology in graph.subjects(RDF.type, OWL.Ontology):
        for imported in graph.objects(ontology, OWL.imports):
            find_imports(str(imported), resolution, found_iris)


def find_ontologies(about_file: str):
    """Return (ontology files, maturity, catalog resolution) for an About file."""
    about_path = os.path.abspath(about_file)
    folder = os.path.dirname(about_path)
    resolution = parse_catalog(os.path.join(folder, 'catalog-v001.xml'))

    print('::notice file=' + about_file + ',title=Parse About::Parsing file', about_file)
    graph = Graph()
    graph.parse(source=about_path)
    about = next(((o, m) for o in graph.subjects(RDF.type, OWL.Ontology)
                  for m in graph.objects(o, IOF_AV.maturity)), None)
    if about is None:
        print('::error file=' + about_file + ',title=Parse About::Could not find maturity level in about file.')
        sys.exit(1)
    iri, maturity = str(about[0]), str(about[1]).replace(INDIVIDUAL_PREFIX, '')
    print('::notice file=' + about_file + ',title=Parse About::Maturity level: ' + maturity)

    found_iris = set()
    find_imports(iri, resolution, found_iris)
    files = [os.path.join(folder, resolution[i]) for i in found_iris if i in resolution]
    return files, maturity, resolution


def load_shapes(shapes_folder: str) -> Graph:
    shapes = Graph()
    for file_name in sorted(os.listdir(shapes_folder)):
        if file_name.endswith('.ttl'):
            shapes.parse(os.path.join(shapes_folder, file_name), format='turtle')
    return shapes


@contextlib.contextmanager
def cached_sparql_parsing():
    """pySHACL re-parses a SPARQL constraint for every focus node, and parsing costs far
    more than evaluating these small queries; reuse the parsed query instead."""
    original_query = Graph.query
    prepare = functools.lru_cache(maxsize=None)(prepareQuery)

    def query(self, query_object, *args, **kwargs):
        if isinstance(query_object, str):
            query_object = prepare(query_object)
        return original_query(self, query_object, *args, **kwargs)

    Graph.query = query
    try:
        yield
    finally:
        Graph.query = original_query


def format_message(template: str, focus, value, path) -> str:
    """Fill the {$this}/{?value}/{?path} placeholders pySHACL leaves in Core messages."""
    for placeholder, term in (('{$this}', focus), ('{?value}', value), ('{?path}', path)):
        if term is not None:
            template = template.replace(placeholder, str(term))
    return template


def source_file(data: Graph, focus, resolution: dict):
    """The ontology file that defines the focus node, for the annotation's file= field."""
    if (focus, RDF.type, OWL.Ontology) in data:
        iri = str(focus)
    else:
        iri = next((str(o) for o in data.objects(focus, RDFS.isDefinedBy)), None)
    return resolution.get(iri) if iri else None


def annotation_level(severity, maturity: str) -> str:
    if severity == IOF_H.Critical:
        return '::error'
    if severity == SH.Violation:
        return '::warning' if maturity == 'Provisional' else '::error'
    if severity == SH.Warning:
        return '::warning'
    return '::notice'


def run_hygiene(files: list, shapes: Graph, maturity: str, resolution: dict, focus_filter: str) -> bool:
    data = Graph()
    for file in files:
        data.parse(source=file)
    with cached_sparql_parsing():
        _, results, _ = validate(
            data, shacl_graph=shapes, advanced=True, inference='none', allow_warnings=True)

    in_scope = re.compile(focus_filter)
    annotations = set()
    for result in results.subjects(RDF.type, SH.ValidationResult):
        focus = results.value(result, SH.focusNode)
        if not isinstance(focus, Literal) and not in_scope.search(str(focus)):
            continue
        # A SPARQL constraint may carry its own label; otherwise use the shape's.
        source = results.value(result, SH.sourceConstraint)
        if source is None or shapes.value(source, RDFS.label) is None:
            source = results.value(result, SH.sourceShape)
        title = str(shapes.value(source, RDFS.label) or source)
        message = format_message(
            str(results.value(result, SH.resultMessage)), focus,
            results.value(result, SH.value), results.value(result, SH.resultPath))
        level = annotation_level(results.value(result, SH.resultSeverity), maturity)
        file = source_file(data, focus, resolution)
        location = 'file=' + file + ',' if file else ''
        annotations.add(level + ' ' + location + 'title=' + title + '::' + message)

    for annotation in sorted(annotations):
        print(annotation)
    return not any(a.startswith('::error') for a in annotations)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the IOF hygiene tests (SHACL)')
    parser.add_argument('about_files', nargs='+', metavar='ABOUT', help='About*.rdf files to test')
    parser.add_argument('--shapes', default='etc/testing/hygiene_shapes',
                        help='Folder of SHACL shape files (*.ttl)')
    parser.add_argument('--focus-filter', default='industrialontologies',
                        help='Only report results whose focus node IRI matches this regex')
    args = parser.parse_args()

    shapes = load_shapes(args.shapes)
    ontology_is_clean = True
    for about_file in args.about_files:
        print('========================================')
        print('::group::Running tests:', about_file)
        files, maturity, resolution = find_ontologies(about_file)
        print('::notice title=' + about_file + ' Maturity::' + about_file + ' has maturity:', maturity)
        clean = run_hygiene(files, shapes, maturity, resolution, args.focus_filter)
        ontology_is_clean = ontology_is_clean and clean
        print('::endgroup::')
        if clean:
            print('::notice title=' + about_file + '::Hygiene tests passed for about file:', about_file)
        else:
            print('::error title=' + about_file + '::Hygiene tests failed for about file:', about_file)

    if not ontology_is_clean:
        print('::error title=Hygiene Tests::some hygiene tests failed.')
        sys.exit(1)
    print('::notice title=Hygiene Tests::all hygiene tests passed.')
    sys.exit(0)
