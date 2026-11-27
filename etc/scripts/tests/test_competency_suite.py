import shutil
import tempfile
import unittest
from pathlib import Path

from competency_suite import (SuiteError, QuestionError, discover_suites, read_expect_inconsistent,
                              read_metadata, resolve_suite, tier_violations)

FIX = Path(__file__).parent / 'fixtures' / 'competency'
CATALOG = FIX / 'catalog-v001.xml'
PROD = FIX / 'AboutProd.ttl'
DEVONLY_IRI = 'https://example.org/DevOnly/'


def one(name):
    return discover_suites(FIX, [name])[0]


class MetadataTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def meta(self, text, name='T.rq'):
        path = self.tmp / name
        path.write_text(text)
        return read_metadata(path)

    def test_header_keys(self):
        self.assertEqual(self.meta('# description: Finds widgets.\n# reasoning: true\nSELECT * {}\n'),
                         ('Finds widgets.', True))
        self.assertEqual(self.meta('#Description:  x \n#   REASONING : No\nASK {}\n'), ('x', False))

    def test_header_may_follow_prefixes_and_free_comments(self):
        text = ('@prefix sh: <http://www.w3.org/ns/shacl#> .\n\n# A note about the shapes.\n'
                '# description: Shapes.\n# reasoning: false\n<a> <b> <c> .\n')
        self.assertEqual(self.meta(text, 'S.shapes.ttl'), ('Shapes.', False))

    def test_keys_after_the_header_are_ignored(self):
        with self.assertRaises(QuestionError) as ctx:
            self.meta('# description: x\nSELECT * {}\n# reasoning: true\n')
        self.assertIn('reasoning', str(ctx.exception))

    def test_missing_description(self):
        with self.assertRaises(QuestionError) as ctx:
            self.meta('# reasoning: true\nSELECT * {}\n')
        self.assertIn('description', str(ctx.exception))

    def test_expect_header(self):
        path = self.tmp / 'T.rq'
        path.write_text('# description: x\n# reasoning: true\n# expect: Inconsistent\nASK {}\n')
        self.assertTrue(read_expect_inconsistent(path, True))
        path.write_text('# description: x\n# reasoning: true\nASK {}\n')
        self.assertFalse(read_expect_inconsistent(path, True))
        path.write_text('# description: x\n# reasoning: true\n# expect: broken\nASK {}\n')
        with self.assertRaises(QuestionError):
            read_expect_inconsistent(path, True)
        path.write_text('# description: x\n# reasoning: false\n# expect: inconsistent\nASK {}\n')
        with self.assertRaises(QuestionError) as ctx:
            read_expect_inconsistent(path, False)
        self.assertIn('reasoning: true', str(ctx.exception))

    def test_bad_reasoning_value(self):
        with self.assertRaises(QuestionError) as ctx:
            self.meta('# description: x\n# reasoning: maybe\nSELECT * {}\n')
        self.assertIn('maybe', str(ctx.exception))


class SuiteDiscoveryTest(unittest.TestCase):
    def test_discover_all_and_selectors(self):
        self.assertEqual([s.name for s in discover_suites(FIX, [])],
                         ['provisional/dev', 'release/good', 'release/leaky', 'release/unresolved'])
        self.assertEqual(len(discover_suites(FIX, ['release'])), 3)
        good = discover_suites(FIX, ['release/good'])
        self.assertEqual(len(good), 1)
        self.assertEqual(good[0].tier, 'release')
        self.assertEqual([p.name for p in good[0].ontology_files], ['Example.ttl'])
        self.assertEqual([s.name for s in good[0].sets], ['basic'])
        tests = good[0].sets[0].tests
        self.assertEqual([(t.path.name, t.kind) for t in tests],
                         [('Asserted.rq', 'sparql'), ('Q.rq', 'sparql'), ('Types.shapes.ttl', 'shacl')])
        self.assertEqual(tests[0].description, 'Without reasoning, w1 is not yet a Thing.')
        self.assertEqual([t.reasoning for t in tests], [False, True, True])
        self.assertEqual(good[0].needs_reasoning, True)
        with self.assertRaises(SuiteError):
            discover_suites(FIX, ['nope'])

    def test_set_selector(self):
        suites = discover_suites(FIX, ['release/good/basic'])
        self.assertEqual([(s.name, [q.name for q in s.sets]) for s in suites], [('release/good', ['basic'])])
        with self.assertRaises(SuiteError):
            discover_suites(FIX, ['release/good/nope'])

    def test_missing_base_has_no_suites(self):
        self.assertEqual(discover_suites(FIX / 'nope', []), [])

    def test_broken_metadata_is_kept_on_the_test(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            shutil.copytree(FIX, tmp / 'c')
            (tmp / 'c/release/good/basic/Q.rq').write_text('SELECT * {}\n')
            tests = discover_suites(tmp / 'c', ['release/good'])[0].sets[0].tests
            q = next(t for t in tests if t.path.name == 'Q.rq')
            self.assertIn('description', q.error)
            self.assertIsNone(q.reasoning)
        finally:
            shutil.rmtree(tmp)

    def test_test_files_outside_a_set_are_an_error(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            shutil.copytree(FIX, tmp / 'c')
            (tmp / 'c/release/good/Stray.rq').write_text('SELECT * {}\n')
            with self.assertRaises(SuiteError) as ctx:
                discover_suites(tmp / 'c', ['release/good'])
            self.assertIn('Stray.rq', str(ctx.exception))
        finally:
            shutil.rmtree(tmp)

    def test_resolve_good_suite(self):
        closure = resolve_suite(one('release/good'), CATALOG)
        self.assertEqual(sorted(p.name for p in closure.files), ['Core.ttl', 'Example.ttl'])

    def test_unresolved_import_is_error(self):
        with self.assertRaises(SuiteError) as ctx:
            resolve_suite(one('release/unresolved'), CATALOG)
        self.assertIn('https://example.org/nowhere/', str(ctx.exception))
        self.assertIn('Example.ttl', str(ctx.exception))

    def test_release_leak_is_violation(self):
        suite = one('release/leaky')
        closure = resolve_suite(suite, CATALOG)
        self.assertEqual(tier_violations(suite, closure, PROD, CATALOG), [DEVONLY_IRI])

    def test_release_good_has_no_violations(self):
        suite = one('release/good')
        self.assertEqual(tier_violations(suite, resolve_suite(suite, CATALOG), PROD, CATALOG), [])

    def test_provisional_has_no_violations(self):
        suite = one('provisional/dev')
        self.assertEqual(tier_violations(suite, resolve_suite(suite, CATALOG), PROD, CATALOG), [])


if __name__ == '__main__':
    unittest.main()
