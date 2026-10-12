import copy
import json
import re
import unittest
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch
from housing_watch.study_report import render_study, uses_study, catalog_for, visuals_for, write_practice_bundle
from housing_watch.research_workflow import digest

ROOT = Path(__file__).resolve().parents[1]


class StudyReportTests(unittest.TestCase):
    def setUp(self):
        # Preserve the contracts of the historical tool-catalog edition.
        self.report = json.loads((ROOT/'config/devops_implementation.2026-10-10.r4.json').read_text(encoding='utf-8'))['reports'][0]
        self.catalog_file = json.loads((ROOT/'config/study_pages.json').read_text(encoding='utf-8'))['catalogs'][self.report['id']]

    def test_existing_report_ids_keep_their_layout_and_future_reports_use_study(self):
        legacy = json.loads((ROOT/'config/study_pages.json').read_text(encoding='utf-8'))['legacy_report_ids']
        self.assertTrue(legacy)
        self.assertTrue(all(not uses_study(id) for id in legacy))
        self.assertTrue(uses_study('new-study-report'))

    def test_beginner_evidence_is_embedded_once_with_its_chapter(self):
        report = json.loads((ROOT/'config/devops_implementation.2026-10-11.r5.json').read_text(encoding='utf-8'))['reports'][0]
        text = render_study(report)
        self.assertEqual(text.count('class="chapter-keypoints"'), 9)
        self.assertNotIn('class="tool-catalog"', text)
        self.assertLess(text.index('id="summary"'), text.index('id="visual-summary"'))
        self.assertLess(text.index('id="visual-summary"'), text.index('class="study-summary-deck"'))
        for chapter, next_chapter, title in [('cases','architecture',report['datasets'][0]['title']), ('research','study',report['datasets'][1]['title']), ('ci','principles',report['tables'][0]['title'])]:
            tag = 'caption' if chapter == 'ci' else 'h3'
            heading = '<'+tag+'>'+title+'</'+tag+'>'
            self.assertEqual(text.count(heading), 1)
            self.assertLess(text.index('id="chapter-'+chapter+'"'), text.index(heading))
            self.assertLess(text.index(heading), text.index('id="chapter-'+next_chapter+'"'))
        ids = re.findall(r'\bid="([^"]+)"', text)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(anchor in ids for anchor in re.findall(r'href="#([^"]+)"',text)))

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
        filename = 'devops_visuals.2026-10-10.r4.json'
        guide = json.loads((ROOT/'config'/filename).read_text(encoding='utf-8'))
        guide['images']['summary']['asset'] = '../outside.png'
        with patch('housing_watch.study_report.settings', return_value={'visual_guides':{self.report['id']:filename}}):
            with patch('housing_watch.study_report.json.loads', return_value=guide):
                with self.assertRaisesRegex(ValueError, 'asset filename'):
                    visuals_for(self.report)
        with patch('housing_watch.study_report.Path.read_bytes', return_value=b'changed'):
            with self.assertRaisesRegex(ValueError, 'reviewed bytes'):
                visuals_for(self.report)

    def test_executed_tutorial_commands_are_visible_without_opening_disclosures(self):
        report = json.loads((ROOT/'config/devops_implementation.2026-10-12.r11.json').read_text(encoding='utf-8'))['reports'][0]
        text = render_study(report)
        chapter = text.split('id="chapter-architecture"', 1)[1].split('id="chapter-operations"', 1)[0]
        count = sum(block['type']=='code' for block in report['explanation'][4]['blocks'])
        self.assertEqual(chapter.count('<details class="study-depth" open>'), count)
        self.assertIn('python smoke.py dist/v1.pyz', chapter)
        # An edited/future report must not inherit an edition-specific setting.
        report['deck'] += ' Other edition'
        self.assertNotIn('<details class="study-depth" open>', render_study(report))
        historical = json.loads((ROOT/'config/devops_implementation.2026-10-12.r9.json').read_text(encoding='utf-8'))['reports'][0]
        self.assertNotIn('<details class="study-depth" open>', render_study(historical))

    def test_reader_content_omits_editorial_badges_but_preserves_citations_and_conditions(self):
        report = json.loads((ROOT/'config/devops_implementation.2026-10-12.r12.json').read_text(encoding='utf-8'))['reports'][0]
        text = render_study(report)
        self.assertNotIn('검토 의견', text)
        self.assertNotIn('검토 범위', text)
        self.assertNotIn('class="learning-kind"', text)
        self.assertNotIn('class="learning-sources">근거 ', text)
        self.assertNotIn('사람 독자 시험', text)
        self.assertIn('학습용 가상 사례', text)
        self.assertIn('무중단 배포가 아닙니다', text)
        self.assertIn('python smoke.py dist/v1.pyz', text)
        for number, reference in enumerate(report['references'], 1):
            self.assertIn('href="#ref-%d"' % number, text)
            self.assertIn(reference['url'].replace('&', '&amp;'), text)
        historical = json.loads((ROOT/'config/devops_implementation.2026-10-12.r11.json').read_text(encoding='utf-8'))['reports'][0]
        self.assertIn('검토 의견', render_study(historical))

    def test_hierarchical_topics_have_nested_navigation_and_visible_commands(self):
        report = json.loads((ROOT/'config/devops_implementation.2026-10-12.r13.json').read_text(encoding='utf-8'))['reports'][0]
        html = render_study(report)
        primary = html.split('<details class="study-depth" id="learning-practice-files"',1)[0]
        self.assertEqual(primary.count('class="study-topic"'),12)
        self.assertEqual(len(re.findall(r'<h3>',primary)),12)
        self.assertIn('class="topic-number">3.2</span> 변경할 때 자동으로 검사하기',html)
        self.assertIn('data-section-link href="#topic-automation">3.2 변경할 때 자동으로 검사하기',html)
        self.assertNotIn('<details class="study-depth"',primary)
        self.assertNotIn('chapter-keypoints" aria-label',html)
        self.assertIn('<figcaption>PowerShell A — 버전 보관, 재검사, 운영 연습 서버 실행</figcaption>',html)
        self.assertIn('aria-label="현재 읽는 위치"',html)
        ids = re.findall(r'\bid="([^"]+)"',html)
        self.assertEqual(len(ids),len(set(ids)))
        self.assertTrue(all(anchor in ids for anchor in re.findall(r'href="#([^"]+)"',html)))
        self.assertIn('href="../assets/devops-sort-r13.zip"',render_study(report,prefix='../',edition=13))
        report['deck'] += ' changed'
        future = render_study(report)
        self.assertNotIn('class="study-topic"',future)
        self.assertNotIn('href="assets/devops-sort-r13.zip"',future)

    def test_practice_download_contains_reviewed_code_and_rejects_unsafe_mapping(self):
        report = json.loads((ROOT/'config/devops_implementation.2026-10-12.r13.json').read_text(encoding='utf-8'))['reports'][0]
        with tempfile.TemporaryDirectory() as temporary:
            path = write_practice_bundle(report,temporary)
            first = path.read_bytes()
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(len(archive.namelist()),9)
                for block in report['learning'][0]['blocks']:
                    self.assertEqual(archive.read('devops-sort/'+block['title']),block['text'].encode('utf-8'))
            write_practice_bundle(report,temporary)
            self.assertEqual(path.read_bytes(),first)
            previous = copy.deepcopy(report)
            previous['deck'] += ' unbound'
            self.assertIsNone(write_practice_bundle(previous,temporary))
        filename = 'devops_visuals.2026-10-12.r13.json'
        guide = json.loads((ROOT/'config'/filename).read_text(encoding='utf-8'))
        with patch('housing_watch.study_report.settings',return_value={'visual_guides':{report['id']:filename}}):
            altered = copy.deepcopy(guide)
            altered['practice_bundle']['files'][0]['path'] = '../escape.py'
            with patch('housing_watch.study_report.json.loads',return_value=altered):
                with self.assertRaisesRegex(ValueError,'Unsafe practice'):
                    visuals_for(report)
            altered = copy.deepcopy(guide)
            altered['topic_sections']['overview'][1]['id'] = 'definition'
            with patch('housing_watch.study_report.json.loads',return_value=altered):
                with self.assertRaisesRegex(ValueError,'IDs must be unique'):
                    visuals_for(report)

    def test_visuals_stay_with_their_topics_and_do_not_change_the_historical_practice(self):
        report = json.loads((ROOT/'config/devops_implementation.2026-10-12.r14.json').read_text(encoding='utf-8'))['reports'][0]
        previous = json.loads((ROOT/'config/devops_implementation.2026-10-12.r13.json').read_text(encoding='utf-8'))['reports'][0]
        html = render_study(report)
        self.assertEqual(html.count('class="process-figure '),2)
        self.assertIn('CI/CD의 자동화 범위와 운영 배포 시점',html.split('id="topic-cicd"',1)[1].split('id="chapter-system"',1)[0])
        self.assertIn('id="visual-change-flow"',html.split('id="topic-flow"',1)[1].split('id="topic-tools"',1)[0])
        self.assertIn('id="visual-version-recovery"',html.split('id="topic-recover"',1)[1].split('id="topic-improve"',1)[0])
        self.assertNotIn('class="process-figure ',render_study(previous))
        self.assertEqual(report['learning'],previous['learning'])
        self.assertEqual([b for c in report['explanation'] for b in c['blocks'] if b['type']=='code'],[b for c in previous['explanation'] for b in c['blocks'] if b['type']=='code'])
        with tempfile.TemporaryDirectory() as temporary:
            first=write_practice_bundle(previous,temporary).read_bytes()
            self.assertEqual(write_practice_bundle(report,temporary).read_bytes(),first)
        ids=re.findall(r'\bid="([^"]+)"',html)
        self.assertEqual(len(ids),len(set(ids)))
        self.assertTrue(all(anchor in ids for anchor in re.findall(r'href="#([^"]+)"',html)))

    def test_visual_mapping_requires_canonical_steps_and_valid_table_location(self):
        report=json.loads((ROOT/'config/devops_implementation.2026-10-12.r14.json').read_text(encoding='utf-8'))['reports'][0]
        filename='devops_visuals.2026-10-12.r14.json'
        guide=json.loads((ROOT/'config'/filename).read_text(encoding='utf-8'))
        with patch('housing_watch.study_report.settings',return_value={'visual_guides':{report['id']:filename}}):
            altered=copy.deepcopy(guide)
            altered['block_visuals'][0]['path']='/explanation/1/blocks/0'
            with patch('housing_watch.study_report.json.loads',return_value=altered):
                with self.assertRaisesRegex(ValueError,'reviewed process steps'):
                    visuals_for(report)
            altered=copy.deepcopy(guide)
            altered['topic_tables']={'missing-topic':['overview-cicd']}
            with patch('housing_watch.study_report.json.loads',return_value=altered):
                with self.assertRaisesRegex(ValueError,'table placement'):
                    visuals_for(report)
