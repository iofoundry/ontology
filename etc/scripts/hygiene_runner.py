"""Run the IOF hygiene tests: validate ontologies against the SHACL shapes in
etc/testing/hygiene_shapes, then classify them with HermiT, and report the results as
GitHub Actions annotations.

    python etc/scripts/hygiene_runner.py AboutIOFDev.rdf AboutIOFProd.rdf

Each About file is resolved through the catalog next to it into the set of ontology
files it imports; those are validated together with pySHACL (SHACL Core, SHACL-SPARQL
and the SHACL-AF rules that classify constructs). See the header of
etc/testing/hygiene_shapes/common.ttl for the conventions the shapes follow.

After all the SHACL tests, each About file's merged import closure is classified with
the HermiT reasoner bundled with owlready2 (needs Java on the PATH). An inconsistent
ontology, an unsatisfiable class, or a reasoner failure or timeout is an error.
"""
import argparse
import contextlib
import functools
import os
import re
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path


from pyshacl import validate
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SH
from rdflib.plugins.sparql import prepareQuery

from ontology_closure import CATALOG_NS, HERMIT_CLASSPATH, import_closure, merge, reasoner_input

IOF_H = Namespace('https://spec.industrialontologies.org/ontology/hygiene/')
IOF_AV = Namespace('https://spec.industrialontologies.org/ontology/annotation/')
INDIVIDUAL_PREFIX = 'https://spec.industrialontologies.org/ontology/individual/'


def parse_catalog(catalog_file_path: str) -> dict:
    """Map ontology IRIs to their .rdf files (relative to the catalog's folder)."""
    print('::notice file=' + catalog_file_path + ',title=Parse Catalog::Parsing file', catalog_file_path)
    catalog = ET.parse(catalog_file_path)
    return {uri.attrib['name']: uri.attrib['uri'] for uri in catalog.getroot().iter(CATALOG_NS + 'uri')
            if uri.attrib['uri'].endswith('.rdf')}


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

    absolute = {i: (Path(folder) / f).resolve() for i, f in resolution.items()}
    as_written = {path: resolution[i] for i, path in absolute.items()}
    closure = import_closure([iri], absolute)
    for file in closure.files:
        print('::notice file=' + as_written[file] + ',title=Find Imports::Getting imports from file:',
              as_written[file])
    for missing, _ in closure.missing:
        print('::warning file=' + missing + ',title=Find Imports::Could not find ontology for IRI:', missing)
    files = [str(f) for f in closure.files]
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


MANCHESTER_RESTRICTIONS = (
    (OWL.someValuesFrom, 'some'), (OWL.allValuesFrom, 'only'), (OWL.hasValue, 'value'),
    (OWL.minQualifiedCardinality, 'min'), (OWL.maxQualifiedCardinality, 'max'),
    (OWL.qualifiedCardinality, 'exactly'), (OWL.minCardinality, 'min'),
    (OWL.maxCardinality, 'max'), (OWL.cardinality, 'exactly'))


def manchester(data: Graph, node, nested: bool = False) -> str:
    """Render a class expression in Manchester syntax, naming entities by their label."""
    if not isinstance(node, BNode):
        if isinstance(node, Literal):
            return str(node)
        labels = list(data.objects(node, RDFS.label))
        label = next((l for l in labels if getattr(l, 'language', None) == 'en-US'), None) or \
            next(iter(labels), None)
        name = str(label) if label is not None else re.split(r'[/#]', str(node))[-1]
        return "'" + name + "'" if re.search(r'\W', name) else name

    def members(predicate):
        return [manchester(data, m, True) for m in data.items(data.value(node, predicate))]

    if data.value(node, OWL.intersectionOf) is not None:
        text = ' and '.join(members(OWL.intersectionOf))
    elif data.value(node, OWL.unionOf) is not None:
        text = ' or '.join(members(OWL.unionOf))
    elif data.value(node, OWL.oneOf) is not None:
        return '{' + ', '.join(members(OWL.oneOf)) + '}'
    elif data.value(node, OWL.complementOf) is not None:
        return 'not ' + manchester(data, data.value(node, OWL.complementOf), True)
    elif data.value(node, OWL.inverseOf) is not None:
        return 'inverse ' + manchester(data, data.value(node, OWL.inverseOf), True)
    elif data.value(node, OWL.onProperty) is not None:
        prop = manchester(data, data.value(node, OWL.onProperty), True)
        if data.value(node, OWL.hasSelf) is not None:
            text = prop + ' Self'
        else:
            text = prop + ' ?'
            for predicate, keyword in MANCHESTER_RESTRICTIONS:
                filler = data.value(node, predicate)
                if filler is not None:
                    text = prop + ' ' + keyword + ' ' + manchester(data, filler, True)
                    on_class = data.value(node, OWL.onClass)
                    if on_class is not None:
                        text += ' ' + manchester(data, on_class, True)
                    break
    else:
        return '_:' + str(node)
    return '(' + text + ')' if nested else text


