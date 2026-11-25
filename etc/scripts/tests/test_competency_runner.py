import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from competency_runner import annotation_level, main

FIX = Path(__file__).parent / 'fixtures'
ASK_ASSERTED = ('# description: {d}\n# reasoning: false\n'
                'PREFIX i: <https://example.org/i/>\nASK {{ i:z a i:D }}\n')
ASK_REASONED = ('# description: {d}\n# reasoning: true\n'
                'PREFIX i: <https://example.org/i/>\nASK {{ i:z a i:D }}\n')


class RunnerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.base = self.tmp / 'competency'
        shutil.copytree(FIX / 'competency', self.base)
        # release/broken: inconsistent data, one question that needs HermiT and one that does not
        self.add_suite('release/broken', {'q/NeedsReasoner.rq': ASK_REASONED.format(d='needs HermiT'),
                                          'q/Plain.rq': ASK_ASSERTED.format(d='asserted z is a D')})

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def add_suite(self, name, questions):
        root = self.base / name
        root.mkdir(parents=True)
        shutil.copy(FIX / 'entail' / 'Inconsistent.ttl', root / 'Example.ttl')
        for path, text in questions.items():
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            (root / path).write_text(text)
            (root / path).with_suffix('.expected.csv').write_text('ask\ntrue\n')

    def run_main(self, *argv, base=None):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main(list(argv) + ['--base', str(base or self.base),
                                      '--catalog', str(self.base / 'catalog-v001.xml'),
                                      '--prod-about', str(self.base / 'AboutProd.ttl'),
                                      '--build-dir', str(self.tmp / 'build'), '--reasoner-memory', '1g'])
        return code, out.getvalue()

    def break_expectation(self, suite):
        (self.base / suite / 'basic' / 'Q.expected.csv').write_text('w\nex:w1\nex:w9\n')

    def test_annotation_levels(self):
        self.assertEqual(annotation_level('release', 'failure'), '::error')
        self.assertEqual(annotation_level('provisional', 'failure'), '::warning')
        self.assertEqual(annotation_level('provisional', 'broken'), '::error')
        self.assertEqual(annotation_level('release', 'warning'), '::warning')
        self.assertEqual(annotation_level('release', 'info'), '::notice')

    def test_good_suite_passes_and_logs_descriptions(self):
        code, out = self.run_main('release/good')
        self.assertEqual(code, 0, out)
        self.assertNotIn('::error', out)
        self.assertIn('::group::release/good', out)
        self.assertIn('basic/Q (reasoning): Both widgets are found.', out)
        # a reasoning: false question sees only the asserted triples
        self.assertIn('basic/Asserted (no reasoning): Without reasoning, w1 is not yet a Thing.', out)
        self.assertIn('release/good passed', out)

    def test_suite_without_reasoning_questions_skips_hermit(self):
        self.add_suite('release/plain', {'q/Plain.rq': ASK_ASSERTED.format(d='asserted z is a D')})
        code, out = self.run_main('release/plain')
        self.assertEqual(code, 0, out)       # the data is inconsistent, but HermiT never runs
        self.assertNotIn('HermiT', out)
        self.assertIn('release/plain passed', out)
        self.assertFalse((self.tmp / 'build' / 'release' / 'plain').exists())

    def test_reasoner_failure_still_runs_questions_without_reasoning(self):
        code, out = self.run_main('release/broken')
        self.assertEqual(code, 1)
        self.assertIn('inconsistent', out)
        self.assertIn('q/NeedsReasoner (reasoning): needs HermiT', out)
        self.assertIn('not run', out)
        plain = out.index('q/Plain (no reasoning)')
        self.assertIn('passed', out[plain:].splitlines()[1])

    def test_missing_metadata_is_error_and_others_run(self):
        (self.base / 'release/good/basic/Q.rq').write_text('PREFIX ex: <https://example.org/ex/>\n'
                                                           'SELECT ?w WHERE { ?w a ex:Widget }\n')
        code, out = self.run_main('release/good')
        self.assertEqual(code, 1)
        self.assertIn('::error file=', out)
        self.assertIn('"# description: …"', out)
        self.assertIn('w1 is a widget.', out)
        self.assertIn('release/good failed', out)

    def test_release_failure_is_error(self):
        self.break_expectation('release/good')
        code, out = self.run_main('release/good')
        self.assertEqual(code, 1)
        self.assertIn('::error file=', out)
        self.assertIn('missing row: ex:w9', out)

    def test_redact_hides_data(self):
        self.break_expectation('release/good')
        code, out = self.run_main('release/good', '--redact')
        self.assertEqual(code, 1)
        self.assertNotIn('ex:w9', out)
        self.assertNotIn('ex:w2', out)
        self.assertIn('2 failures', out)
        self.assertIn('details hidden', out)
        self.assertIn('Both widgets are found.', out)   # descriptions are still logged

    def test_redact_hides_import_details(self):
        code, out = self.run_main('release/unresolved', '--redact')
        self.assertEqual(code, 1)
        self.assertNotIn('nowhere', out)
        self.assertIn('details hidden', out)

    def test_provisional_failure_is_warning(self):
        shutil.copytree(self.base / 'release' / 'good', self.base / 'provisional' / 'good2')
        (self.base / 'provisional' / 'good2' / 'Example.ttl').write_text(
            (self.base / 'provisional' / 'good2' / 'Example.ttl').read_text().replace('/good/', '/good2/'))
        self.break_expectation('provisional/good2')
        code, out = self.run_main('provisional/good2')
        self.assertEqual(code, 0, out)
        self.assertIn('::warning file=', out)
        self.assertNotIn('::error', out)
        self.assertIn('provisional suites failed (warnings only): provisional/good2', out)
        self.assertNotIn('all competency questions passed', out)

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

    def test_update_expected_writes_file(self):
        (self.base / 'release' / 'good' / 'basic' / 'Q.expected.csv').unlink()
        code, out = self.run_main('release/good', '--update-expected')
        self.assertEqual(code, 0, out)
        self.assertEqual((self.base / 'release' / 'good' / 'basic' / 'Q.expected.csv').read_text(),
                         'w\nex:w1\nex:w2\n')

    def test_parallel_jobs_same_result(self):
        code, out = self.run_main('release/good', 'release/broken', '--jobs', '2')
        self.assertEqual(code, 1)
        self.assertLess(out.index('::group::release/broken'), out.index('::group::release/good'))
        self.assertIn('release/good passed', out)

    def test_malformed_suite_ontology_is_error_and_others_run(self):
        bad = self.base / 'release' / 'bad'
        bad.mkdir()
        (bad / 'Example.ttl').write_text('this is not turtle')
        code, out = self.run_main('release/bad', 'release/good')
        self.assertEqual(code, 1)
        self.assertIn('::error file=', out)
        self.assertIn('release/good passed', out)

    def test_catalog_entry_to_missing_file_is_error_and_others_run(self):
        (self.base / 'DevOnly.ttl').unlink()
        code, out = self.run_main('provisional/dev', 'release/good')
        self.assertEqual(code, 1)
        self.assertIn('DevOnly.ttl', out)
        self.assertIn('release/good passed', out)

    def test_corrupt_cache_is_error_and_others_run(self):
        self.run_main('release/good')
        (self.tmp / 'build' / 'release' / 'good' / 'entailed.nq').write_text('not n-quads at all\n')
        code, out = self.run_main('release/good', 'release/broken')
        self.assertEqual(code, 1)
        self.assertIn('release/good failed', out)
        self.assertIn('::group::release/broken', out)

    def test_set_selector_runs_one_set(self):
        (self.base / 'release/good/other').mkdir()
        (self.base / 'release/good/other/X.rq').write_text('SELECT * {}\n')   # broken, but not selected
        code, out = self.run_main('release/good/basic')
        self.assertEqual(code, 0, out)
        self.assertNotIn('other/X', out)

    def test_list_prints_suite_names_as_json(self):
        code, out = self.run_main('release', '--list')
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), ['release/broken', 'release/good', 'release/leaky',
                                           'release/unresolved'])

    def test_missing_questions_checkout_is_not_an_error(self):
        code, out = self.run_main(base=self.tmp / 'not-checked-out')
        self.assertEqual(code, 0)
        self.assertIn('::notice', out)
        self.assertIn('ontology-questions', out)
        code, out = self.run_main('--list', base=self.tmp / 'not-checked-out')
        self.assertEqual((code, json.loads(out)), (0, []))

    def test_unknown_selector_is_error(self):
        code, out = self.run_main('release/nope')
        self.assertEqual(code, 1)
        self.assertIn('::error', out)


if __name__ == '__main__':
    unittest.main()
