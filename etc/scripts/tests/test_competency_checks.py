import shutil
import tempfile
import unittest
from pathlib import Path

from rdflib import Dataset, Literal, Namespace
from rdflib.namespace import RDF

from competency_checks import (check_sparql, compare_rows, read_expected, render_term, run_shacl,
                               run_sparql, write_expected)
from competency_entail import ASSERTED, CLOSURE, INFERRED

EX = Namespace('https://example.org/ex/')
PREFIX = 'PREFIX ex: <https://example.org/ex/>\n'


def dataset():
    ds = Dataset(default_union=True)
    ds.graph(ASSERTED).add((EX.w1, RDF.type, EX.Widget))
    ds.graph(ASSERTED).add((EX.w1, EX.p, EX.w2))
    ds.graph(ASSERTED).add((EX.w1, EX.label, Literal('one', lang='en')))
    ds.graph(CLOSURE).add((EX.w1, RDF.type, EX.Thing))
    ds.graph(INFERRED).add((EX.w2, RDF.type, EX.Widget))
    return ds


class ChecksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, name, text):
        path = self.tmp / name
        path.write_text(text)
        return path

    SHAPES = ('@prefix sh: <http://www.w3.org/ns/shacl#> . @prefix ex: <https://example.org/ex/> .\n'
              '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')

    def test_shacl_sees_union(self):
        shapes = self.write('s.shapes.ttl', self.SHAPES +
                            'ex:S a sh:NodeShape ; sh:targetClass ex:Thing ; '
                            'sh:property [ sh:path ex:p ; sh:minCount 1 ] .')
        self.assertEqual(run_shacl(shapes, dataset()), [])

    def test_shacl_violation_is_failure(self):
        shapes = self.write('s.shapes.ttl', self.SHAPES +
                            'ex:S a sh:NodeShape ; rdfs:label "w1 is a gadget" ; '
                            'sh:targetNode ex:w1 ; sh:class ex:Gadget .')
        findings = run_shacl(shapes, dataset())
        self.assertEqual([f.kind for f in findings], ['failure'])
        self.assertEqual(findings[0].title, 'w1 is a gadget')
        self.assertIn('w1', findings[0].message)

    def test_shacl_warning_severity(self):
        shapes = self.write('s.shapes.ttl', self.SHAPES +
                            'ex:S a sh:NodeShape ; sh:severity sh:Warning ; '
                            'sh:targetNode ex:w1 ; sh:class ex:Gadget .')
        self.assertEqual([f.kind for f in run_shacl(shapes, dataset())], ['warning'])

    def test_broken_shapes_file(self):
        shapes = self.write('s.shapes.ttl', 'this is not turtle')
        self.assertEqual([f.kind for f in run_shacl(shapes, dataset())], ['broken'])

    def test_render_compacts_with_query_prefixes(self):
        prefixes = {'ex': str(EX)}
        self.assertEqual(render_term(EX.w1, prefixes), 'ex:w1')
        self.assertEqual(render_term(EX['a/b'], prefixes), 'https://example.org/ex/a/b')
        self.assertEqual(render_term(Literal('one', lang='en'), prefixes), 'one')
        self.assertEqual(render_term(None, prefixes), '')

    def test_unbound_is_empty_cell(self):
        q = self.write('q.rq', PREFIX + 'SELECT ?w ?o WHERE { ?w a ex:Widget OPTIONAL { ?w ex:p ?o } }')
        header, rows = run_sparql(q, dataset())
        self.assertEqual(header, ['w', 'o'])
        self.assertEqual(sorted(rows), [('ex:w1', 'ex:w2'), ('ex:w2', '')])

    def test_graph_names_visible(self):
        q = self.write('q.rq', PREFIX + 'SELECT ?g WHERE { GRAPH ?g { ex:w2 a ex:Widget } }')
        self.assertEqual(run_sparql(q, dataset())[1], [('urn:inferred',)])

    def test_ask_true(self):
        q = self.write('q.rq', PREFIX + 'ASK { ex:w1 a ex:Thing }')
        self.assertEqual(run_sparql(q, dataset()), (['ask'], [('true',)]))

    def test_duplicate_rows_count(self):
        missing, unexpected = compare_rows([('a',), ('a',)], [('a',)])
        self.assertEqual((missing, unexpected), ([('a',)], []))

    def test_missing_expected_is_broken(self):
        q = self.write('q.rq', PREFIX + 'SELECT ?w WHERE { ?w a ex:Widget }')
        self.assertEqual([f.kind for f in check_sparql(q, dataset(), update=False)], ['broken'])

    def test_update_writes_sorted_csv(self):
        q = self.write('q.rq', PREFIX + 'SELECT ?w WHERE { ?w a ex:Widget } ORDER BY DESC(?w)')
        self.assertEqual(check_sparql(q, dataset(), update=True), [])
        self.assertEqual((self.tmp / 'q.expected.csv').read_text().splitlines(), ['w', 'ex:w1', 'ex:w2'])
        self.assertEqual(check_sparql(q, dataset(), update=False), [])

    def test_mismatch_reports_rows(self):
        q = self.write('q.rq', PREFIX + 'SELECT ?w WHERE { ?w a ex:Widget }')
        write_expected(self.tmp / 'q.expected.csv', ['w'], [('ex:w1',), ('ex:w9',)])
        messages = sorted(f.message for f in check_sparql(q, dataset(), update=False))
        self.assertEqual(messages, ['missing row: ex:w9', 'unexpected row: ex:w2'])
        self.assertEqual(read_expected(self.tmp / 'q.expected.csv'), (['w'], [('ex:w1',), ('ex:w9',)]))

    def test_header_mismatch_is_failure(self):
        q = self.write('q.rq', PREFIX + 'SELECT ?w WHERE { ?w a ex:Widget }')
        write_expected(self.tmp / 'q.expected.csv', ['x'], [('ex:w1',), ('ex:w2',)])
        findings = check_sparql(q, dataset(), update=False)
        self.assertEqual([f.kind for f in findings], ['failure'])
        self.assertIn('columns', findings[0].message)

    def test_column_order_ignored(self):
        # SELECT * column order is not stable between processes in rdflib.
        q = self.write('q.rq', PREFIX + 'SELECT ?w ?o WHERE { ?w a ex:Widget OPTIONAL { ?w ex:p ?o } }')
        write_expected(self.tmp / 'q.expected.csv', ['o', 'w'], [('ex:w2', 'ex:w1'), ('', 'ex:w2')])
        self.assertEqual(check_sparql(q, dataset(), update=False), [])

    def test_invalid_shapes_constraint_is_broken(self):
        shapes = self.write('s.shapes.ttl', self.SHAPES +
                            'ex:S a sh:NodeShape ; sh:targetNode ex:w1 ; '
                            'sh:property [ sh:path ex:p ; sh:minCount "x" ] .')
        self.assertEqual([f.kind for f in run_shacl(shapes, dataset())], ['broken'])

    def test_construct_query_is_broken(self):
        q = self.write('q.rq', PREFIX + 'CONSTRUCT { ?w a ex:Thing } WHERE { ?w a ex:Widget }')
        findings = check_sparql(q, dataset(), update=False)
        self.assertEqual([f.kind for f in findings], ['broken'])
        self.assertIn('SELECT or ASK', findings[0].message)

    def test_trailing_blank_line_in_expected_ignored(self):
        q = self.write('q.rq', PREFIX + 'SELECT ?w WHERE { ?w a ex:Widget }')
        (self.tmp / 'q.expected.csv').write_text('w\nex:w1\nex:w2\n\n')
        self.assertEqual(check_sparql(q, dataset(), update=False), [])

    def test_bad_query_is_broken(self):
        q = self.write('q.rq', 'SELEKT nonsense')
        self.assertEqual([f.kind for f in check_sparql(q, dataset(), update=False)], ['broken'])


if __name__ == '__main__':
    unittest.main()
