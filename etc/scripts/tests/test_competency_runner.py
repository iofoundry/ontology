import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from competency_runner import annotation_level, main

FIX = Path(__file__).parent / 'fixtures'


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.base = self.tmp / 'competency'
        shutil.copytree(FIX / 'competency', self.base)
        broken = self.base / 'release' / 'broken'
        broken.mkdir()
        shutil.copy(FIX / 'entail' / 'Inconsistent.ttl', broken / 'Example.ttl')

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_main(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(list(argv) + ['--base', str(self.base), '--catalog', str(self.base / 'catalog-v001.xml'),
                                      '--prod-about', str(self.base / 'AboutProd.ttl'),
                                      '--build-dir', str(self.tmp / 'build'), '--reasoner-memory', '1g'])
        return code, out.getvalue()

    def break_expectation(self, suite):
        (self.base / suite / 'tests' / 'Q.expected.csv').write_text('w\nex:w1\nex:w9\n')

    def test_annotation_levels(self):
        self.assertEqual(annotation_level('release', 'failure'), '::error')
        self.assertEqual(annotation_level('provisional', 'failure'), '::warning')
        self.assertEqual(annotation_level('provisional', 'broken'), '::error')
        self.assertEqual(annotation_level('release', 'warning'), '::warning')
        self.assertEqual(annotation_level('release', 'info'), '::notice')

    def test_good_suite_passes(self):
        code, out = self.run_main('release/good')
        self.assertEqual(code, 0, out)
        self.assertNotIn('::error', out)
        self.assertIn('::group::release/good', out)

    def test_release_failure_is_error(self):
        self.break_expectation('release/good')
        code, out = self.run_main('release/good')
        self.assertEqual(code, 1)
        self.assertIn('::error file=', out)
        self.assertIn('missing row: ex:w9', out)

    def test_provisional_failure_is_warning(self):
        shutil.copytree(self.base / 'release' / 'good', self.base / 'provisional' / 'good2')
        (self.base / 'provisional' / 'good2' / 'Example.ttl').write_text(
            (self.base / 'provisional' / 'good2' / 'Example.ttl').read_text().replace('/good/', '/good2/'))
        self.break_expectation('provisional/good2')
        code, out = self.run_main('provisional/good2')
        self.assertEqual(code, 0, out)
        self.assertIn('::warning file=', out)
        self.assertNotIn('::error', out)

    def test_leaky_release_is_tier_error(self):
        code, out = self.run_main('release/leaky')
        self.assertEqual(code, 1)
        self.assertIn('depends on provisional module https://example.org/DevOnly/', out)

    def test_unresolved_import_is_error_and_others_run(self):
        code, out = self.run_main('release/unresolved', 'release/good')
        self.assertEqual(code, 1)
        self.assertIn('https://example.org/nowhere/', out)
        self.assertIn('::group::release/good', out)
        self.assertIn('release/good passed', out)

    def test_inconsistent_suite_does_not_stop_others(self):
        code, out = self.run_main('release/broken', 'release/good')
        self.assertEqual(code, 1)
        self.assertIn('inconsistent', out)
        self.assertIn('release/good passed', out)

    def test_update_expected_writes_file(self):
        (self.base / 'release' / 'good' / 'tests' / 'Q.expected.csv').unlink()
        code, out = self.run_main('release/good', '--update-expected')
        self.assertEqual(code, 0, out)
        self.assertEqual((self.base / 'release' / 'good' / 'tests' / 'Q.expected.csv').read_text(),
                         'w\nex:w1\nex:w2\n')

    def test_parallel_jobs_same_result(self):
        code, out = self.run_main('release/good', 'release/broken', '--jobs', '2')
        self.assertEqual(code, 1)
        self.assertLess(out.index('::group::release/broken'), out.index('::group::release/good'))
        self.assertIn('release/good passed', out)

    def test_list_prints_suite_names_as_json(self):
        code, out = self.run_main('release', '--list')
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), ['release/broken', 'release/good', 'release/leaky',
                                           'release/unresolved'])

    def test_unknown_selector_is_error(self):
        code, out = self.run_main('release/nope')
        self.assertEqual(code, 1)
        self.assertIn('::error', out)


if __name__ == '__main__':
    unittest.main()
