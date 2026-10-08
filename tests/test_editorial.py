import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from housing_watch.briefing_preview import build_briefing_preview
from housing_watch.db import connect, init_db
from housing_watch.research_data import build_research_data, import_reports, load_report_input


class EditorialTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        init_db(self.conn)
        self.report = load_report_input()[0]
        publication = {"featured_report_id": self.report["id"], "report_ids": [self.report["id"]]}
        patcher = patch("housing_watch.research_data.load_publication", return_value=(publication, []))
        patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(self.conn.close)

    def test_essential_explanation_is_visible_before_data_and_optional_depth_stays_collapsed(self):
        from html.parser import HTMLParser
        report = copy.deepcopy(self.report)
        report['deck'] = '후보의 조건을 비교한 뒤 하나를 선택하는 이유를 설명한다.'
        report['explanation'] = [{
            'id': 'roles', 'title': '역할 이해', 'lead': '조회와 표시를 구분한다.',
            'blocks': [{'type': 'paragraph', 'kind': 'fact', 'title': '읽는 주체',
                        'text': '<서버>가 HTML을 제공한다.\n\n호스트가 읽고 결과를 표시한다.',
                        'source_ids': [report['references'][0]['id']]}]}]
        report['learning'] = [{
            'id': 'roles', 'title': '추가 연습', 'lead': '다른 업무에 적용한다.',
            'blocks': [{'type': 'paragraph', 'kind': 'example', 'title': '가상 연습',
                        'text': '매출 표의 날짜를 바꿔 보자.', 'source_ids': []}]}]
        import_reports(self.conn, [report])
        data = build_research_data(self.conn, [], [])
        with tempfile.TemporaryDirectory() as temp:
            output = build_briefing_preview(temp, {'topics': [], 'items': []}, report, data)
            html = (output / (report['id'] + '.html')).read_text(encoding='utf-8')
            self.assertLess(html.index('id="explanation"'), html.index('id="data"'))
            self.assertIn('<p>&lt;서버&gt;가 HTML을 제공한다.</p><p>호스트가 읽고 결과를 표시한다.</p>', html)
            self.assertIn('href="#explanation">본문</a>', html)
            self.assertIn('href="#ref-1"', html)
            class ReadingPath(HTMLParser):
                depth = 0
                essential_depth = None
                optional_open = None
                def handle_starttag(self, tag, attrs):
                    attrs = dict(attrs)
                    if tag == 'details':
                        self.depth += 1
                    if attrs.get('id') == 'explanation-roles':
                        self.essential_depth = self.depth
                    if attrs.get('id') == 'learning-roles':
                        self.optional_open = 'open' in attrs
                def handle_endtag(self, tag):
                    if tag == 'details':
                        self.depth -= 1
            reading = ReadingPath(); reading.feed(html)
            self.assertEqual(reading.essential_depth, 0)
            self.assertFalse(reading.optional_open)
            main = (output / 'index.html').read_text(encoding='utf-8')
            self.assertIn('<h3><a href="%s.html">' % report['id'], main)
            self.assertIn('<p>%s</p>' % report['deck'], main)
            legacy = copy.deepcopy(report); del legacy['explanation']
            import_reports(self.conn, [legacy])
            data = build_research_data(self.conn, [], [])
            build_briefing_preview(temp, {'topics': [], 'items': []}, legacy, data)
            html = (output / (legacy['id'] + '.html')).read_text(encoding='utf-8')
            self.assertNotIn('href="#explanation"', html)
            self.assertNotIn('id="explanation"', html)

    def test_deep_topics_remain_under_parent_and_link_to_their_report(self):
        from housing_watch.editorial import _tree, _board_tools
        from html.parser import HTMLParser

        parent = copy.deepcopy(self.report)
        parent.update(id="hackathon-notice", topic_path=["지원·참여", "해커톤·공모전"])
        child = copy.deepcopy(self.report)
        child.update(id="hackathon-learning", topic_path=["지원·참여", "해커톤·공모전", "기술 학습"])
        other = copy.deepcopy(self.report)
        other.update(id="hackathon-advanced", topic_path=["지원·참여", "해커톤·공모전", "기술 학습", "심화 <자료>"])

        class TreeParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.depth, self.links = 0, []
            def handle_starttag(self, tag, attrs):
                if tag == "ul":
                    self.depth += 1
                if tag == "a":
                    self.links.append((self.depth, dict(attrs)["href"]))
            def handle_endtag(self, tag):
                if tag == "ul":
                    self.depth -= 1

        tree = _tree([parent, child, other], "../", other["id"])
        parser = TreeParser()
        parser.feed(tree)
        self.assertEqual([depth for depth, _ in parser.links], [2, 3, 4])
        self.assertEqual(parser.links[-1][1], "../hackathon-advanced.html")
        self.assertIn("&lt;자료&gt;", tree)
        self.assertIn("<small>3</small>", tree)
        self.assertEqual(tree.count('aria-current="page"'), 3)
        options = _board_tools([other])
        self.assertIn('value="지원·참여">지원·참여 전체', options)
        self.assertIn('해커톤·공모전 / 기술 학습 / 심화 &lt;자료&gt;', options)
        self.assertIn('value="지원·참여 / 해커톤·공모전"', options)

    def test_new_reports_accumulate_even_without_changing_curated_manifest(self):
        import_reports(self.conn, [self.report])
        with tempfile.TemporaryDirectory() as temp:
            root = build_briefing_preview(temp, {}, self.report, build_research_data(self.conn, [], []))
            before = (root / (self.report["id"] + ".html")).read_bytes()
            new = copy.deepcopy(self.report)
            new.update(id="new-topic-report", title="새 주제의 검토 결과", checked_on="2026-10-07")
            new["topic_path"] = ["새 리서치", "새 주제"]
            import_reports(self.conn, [new])
            build_briefing_preview(temp, {}, self.report, build_research_data(self.conn, [], []))
            home = (root / "index.html").read_text(encoding="utf-8")
            self.assertIn('href="new-topic-report.html"', home)
            self.assertIn('href="%s.html"' % self.report["id"], home)
            self.assertEqual(home.count('class="research-post"'), 2)
            self.assertTrue((root / "new-topic-report.html").is_file())
            # Navigation can grow; the existing authored body must remain intact.
            self.assertIn(self.report["deck"], (root / (self.report["id"] + ".html")).read_text(encoding="utf-8"))
            self.assertNotEqual(before, (root / (self.report["id"] + ".html")).read_bytes())

    def test_updates_preserve_addressable_previous_editions_and_stable_routes(self):
        import_reports(self.conn, [self.report])
        changed = copy.deepcopy(self.report)
        changed.update(title="두 번째 검토 결과", checked_on="2026-10-07")
        import_reports(self.conn, [changed])
        data = build_research_data(self.conn, [], [])
        self.assertEqual(data["report_history"][0]["document"], self.report)
        self.assertEqual(data["report_history"][1]["document"], changed)
        with tempfile.TemporaryDirectory() as temp:
            root = build_briefing_preview(temp, {}, changed, data)
            old_path = root / "history" / (self.report["id"] + "-r1.html")
            old = old_path.read_bytes()
            html = old.decode("utf-8")
            self.assertIn("<h1>%s</h1>" % self.report["title"], html)
            self.assertIn('href="../%s.html"' % self.report["id"], html)
            self.assertIn('href="history/%s-r1.html"' % self.report["id"], (root / "report.html").read_text(encoding="utf-8"))
            self.assertIn('href="%s-r1.html"' % self.report["id"], (root / "history/index.html").read_text(encoding="utf-8"))
            build_briefing_preview(temp, {}, changed, data)
            self.assertEqual(old_path.read_bytes(), old)
            self.assertFalse((root / "history" / (self.report["id"] + "-r2.html")).exists())

    def test_history_is_validated_before_any_output_is_written(self):
        import_reports(self.conn, [self.report])
        data = build_research_data(self.conn, [], [])
        data["report_history"][0]["id"] = "../../escape"
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                build_briefing_preview(temp, {}, self.report, data)
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_standalone_pages_have_embedded_design_fonts_and_local_evidence_links(self):
        with tempfile.TemporaryDirectory() as temp:
            root = build_briefing_preview(temp, {}, self.report)
            home = (root / "index.html").read_text(encoding="utf-8")
            report = (root / "report.html").read_text(encoding="utf-8")
            self.assertIn("data:font/woff2;base64,", report)
            self.assertNotIn("@import", report)
            self.assertNotIn("fonts.googleapis.com", report)
            self.assertNotIn('href="#ref-', home)
            self.assertTrue('href="%s.html"' % self.report["id"] in home)
            self.assertIn("HTML5 UP Editorial", report)
            for section in ("summary", "data", "result", "references"):
                self.assertIn('id="%s"' % section, report)
            self.assertLess(report.index('id="summary"'), report.index('id="data"'))
            self.assertLess(report.index('id="data"'), report.index('id="result"'))

    def test_published_pages_share_one_local_stylesheet_with_working_history_prefix(self):
        import_reports(self.conn, [self.report])
        changed = copy.deepcopy(self.report)
        changed["title"] = "다음 검토"
        import_reports(self.conn, [changed])
        with tempfile.TemporaryDirectory() as temp:
            root = build_briefing_preview(temp, {}, changed, build_research_data(self.conn, [], []), standalone=False)
            current = (root / "report.html").read_text(encoding="utf-8")
            previous = (root / "history" / (changed["id"] + "-r1.html")).read_text(encoding="utf-8")
            self.assertTrue('href="briefing.css?v=' in current)
            self.assertTrue('href="../briefing.css?v=' in previous)
            self.assertNotIn("data:font/woff2", current)
            self.assertTrue("data:font/woff2;base64," in (root / "briefing.css").read_text(encoding="utf-8"))
            self.assertIn(changed["title"], current)
            self.assertIn(self.report["title"], previous)


if __name__ == "__main__":
    unittest.main()
