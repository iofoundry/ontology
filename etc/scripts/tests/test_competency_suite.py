import unittest
from pathlib import Path

from competency_suite import SuiteError, discover_suites, resolve_suite, tier_violations

FIX = Path(__file__).parent / 'fixtures' / 'competency'
CATALOG = FIX / 'catalog-v001.xml'
PROD = FIX / 'AboutProd.ttl'
DEVONLY_IRI = 'https://example.org/DevOnly/'


def one(name):
    return discover_suites(FIX, [name])[0]


class SuiteDiscoveryTest(unittest.TestCase):
    def test_discover_all_and_selectors(self):
        self.assertEqual([s.name for s in discover_suites(FIX, [])],
                         ['provisional/dev', 'release/good', 'release/leaky', 'release/unresolved'])
        self.assertEqual(len(discover_suites(FIX, ['release'])), 3)
        good = discover_suites(FIX, ['release/good'])
        self.assertEqual(len(good), 1)
        self.assertEqual(good[0].tier, 'release')
        self.assertEqual([p.name for p in good[0].ontology_files], ['Example.ttl'])
        self.assertEqual([p.name for p in good[0].shapes_tests], ['Types.shapes.ttl'])
        self.assertEqual([p.name for p in good[0].sparql_tests], ['Q.rq'])
        with self.assertRaises(SuiteError):
            discover_suites(FIX, ['nope'])

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
