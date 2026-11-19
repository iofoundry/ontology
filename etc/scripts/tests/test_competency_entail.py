import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from rdflib import Namespace
from rdflib.namespace import RDF

from competency_entail import ASSERTED, CLOSURE, INFERRED, cache_key, entail

FIX = Path(__file__).parent / 'fixtures' / 'entail'
D = Namespace('https://example.org/d/')


class EntailTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_entail(self, files, **kw):
        return entail(files, self.tmp / 'cache', timeout=kw.pop('timeout', 120), memory='1g', **kw)

    def test_defined_class_inferred(self):
        r = self.run_entail([FIX / 'Defined.ttl'])
        self.assertIsNone(r.failure)
        ds = r.dataset
        self.assertIn((D.x, RDF.type, D.A), ds.graph(INFERRED))
        self.assertNotIn((D.x, RDF.type, D.A), ds.graph(ASSERTED))
        self.assertIn((D.x, RDF.type, D.B), ds.graph(ASSERTED))
        self.assertIn((D.x, RDF.type, D.Top), ds.graph(CLOSURE))
        self.assertEqual(r.unsatisfiable, [])
        self.assertFalse(r.cached)

    def test_inconsistent_reports_failure(self):
        r = self.run_entail([FIX / 'Inconsistent.ttl'])
        self.assertEqual(r.failure, 'inconsistent')
        self.assertIsNone(r.dataset)
        again = self.run_entail([FIX / 'Inconsistent.ttl'])
        self.assertFalse(again.cached)   # failures are never cached

    def test_cache_hit_skips_reasoner(self):
        self.run_entail([FIX / 'Defined.ttl'])
        r = self.run_entail([FIX / 'Defined.ttl'])
        self.assertTrue(r.cached)
        self.assertLess(r.seconds, 2)
        self.assertIn((D.x, RDF.type, D.A), r.dataset.graph(INFERRED))

    def test_no_cache_forces_reasoner(self):
        self.run_entail([FIX / 'Defined.ttl'])
        self.assertFalse(self.run_entail([FIX / 'Defined.ttl'], use_cache=False).cached)

    def test_cache_key_changes_with_input(self):
        copy = self.tmp / 'Defined.ttl'
        shutil.copy(FIX / 'Defined.ttl', copy)
        before = cache_key([copy], True)
        with open(copy, 'a') as f:
            f.write('\n:z a :B .\n')
        self.assertNotEqual(cache_key([copy], True), before)
        self.assertNotEqual(cache_key([copy], False), cache_key([copy], True))

    def test_cache_key_ignores_other_files(self):
        copy = self.tmp / 'Defined.ttl'
        shutil.copy(FIX / 'Defined.ttl', copy)
        before = cache_key([copy], True)
        (self.tmp / 'unrelated.rq').write_text('SELECT * {}')
        self.assertEqual(cache_key([copy], True), before)

    def test_cache_key_changes_with_runner_code(self):
        import competency_entail
        code = self.tmp / 'code.py'
        code.write_text('a = 1\n')
        saved = competency_entail.CODE_FILES
        competency_entail.CODE_FILES = [code]
        try:
            before = cache_key([FIX / 'Defined.ttl'], True)
            code.write_text('a = 2\n')
            self.assertNotEqual(cache_key([FIX / 'Defined.ttl'], True), before)
        finally:
            competency_entail.CODE_FILES = saved

    def test_timeout_kills_worker(self):
        r = self.run_entail([FIX / 'Defined.ttl'], timeout=0.05)
        self.assertEqual(r.failure, 'timeout')
        self.assertIsNone(r.dataset)
        left = subprocess.run(['pgrep', '-f', str(self.tmp / 'cache')], capture_output=True)
        self.assertEqual(left.returncode, 1, left.stdout)


if __name__ == '__main__':
    unittest.main()
