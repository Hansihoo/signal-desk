import copy
import json
import re
import unittest
from pathlib import Path
from unittest.mock import patch
from housing_watch.study_report import render_study, uses_study, catalog_for, visuals_for
from housing_watch.research_workflow import digest

ROOT = Path(__file__).resolve().parents[1]


class StudyReportTests(unittest.TestCase):
    def setUp(self):
        manifest = json.loads((ROOT/'config/research_publication.json').read_text(encoding='utf-8'))
        for batch in reversed(manifest['batches']):
            reports = json.loads((ROOT/'config'/batch['input']).read_text(encoding='utf-8'))['reports']
            current = next((r for r in reports if r['id'] == 'devops-implementation-guide'), None)
            if current:
                self.report = current
                break
        self.catalog_file = json.loads((ROOT/'config/study_pages.json').read_text(encoding='utf-8'))['catalogs'][self.report['id']]

    def test_existing_report_ids_keep_their_layout_and_future_reports_use_study(self):
        legacy = json.loads((ROOT/'config/study_pages.json').read_text(encoding='utf-8'))['legacy_report_ids']
        self.assertTrue(legacy)
        self.assertTrue(all(not uses_study(id) for id in legacy))
        self.assertTrue(uses_study('new-study-report'))

    def test_catalog_is_bound_to_content_and_history_does_not_use_later_catalog(self):
        self.assertEqual(len(catalog_for(self.report)['tools']), 15)
        previous = copy.deepcopy(self.report)
        previous['deck'] += ' 이전 판'
        self.assertIsNone(catalog_for(previous))
        rendered = render_study(previous)
        self.assertNotIn('class="tool-catalog"', rendered)
        self.assertIn('Jenkins', rendered)

    def test_citations_and_all_primary_chapters_are_addressable(self):
        rendered = render_study(self.report)
        ids = re.findall(r'\bid="([^"]+)"', rendered)
        self.assertEqual(len(ids), len(set(ids)))
        for ref in re.findall(r'href="#([^"]+)"', rendered):
            self.assertIn(ref, ids)
        self.assertLess(rendered.index('id="summary"'), rendered.index('id="outline"'))
        self.assertLess(rendered.index('id="outline"'), rendered.index('id="chapter-overview"'))
        self.assertEqual(rendered.count('class="study-chapter" id="chapter-'), 13)
        self.assertIn('id="data"', rendered)

    def test_catalog_copy_drift_and_unsafe_links_are_rejected(self):
        original = json.loads((ROOT/'config'/self.catalog_file).read_text(encoding='utf-8'))
        with patch('housing_watch.study_report.json.loads', return_value=original):
            with patch('housing_watch.study_report.settings', return_value={'catalogs':{self.report['id']:self.catalog_file}}):
                altered = copy.deepcopy(original)
                altered['tools'][0]['reuse'] = 'unreviewed new factual copy'
                with patch('housing_watch.study_report.json.loads', return_value=altered):
                    with self.assertRaisesRegex(ValueError, 'differs'):
                        catalog_for(self.report)
                altered['tools'][0]['docs'] = 'javascript:alert(1)'
                with patch('housing_watch.study_report.json.loads', return_value=altered):
                    with self.assertRaisesRegex(ValueError, 'Unsafe'):
                        catalog_for(self.report)

    def test_embedded_data_is_safe_and_preserves_special_characters(self):
        catalog = {'tools':[{'id':'special','name':'<script>&"한글','field':'CI/CD','tier':'상황별 권장','kind':'도구','purpose':'</script>','use':'예시','reuse':'기능','fit':'조건','jenkins':'추가','limits':'주의','alternatives':'대안','license':'MIT','docs':'https://example.com','repo':'https://example.com','license_url':'https://example.com','maintenance':'확인','source_ids':[]}]}
        with patch('housing_watch.study_report.catalog_for', return_value=catalog):
            text = render_study(self.report)
        payload = re.search(r'<script type="application/json" id="study-tools">(.*?)</script>', text, re.S).group(1)
        self.assertNotIn('<script>', payload)
        self.assertEqual(json.loads(payload), catalog['tools'])
        self.assertIn('&lt;/script&gt;', text)

    def test_visuals_bind_to_edition_and_keypoints_precede_full_explanation(self):
        guide = visuals_for(self.report)
        self.assertEqual(len(guide['images']), 4)
        previous = copy.deepcopy(self.report)
        previous['deck'] += ' 이전 판'
        self.assertIsNone(visuals_for(previous))
        self.assertNotIn('class="study-visual"', render_study(previous))
        rendered = render_study(self.report)
        self.assertEqual(rendered.count('class="chapter-keypoints"'), 13)
        self.assertEqual(rendered.count('class="study-visual"'), 4)
        ci = rendered.split('id="chapter-ci"', 1)[1].split('id="chapter-quality"', 1)[0]
        self.assertLess(ci.index('class="chapter-keypoints"'), ci.index('id="visual-ci"'))
        self.assertLess(ci.index('id="visual-ci"'), ci.index('class="chapter-lead"'))
        self.assertIn('aria-labelledby="study-image-title"', rendered)
        self.assertIn('data:image/png;base64,', rendered)

    def test_visual_asset_traversal_and_changed_bytes_are_rejected(self):
        filename = json.loads((ROOT/'config/study_pages.json').read_text(encoding='utf-8'))['visual_guides'][self.report['id']]
        guide = json.loads((ROOT/'config'/filename).read_text(encoding='utf-8'))
        guide['images']['summary']['asset'] = '../outside.png'
        with patch('housing_watch.study_report.settings', return_value={'visual_guides':{self.report['id']:filename}}):
            with patch('housing_watch.study_report.json.loads', return_value=guide):
                with self.assertRaisesRegex(ValueError, 'asset filename'):
                    visuals_for(self.report)
        with patch('housing_watch.study_report.Path.read_bytes', return_value=b'changed'):
            with self.assertRaisesRegex(ValueError, 'reviewed bytes'):
                visuals_for(self.report)
