import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from housing_watch.study_report import _process_figure, render_study, visuals_for
from housing_watch.research_workflow import digest

ROOT = Path(__file__).resolve().parents[1]


class PositionVisualTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((ROOT/'config/rea_ghidra_research.2026-10-17.r4.json').read_text(encoding='utf-8'))['reports'][0]
        self.guide = json.loads((ROOT/'config/rea_ghidra_visuals.2026-10-17.r4.json').read_text(encoding='utf-8'))

    def test_parallel_states_keep_accessible_labels_without_sequence_arrows(self):
        page = render_study(self.report)
        figure = page.split('class="position-figure"', 1)[1].split('</figure>', 1)[0]
        for label in ['x = 0', 'x = 320', 'x = 640', '−500', '+500', '가운데']:
            self.assertIn(label, figure)
        self.assertIn('aria-hidden="true"', figure)
        self.assertNotIn('visual-arrow', figure)
        self.assertIn('실제 벽돌이 이 세 곳에 배치됐다는 뜻은 아닙니다', page)
        self.assertLess(page.index('옛 DLL'), page.index('<caption>같은 조사'))
        self.assertLess(page.index('네이티브 분석 대상'), page.index('<caption>같은 조사'))

    def test_visual_requires_three_complete_states(self):
        report = copy.deepcopy(self.report)
        report['explanation'][1]['blocks'][7]['items'].pop()
        guide = copy.deepcopy(self.guide)
        guide['report_hash'] = digest(report)
        with patch('housing_watch.study_report.settings', return_value={'visual_guides':{report['id']:'rea_ghidra_visuals.2026-10-17.r4.json'}}), patch('housing_watch.study_report.json.loads', return_value=guide):
            with self.assertRaisesRegex(ValueError, 'three reviewed states'):
                visuals_for(report)

    def test_visual_escapes_authored_text(self):
        block = copy.deepcopy(self.report['explanation'][1]['blocks'][7])
        block['items'][0] = {'label':'<input>', 'text':'<value>\n<script>'}
        page = _process_figure(block, {'kind':'positions','id':'visual-example'}, {'dxball':1,'dx-evidence':2})
        self.assertNotIn('<script>', page)
        self.assertIn('&lt;value&gt;', page)


if __name__ == '__main__':
    unittest.main()
