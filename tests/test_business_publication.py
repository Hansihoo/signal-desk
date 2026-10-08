import tempfile
import unittest
from pathlib import Path

from housing_watch.editorial import render_editorial
from housing_watch.research_data import load_report_input


class BusinessPublicationTests(unittest.TestCase):
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