def format_message(template: str, focus, value, path, data: Graph) -> str:
    """Fill the {$this}/{?value}/{?path} placeholders pySHACL leaves in messages; an
    anonymous class expression value is written out in Manchester syntax (in place of the
    blank node id pySHACL itself substitutes into SPARQL constraint messages)."""
    if isinstance(value, BNode):
        expression = manchester(data, value)
        template = template.replace('{?value}', expression).replace(str(value), expression)
    for placeholder, term in (('{$this}', focus), ('{?value}', value), ('{?path}', path)):
        if term is not None:
            template = template.replace(placeholder, str(term))
    return template


def load_suppressions(path: str) -> dict:
    """{(focus node, rule): justification} from the suppressions file, if there is one."""
    suppressions = {}
    if not path or not os.path.exists(path):
        return suppressions
    graph = Graph().parse(path, format='turtle')
    for entry in graph.subjects(RDF.type, IOF_H.Suppression):
        focus, rule = graph.value(entry, IOF_H.focusNode), graph.value(entry, IOF_H.rule)
        justification = graph.value(entry, RDFS.comment)
        if focus is None or rule is None or justification is None:
            print('::warning file=' + path + ',title=Suppressions::Ignoring a suppression without '
                  'iof-h:focusNode, iof-h:rule and an rdfs:comment justification.')
            continue
        suppressions[(focus, rule)] = str(justification)
    return suppressions


def result_rules(results: Graph, shapes: Graph, result) -> set:
    """Everything a suppression may name for a result: the constraint, its shape, and the
    node shape a property shape belongs to."""
    rules = {results.value(result, SH.sourceConstraint), results.value(result, SH.sourceShape)}
    rules |= set(shapes.subjects(SH.property, results.value(result, SH.sourceShape)))
    return rules - {None}


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


def load_data(files: list) -> Graph:
    return merge(files)


def run_hygiene(data: Graph, shapes: Graph, maturity: str, resolution: dict, focus_filter: str,
                suppressions: dict) -> bool:
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
            results.value(result, SH.value), results.value(result, SH.resultPath), data)
        level = annotation_level(results.value(result, SH.resultSeverity), maturity)
        justification = next((suppressions[(focus, rule)] for rule in result_rules(results, shapes, result)
                              if (focus, rule) in suppressions), None)
        if justification is not None:
            level, message = '::notice', 'Suppressed (' + justification + '): ' + message
        file = source_file(data, focus, resolution)
        location = 'file=' + file + ',' if file else ''
        annotations.add(level + ' ' + location + 'title=' + title + '::' + message)

    for annotation in sorted(annotations):
        print(annotation)
    return not any(a.startswith('::error') for a in annotations)


