import tempfile
import unittest
from pathlib import Path

from rdflib import Graph
from rdflib.namespace import OWL, RDF

from ontology_closure import (ClosureError, import_closure, load_catalog, merge, ontology_iri,
                              reasoner_input)

FIX = Path(__file__).parent / 'fixtures' / 'closure'
A_IRI, C_IRI = 'https://example.org/A/', 'https://example.org/C/'


class OntologyClosureTest(unittest.TestCase):
    def test_load_catalog_absolute_paths(self):
        res = load_catalog(FIX / 'catalog-v001.xml')
        self.assertEqual(res[C_IRI], FIX.resolve() / 'C.rdf')

    def test_closure_follows_imports(self):
        c = import_closure([A_IRI], load_catalog(FIX / 'catalog-v001.xml'))
        self.assertEqual({p.name for p in c.files}, {'A.ttl', 'B.ttl', 'C.rdf'})
        self.assertEqual(c.iris, {A_IRI, 'https://example.org/B/', C_IRI})
        self.assertEqual(c.missing, [])

    def test_missing_import_reported_with_importer(self):
        res = load_catalog(FIX / 'catalog-v001.xml')
        del res[C_IRI]
        c = import_closure([A_IRI], res)
        self.assertEqual(c.missing, [(C_IRI, FIX.resolve() / 'B.ttl')])

    def test_ontology_iri_requires_exactly_one(self):
        self.assertEqual(ontology_iri(FIX / 'A.ttl'), A_IRI)
        with self.assertRaises(ClosureError):
            ontology_iri(FIX / 'NoHeader.ttl')

    def test_reasoner_input_strips_imports_and_langstring(self):
        g = merge([FIX / 'A.ttl', FIX / 'Lang.ttl'])
        self.assertTrue(list(g.triples((None, OWL.imports, None))))
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'x.nt'
            reasoner_input(g, out)
            r = Graph().parse(out)
        self.assertFalse(list(r.triples((None, OWL.imports, None))))
        self.assertFalse(list(r.triples((None, None, RDF.langString))))
        self.assertTrue(list(r.triples((None, None, RDF.PlainLiteral))))


if __name__ == '__main__':
    unittest.main()
