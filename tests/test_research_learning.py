import copy
import json
import re
import tempfile
import unittest
from html.parser import HTMLParser

from housing_watch.briefing_preview import build_briefing_preview
from housing_watch.db import connect, init_db
from housing_watch.research_data import (
    build_research_data, import_reports, load_report_input, validate_report,
)


class DisclosureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chapters = []
        self.code_regions = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "details" and attrs.get("class") == "learning-chapter":
            self.chapters.append(attrs)
        if tag == "pre":
            self.code_regions.append(attrs)


class ResearchLearningTests(unittest.TestCase):
    def setUp(self):
        # Exercise every block type with a fixed immutable fixture. A newer
        # editorial revision may legitimately use a different selection of blocks.
        self.report = next(copy.deepcopy(r) for r in load_report_input(
            'config/development_learning.2026-10-04.json') if r['id'] == 'mcp-apps-workflows')

    def test_rejects_invalid_learning_before_mutating_storage(self):
        conn = connect(":memory:")
        self.addCleanup(conn.close)
        init_db(conn)
        import_reports(conn, [self.report])
        for mutation in (
            lambda r: r["learning"].append(copy.deepcopy(r["learning"][0])),
            lambda r: r["learning"][0].update(blocks=[]),
            lambda r: r["learning"][0]["blocks"][0].update(source_ids=["missing"]),
            lambda r: r["learning"][0]["blocks"][0].update(source_ids=[]),
            lambda r: r["learning"][0]["blocks"][0].update(type="html"),
            lambda r: r["learning"][0]["blocks"][0].update(css="background:red"),
            lambda r: r["learning"][0]["blocks"][1]["items"][0].update(text=""),
        ):
            with self.subTest(mutation=mutation):
                invalid = copy.deepcopy(self.report)
                mutation(invalid)
                with self.assertRaises(ValueError):
                    import_reports(conn, [invalid])
                row = conn.execute("SELECT revision, document FROM research_reports").fetchone()
                self.assertEqual(row["revision"], 1)
                self.assertEqual(json.loads(row["document"]), self.report)

    def test_learning_round_trip_and_collapsed_semantic_rendering(self):
        conn = connect(":memory:")
        self.addCleanup(conn.close)
        init_db(conn)
        build_research_data(conn, [], [])
        report = copy.deepcopy(self.report)
        report["learning"][0]["blocks"][0]["text"] = '<img src=x onerror="alert(1)">'
        code_block = next(b for l in report["learning"] for b in l["blocks"] if b["type"] == "code")
        code_block["text"] = "<script>danger()</script>\nsecond line"
        code_block["title"] = 'Code " onfocus="alert(1)'
        import_reports(conn, [report])
        data = build_research_data(conn, [], [])
        stored = next(r for r in data["reports"] if r["id"] == report["id"])
        # Previously applied publication batches must preserve this later edit.
        self.assertEqual(stored, report)
        with tempfile.TemporaryDirectory() as temp:
            output = build_briefing_preview(temp, {"items": [], "topics": []}, stored)
            html = (output / "report.html").read_text(encoding="utf-8")
        parser = DisclosureParser()
        parser.feed(html)
        self.assertEqual(len(parser.chapters), len(report["learning"]))
        self.assertTrue(all("open" not in chapter for chapter in parser.chapters))
        self.assertEqual(len({d["id"] for d in parser.chapters}), len(parser.chapters))
        self.assertIn("<dl ", html)
        self.assertIn("<ol ", html)
        self.assertIn("<code>&lt;script&gt;danger()", html)
        code_region = next(region for region in parser.code_regions
                           if region.get("aria-label") == code_block["title"])
        self.assertEqual(code_region.get("tabindex"), "0")
        self.assertEqual(code_region.get("role"), "region")
        self.assertNotIn("onfocus", code_region)
        self.assertIn("\nsecond line", html)
        self.assertIn("&lt;img src=x", html)
        self.assertNotIn("<script>", html)
        self.assertNotIn("<img src=x", html)
        self.assertIn("가상 예시", html)
        self.assertIn("검토 의견", html)
        for anchor in re.findall(r'href="#(ref-\d+)"', html):
            self.assertIn('id="%s"' % anchor, html)

    def test_old_report_has_no_empty_learning_section(self):
        old = load_report_input()[0]
        validate_report(old)
        with tempfile.TemporaryDirectory() as temp:
            output = build_briefing_preview(temp, {"items": [], "topics": []}, old)
            html = (output / "report.html").read_text(encoding="utf-8")
        self.assertNotIn('id="learning"', html)
        self.assertNotIn('href="#learning"', html)
        self.assertNotIn("__LEARNING", html)


if __name__ == "__main__":
    unittest.main()
