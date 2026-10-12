import tempfile
import unittest
from pathlib import Path

from housing_watch.editorial import render_editorial
from housing_watch.research_data import load_report_input


class BusinessPublicationTests(unittest.TestCase):
    def test_reviewed_business_opening_teaches_before_comparison_and_preserves_previous_editions(self):
        from html.parser import HTMLParser

        original = load_report_input(Path("config/business_planning.2026-10-08.json"))
        reviewed = load_report_input(Path("config/business_review.2026-10-12.json"))
        current = {r["id"]: r for r in original}
        current.update({r["id"]: r for r in reviewed})
        history = [{"id": r["id"], "revision": 1, "document": r,
                    "saved_at": "2026-10-08T00:00:00Z"} for r in original]

        class Banner(HTMLParser):
            in_banner = False
            tables = 0
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if attrs.get("id") == "banner":
                    self.in_banner = True
                if tag == "table" and self.in_banner:
                    self.tables += 1
            def handle_endtag(self, tag):
                if tag == "section":
                    self.in_banner = False

        with tempfile.TemporaryDirectory() as root:
            render_editorial(root, {"topics": [], "items": []}, reviewed[0],
                             {"reports": list(current.values()), "report_history": history,
                              "report_versions": [{"id": r["id"], "revision": 2} for r in reviewed]}, standalone=False)
            for report in reviewed:
                html = (Path(root) / "preview" / (report["id"] + ".html")).read_text(encoding="utf-8")
                banner = Banner(); banner.feed(html)
                self.assertEqual(banner.tables, 0)
                self.assertLess(html.index('id="summary"'), html.index('<table'))
                self.assertIn(report["deck"], html)
                self.assertIn(report["tables"][0]["title"], html)
                old = (Path(root) / "preview/history" / (report["id"] + "-r1.html")).read_text(encoding="utf-8")
                self.assertIn('class="image object evidence-panel"', old)
                self.assertIn('이전 기록 · 1차', old)

    def test_three_sourced_reports_reach_dedicated_board_and_formal_route(self):
        reports = load_report_input(Path("config/business_planning.2026-10-08.json"))
        self.assertEqual({r["topic_path"][1] for r in reports}, {"국책사업", "영업 기회", "경쟁사·시장"})
        self.assertTrue(all(r.get("explanation") for r in reports))
        with tempfile.TemporaryDirectory() as root:
            render_editorial(root, {"topics": [], "items": []}, reports[0], {"reports": reports}, standalone=False)
            board = (Path(root) / "preview/business.html").read_text(encoding="utf-8")
            formal = (Path(root) / "research/business/index.html").read_text(encoding="utf-8")
            for report in reports:
                self.assertIn(report["id"] + ".html", board)
                self.assertIn('../../preview/' + report["id"] + ".html", formal)
            self.assertIn('id="report-topic"', board)
            self.assertNotIn("business.sqlite3", board)
            self.assertNotIn("technical_evidence", board)
            self.assertNotIn("private customer sentinel", board)