def run_reasoner(data: Graph, about_file: str, resolution: dict, timeout: float, memory: str) -> bool:
    """Classify with HermiT within ``timeout`` seconds; report inconsistency,
    unsatisfiable classes and failures."""
    with tempfile.TemporaryDirectory() as folder:
        path = os.path.join(folder, 'closure.nt')
        reasoner_input(data, path)
        command = ['java', '-Xmx' + memory, '-cp', HERMIT_CLASSPATH,
                   'org.semanticweb.HermiT.cli.CommandLine', '--unsatisfiable', 'file://' + path]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            print('::error title=Reasoner::HermiT did not finish classifying ' + about_file +
                  ' within the ' + str(round(timeout)) + ' seconds left of the reasoner time limit.')
            return False
        except FileNotFoundError:
            print('::error title=Reasoner::java was not found on the PATH; HermiT needs Java.')
            return False

    if 'InconsistentOntologyException' in result.stderr:
        print('::error title=Reasoner::' + about_file + ' is inconsistent: its ontologies have no model.')
        return False
    if result.returncode != 0:
        detail = next((line for line in result.stderr.splitlines() if 'Exception' in line), 'see log')
        print(result.stderr, file=sys.stderr)
        print('::error title=Reasoner::HermiT failed on ' + about_file + ': ' + detail)
        return False

    # --unsatisfiable prints "Classes equivalent to 'owl:Nothing':" then one class per line.
    unsatisfiable = sorted(m.group(1) for m in re.finditer(r'^\s*<([^>]+)>\s*$', result.stdout, re.M))
    for iri in unsatisfiable:
        file = source_file(data, URIRef(iri), resolution)
        location = 'file=' + file + ',' if file else ''
        print('::error ' + location + 'title=Reasoner::Class ' + iri + ' is unsatisfiable (equivalent to owl:Nothing).')
    if not unsatisfiable:
        print('::notice title=Reasoner::' + about_file + ' is consistent and has no unsatisfiable classes.')
    return not unsatisfiable


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the IOF hygiene tests (SHACL)')
    parser.add_argument('about_files', nargs='+', metavar='ABOUT', help='About*.rdf files to test')
    parser.add_argument('--shapes', default='etc/testing/hygiene_shapes',
                        help='Folder of SHACL shape files (*.ttl)')
    parser.add_argument('--focus-filter', default='industrialontologies',
                        help='Only report results whose focus node IRI matches this regex')
    parser.add_argument('--suppressions', default='etc/testing/hygiene_suppressions.ttl',
                        help='Turtle file of accepted findings (iof-h:Suppression), reported as notices')
    parser.add_argument('--no-reasoner', action='store_true', help='Skip the HermiT classification')
    parser.add_argument('--reasoner-timeout', type=int, default=3600, metavar='SECONDS',
                        help='Time limit for classifying all the About files combined (default 3600)')
    parser.add_argument('--reasoner-memory', default='4g', metavar='SIZE',
                        help='Java heap for HermiT, e.g. 4g (default 4g)')
    args = parser.parse_args()

    shapes = load_shapes(args.shapes)
    suppressions = load_suppressions(args.suppressions)
    ontology_is_clean = True
    closures = []
    for about_file in args.about_files:
        print('========================================')
        print('::group::Running tests:', about_file)
        files, maturity, resolution = find_ontologies(about_file)
        print('::notice title=' + about_file + ' Maturity::' + about_file + ' has maturity:', maturity)
        data = load_data(files)
        closures.append((about_file, data, resolution))
        clean = run_hygiene(data, shapes, maturity, resolution, args.focus_filter, suppressions)
        ontology_is_clean = ontology_is_clean and clean
        print('::endgroup::')
        if clean:
            print('::notice title=' + about_file + '::Hygiene tests passed for about file:', about_file)
        else:
            print('::error title=' + about_file + '::Hygiene tests failed for about file:', about_file)

    if not args.no_reasoner:
        deadline = time.monotonic() + args.reasoner_timeout
        for about_file, data, resolution in closures:
            print('========================================')
            print('::group::Reasoning:', about_file)
            remaining = deadline - time.monotonic()
            if remaining > 0:
                consistent = run_reasoner(data, about_file, resolution, remaining, args.reasoner_memory)
            else:
                print('::error title=Reasoner::Not classified: the ' + str(args.reasoner_timeout) +
                      ' second reasoner time limit was used up before ' + about_file + '.')
                consistent = False
            ontology_is_clean = ontology_is_clean and consistent
            print('::endgroup::')
            if not consistent:
                print('::error title=' + about_file + '::Reasoner found errors for about file:', about_file)

    if not ontology_is_clean:
        print('::error title=Hygiene Tests::some hygiene tests failed.')
        sys.exit(1)
    print('::notice title=Hygiene Tests::all hygiene tests passed.')
    sys.exit(0)
