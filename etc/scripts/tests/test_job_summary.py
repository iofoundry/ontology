import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import check_module_iris
import hygiene_runner
import job_summary
from hygiene_runner import annotate, summary_markdown, write_summary


class HygieneSummaryTest(unittest.TestCase):
    def setUp(self):
        findings = mock.patch.object(hygiene_runner, 'FINDINGS', [])
        findings.start()
        self.addCleanup(findings.stop)

    def report(self, about, *annotations):
        hygiene_runner.CURRENT_ABOUT = about
        with redirect_stdout(io.StringIO()) as out:
            for a in annotations:
                annotate(*a)
        return out.getvalue()

    def test_annotations_are_printed_and_errors_and_warnings_recorded(self):
        out = self.report('AboutIOFProd.rdf',
                          ('error', 'Label', 'X has no label | twice', 'core/Core.rdf'),
                          ('warning', 'Reasoner', 'slow'),
                          ('notice', 'Reasoner', 'consistent'))
        self.assertIn('::error file=core/Core.rdf,title=Label::X has no label | twice\n', out)
        self.assertIn('::warning title=Reasoner::slow\n', out)
        self.assertEqual([f['level'] for f in hygiene_runner.FINDINGS], ['error', 'warning'])

    def test_summary_has_one_section_per_about_file_listing_errors_and_warnings(self):
        self.report('AboutIOFProd.rdf', ('error', 'Label', 'X has no label | twice', 'core/Core.rdf'),
                    ('warning', 'Reasoner', 'slow'))
        self.report('AboutIOFDev.rdf', ('notice', 'Reasoner', 'consistent'))
        text = summary_markdown(['AboutIOFDev.rdf', 'AboutIOFProd.rdf'], hygiene_runner.FINDINGS)
        self.assertIn('## ✅ Hygiene tests: AboutIOFDev.rdf: 0 errors, 0 warnings', text)
        self.assertIn('## ❌ Hygiene tests: AboutIOFProd.rdf: 1 error, 1 warning', text)
        self.assertIn('| Label | core/Core.rdf | X has no label \\| twice |', text)
        self.assertIn('### Warnings\n\n| Rule | File | Message |\n|---|---|---|\n| Reasoner |  | slow |', text)
        self.assertLess(text.index('AboutIOFDev'), text.index('AboutIOFProd'))
        self.assertNotIn('consistent', text)

    def test_summary_is_written_only_under_github_actions(self):
        self.report('AboutIOFProd.rdf', ('warning', 'Reasoner', 'slow'))
        page = Path(tempfile.mkdtemp()) / 'summary.md'
        with mock.patch.dict(os.environ, {'GITHUB_STEP_SUMMARY': str(page)}):
            write_summary(['AboutIOFProd.rdf'])
        self.assertIn('## ⚠️ Hygiene tests: AboutIOFProd.rdf: 0 errors, 1 warning', page.read_text())
        with mock.patch.dict(os.environ):
            os.environ.pop('GITHUB_STEP_SUMMARY', None)
            write_summary(['AboutIOFProd.rdf'])      # nowhere to write: no error


class JobSummaryTest(unittest.TestCase):
    def test_parse_reads_errors_and_warnings_with_colons_in_the_title(self):
        self.assertEqual(job_summary.parse('::error file=a/B.rdf,line=12,title=rdfs:isDefinedBy::x <y> is wrong'),
                         {'level': 'error', 'title': 'rdfs:isDefinedBy', 'file': 'a/B.rdf', 'line': '12',
                          'message': 'x <y> is wrong'})
        self.assertEqual(job_summary.parse('::warning::<z> has no home')['message'], '<z> has no home')
        self.assertIsNone(job_summary.parse('::notice title=T::fine'))
        self.assertIsNone(job_summary.parse('plain output'))

    def test_recording_collects_printed_annotations_and_still_prints_them(self):
        with redirect_stdout(io.StringIO()) as out:
            with job_summary.recording() as findings:
                print('::error file=a.rdf,line=3,title=Ontology IRI::bad IRI')
                print('chatter')
                sys.stdout.write('::warning::no newline at the end')
        self.assertIn('chatter', out.getvalue())
        self.assertEqual([f['level'] for f in findings], ['error', 'warning'])
        self.assertIn('| Ontology IRI | a.rdf:3 | bad IRI |', job_summary.section('Module IRIs', findings))

    def test_module_iri_page_lists_problems_but_not_the_closing_count(self):
        def check():
            print('::error file=a.rdf,line=3,title=Ontology IRI::bad IRI')
            print('::error title=Module IRIs::2 modules: 1 error(s), 0 warning(s). Run ...')
            return 1, 2
        page = Path(tempfile.mkdtemp()) / 'summary.md'
        with mock.patch.object(check_module_iris, 'check', check), \
                mock.patch.dict(os.environ, {'GITHUB_STEP_SUMMARY': str(page)}), redirect_stdout(io.StringIO()):
            self.assertEqual(check_module_iris.main(), 1)
        text = page.read_text()
        self.assertIn('## ❌ Module IRIs: 2 modules: 1 error, 0 warnings', text)
        self.assertIn('| Ontology IRI | a.rdf:3 | bad IRI |', text)
        self.assertNotIn('Run ...', text)


if __name__ == '__main__':
    unittest.main()
