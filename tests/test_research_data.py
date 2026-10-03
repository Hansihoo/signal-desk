import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

from housing_watch.briefing_preview import build_briefing_preview
from housing_watch.cli import main
from housing_watch.db import connect, init_db, upsert_news_items
from housing_watch.public_site import build_public_site, public_library
from housing_watch.research_data import (
    build_research_data, ensure_example_report, import_reports, load_report_input,
    validate_report, write_research_data,
)
from housing_watch.research_topics import load_topics


class ResearchDataTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        init_db(self.conn)
        self.report = load_report_input()[0]

    def tearDown(self):
        self.conn.close()

    def test_round_trip_and_changed_only_revision_history(self):
        self.assertEqual(import_reports(self.conn, [self.report])["inserted"], 1)
        self.assertEqual(import_reports(self.conn, [copy.deepcopy(self.report)])["unchanged"], 1)
        changed = copy.deepcopy(self.report)
        changed["title"] = "수정된 보고서"
        self.assertEqual(import_reports(self.conn, [changed])["updated"], 1)
        ensure_example_report(self.conn)
        document = build_research_data(self.conn, [], load_topics())
        self.assertEqual(document["reports"], [changed])
        self.assertEqual(document["report_versions"][0]["revision"], 2)
        old = self.conn.execute("SELECT document FROM research_report_revisions WHERE revision=1").fetchone()
        self.assertEqual(json.loads(old["document"]), self.report)
        with tempfile.TemporaryDirectory() as temp:
            output = write_research_data(Path(temp) / "data.json", document)
            self.assertEqual(load_report_input(output), [changed])

    def test_invalid_batch_and_duplicate_ids_do_not_mutate_existing_reports(self):
        import_reports(self.conn, [self.report])
        changed = copy.deepcopy(self.report)
        changed["title"] = "Must not persist"
        invalid = copy.deepcopy(self.report)
        invalid["id"] = "other"
        invalid["summary"][0]["source_ids"] = ["missing"]
        with self.assertRaises(ValueError):
            import_reports(self.conn, [changed, invalid])
        with self.assertRaises(ValueError):
            import_reports(self.conn, [changed, changed])
        document = build_research_data(self.conn, [], [])
        self.assertEqual(document["reports"][0]["title"], self.report["title"])
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM research_report_revisions").fetchone()[0], 1)

    def test_rejects_bad_numbers_urls_and_presentation_fields(self):
        mutations = [
            lambda r: r["datasets"][0]["rows"][0].update(value=float("nan")),
            lambda r: r["datasets"][0]["rows"][0].update(value=-1),
            lambda r: r["datasets"][0]["rows"][0].update(value=True),
            lambda r: r["references"][0].update(url="javascript:alert(1)"),
            lambda r: r["references"][0].update(url="https://user:secret@example.com"),
            lambda r: r.update(css="color: red"),
            lambda r: r["summary"][0].update(source_ids=[]),
            lambda r: r["datasets"][0].update(assumptions=[]),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                report = copy.deepcopy(self.report)
                mutate(report)
                with self.assertRaises(ValueError):
                    validate_report(report)

    def test_database_failure_rolls_back_all_reports_and_revisions(self):
        import_reports(self.conn, [self.report])
        self.conn.execute("CREATE TRIGGER reject_second BEFORE INSERT ON research_reports WHEN NEW.id='second' BEGIN SELECT RAISE(ABORT, 'test failure'); END")
        changed = copy.deepcopy(self.report)
        changed["title"] = "Must roll back"
        second = copy.deepcopy(self.report)
        second["id"] = "second"
        import sqlite3
        with self.assertRaises(sqlite3.IntegrityError):
            import_reports(self.conn, [changed, second])
        current = self.conn.execute("SELECT document, revision FROM research_reports").fetchall()
        self.assertEqual(len(current), 1)
        self.assertEqual(current[0]["revision"], 1)
        self.assertEqual(json.loads(current[0]["document"]), self.report)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM research_report_revisions").fetchone()[0], 1)

    def test_data_only_cli_refreshes_records_without_touching_web_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config_path = root / "sources.json"
            config_path.write_text(json.dumps({"project": {"database_path": str(root / "test.sqlite")}, "sources": []}), encoding="utf-8")
            web = root / "site"
            web.mkdir()
            for name in ("index.html", "briefing.css", "report.html"):
                (web / name).write_text("existing design", encoding="utf-8")
            before = {path.name: path.read_bytes() for path in web.iterdir()}
            output = root / "research.json"

            def collect(conn, config, topics):
                upsert_news_items(conn, [{"source_id": "ai_test", "external_id": "new", "title": "Collected source",
                    "url": "https://example.org/new", "summary_ko": "Source excerpt"}])
                conn.commit()
                return [{"source": "test", "topic_id": "ai", "ok": True, "count": 1}]

            with patch("housing_watch.cli.collect_public_data", side_effect=collect) as collector, \
                    patch("housing_watch.cli.build_public_site") as renderer, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                status = main(["--config", str(config_path), "research-data", "--collect", "--output", str(output)])
            self.assertEqual(status, 0)
            collector.assert_called_once()
            renderer.assert_not_called()
            self.assertEqual(before, {path.name: path.read_bytes() for path in web.iterdir()})
            document = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(document["source_records"][0]["title"], "Collected source")
            self.assertEqual(document["health"][0]["count"], 1)
            self.assertEqual(len(document["reports"]), 1)
            self.assertEqual(set(path.name for path in root.iterdir()), {"sources.json", "test.sqlite", "site", "research.json"})

    def test_export_excludes_private_jobs_and_layout(self):
        self.conn.execute("INSERT INTO job_items(source_id, external_id, company_name, posting_title, url, first_seen_at, last_seen_at) VALUES ('private','1','PRIVATE','SECRET','https://example.org/private','now','now')")
        topics = load_topics()
        document = build_research_data(self.conn, public_library(self.conn, topics), topics)
        encoded = json.dumps(document, ensure_ascii=False)
        self.assertNotIn("SECRET", encoded)
        self.assertNotIn("PRIVATE", encoded)
        self.assertNotIn("detail_page", encoded)
        self.assertNotIn("class=", encoded)
        self.assertNotIn("style=", encoded)
        self.assertEqual(document["source_records"], [])

    def test_same_report_data_controls_html_text_numbers_threshold_and_escaping(self):
        report = copy.deepcopy(self.report)
        report["title"] = '<script>__STYLE_VERSION__</script>'
        dataset = report["datasets"][0]
        dataset["unit"] = "건"
        dataset["rows"] = [{"label": "<img src=x>", "value": 25, "source_ids": []}, {"label": "B", "value": 100, "source_ids": []}]
        dataset["threshold"]["value"] = 50
        with tempfile.TemporaryDirectory() as temp:
            root = build_briefing_preview(temp, {"items": [], "topics": []}, report)
            html = (root / "report.html").read_text(encoding="utf-8")
            self.assertNotIn("<script>", html)
            self.assertNotIn("<img src=x>", html)
            self.assertIn("&lt;script&gt;__STYLE_VERSION__&lt;/script&gt;", html)
            self.assertIn('style="width:25.0%"', html)
            self.assertIn("--threshold-position:50.000000%", html)
            self.assertIn("25 건", html)
            self.assertNotIn("5.2 GB</span>", html)
            self.assertIn("left:var(--threshold-position)", (root / "briefing.css").read_text(encoding="utf-8"))

    def test_publish_uses_current_db_report_and_exports_identical_content(self):
        upsert_news_items(self.conn, [{"source_id": "ai_test", "external_id": "one", "title": "Source", "url": "https://example.org/one"}])
        changed = copy.deepcopy(self.report)
        changed["title"] = "DB에 저장된 제목"
        import_reports(self.conn, [changed])
        with tempfile.TemporaryDirectory() as temp:
            build_public_site(self.conn, temp)
            data = json.loads((Path(temp) / "research-data.json").read_text(encoding="utf-8"))
            html = (Path(temp) / "preview/report.html").read_text(encoding="utf-8")
            self.assertEqual(data["reports"], [changed])
            self.assertIn("DB에 저장된 제목", html)
            self.assertNotIn(self.report["title"], html)


if __name__ == "__main__":
    unittest.main()
