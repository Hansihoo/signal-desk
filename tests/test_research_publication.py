import copy
import json
import re
import tempfile
import unittest
from pathlib import Path

from housing_watch.briefing_preview import build_briefing_preview
from housing_watch.db import connect, init_db
from housing_watch.research_data import (
    apply_publication, build_research_data, import_reports, load_publication, load_report_input, validate_report,
)


class ResearchPublicationTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        init_db(self.conn)
        self.publication, self.batches = load_publication()
        self.reviewed_ids = {report["id"] for _, reports in self.batches for report in reports}

    def tearDown(self):
        self.conn.close()

    def test_reviewed_batch_is_applied_once_and_keeps_later_edits(self):
        apply_publication(self.conn, self.publication, self.batches)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM research_reports").fetchone()[0], len(self.reviewed_ids))
        before = self.conn.execute("SELECT COUNT(*) FROM research_report_revisions").fetchone()[0]
        edited = copy.deepcopy(self.batches[-1][1][0])
        old_revision = self.conn.execute("SELECT revision FROM research_reports WHERE id=?", (edited["id"],)).fetchone()[0]
        edited["title"] = "후속 검토로 바뀐 제목"
        import_reports(self.conn, [edited])
        apply_publication(self.conn, self.publication, self.batches)
        row = self.conn.execute("SELECT revision, document FROM research_reports WHERE id=?", (edited["id"],)).fetchone()
        self.assertEqual(row["revision"], old_revision + 1)
        self.assertEqual(json.loads(row["document"])["title"], edited["title"])
        altered = copy.deepcopy(self.batches)
        altered[0][1][1]["title"] = "기존 배치 수정 금지"
        with self.assertRaisesRegex(ValueError, "new batch ID"):
            apply_publication(self.conn, self.publication, altered)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM research_report_revisions").fetchone()[0], before + 1)

    def test_missing_publication_report_rolls_back_reports_and_receipts(self):
        publication = copy.deepcopy(self.publication)
        publication["report_ids"].append("missing-report")
        with self.assertRaisesRegex(ValueError, "missing report"):
            apply_publication(self.conn, publication, self.batches)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM research_reports").fetchone()[0], 0)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM research_import_batches").fetchone()[0], 0)

    def test_table_contract_rejects_wrong_columns_and_missing_evidence(self):
        report = copy.deepcopy(self.batches[0][1][0])
        report["tables"][0]["rows"][0]["values"].append("extra")
        with self.assertRaisesRegex(ValueError, "match its columns"):
            validate_report(report)
        report = copy.deepcopy(self.batches[0][1][0])
        report["tables"][0]["rows"][0]["source_ids"] = []
        with self.assertRaisesRegex(ValueError, "needs a source"):
            validate_report(report)

    def test_all_selected_reports_render_and_citations_resolve(self):
        data = build_research_data(self.conn, [], [])
        self.assertEqual({report["id"] for report in data["reports"]}, self.reviewed_ids | {report["id"] for report in load_report_input()})
        featured = next(r for r in data["reports"] if r["id"] == data["featured_report_id"])
        with tempfile.TemporaryDirectory() as temp:
            root = build_briefing_preview(temp, {"items": [], "topics": []}, featured, data)
            home = (root / "index.html").read_text(encoding="utf-8")
            for report_id in self.publication["report_ids"]:
                self.assertIn(report_id + ".html", home)
                report = (root / (report_id + ".html")).read_text(encoding="utf-8")
                self.assertNotRegex(report, r"__[A-Z_]+__")
                for anchor in re.findall(r'href="#(ref-\d+)"', report):
                    self.assertIn('id="%s"' % anchor, report)
                for section in ("summary", "data", "result", "references"):
                    self.assertIn('id="%s"' % section, report)
            self.assertIn("178 %", (root / "upwork-ai-integration-demand.html").read_text(encoding="utf-8"))
            self.assertNotIn('role="img"', (root / "aws-partner-hackathon.html").read_text(encoding="utf-8"))
            featured["tables"][0]["rows"][0]["values"][0] = '<script>alert(1)</script>'
            build_briefing_preview(temp, {"items": [], "topics": []}, featured, data)
            report = (root / (featured["id"] + ".html")).read_text(encoding="utf-8")
            self.assertIn("&lt;script&gt;", report)
            self.assertNotIn("<script>", report)


if __name__ == "__main__":
    unittest.main()
