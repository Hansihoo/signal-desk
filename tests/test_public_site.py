import io
import json
import os
import re
import tarfile
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlsplit

from housing_watch.cloud_state import create_archive, latest_asset, restore_archive
from housing_watch.db import connect, init_db, upsert_news_items
from housing_watch.public_site import build_public_site, collect_public_data


class PublicSiteTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        init_db(self.conn)
        self.add_news("old", "2026-09-01", "Older research")

    def tearDown(self):
        self.conn.close()

    def add_news(self, identifier, date, title):
        upsert_news_items(self.conn, [{"source_id": "ai_test", "external_id": identifier, "title": title,
            "url": "https://example.com/" + identifier, "published_at": date,
            "summary_ko": "Public summary", "raw_payload": json.dumps({"detail": "Source excerpt"})}])

    def test_daily_snapshot_is_preserved_and_new_days_accumulate(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch("housing_watch.public_site.now_kst", return_value=datetime(2026, 10, 3, tzinfo=timezone.utc)):
                build_public_site(self.conn, temp)
                first = (Path(temp) / "archive/2026-10-03/briefing.json").read_bytes()
                self.add_news("new", "2026-10-03", "New evidence")
                build_public_site(self.conn, temp)
                self.assertEqual(first, (Path(temp) / "archive/2026-10-03/briefing.json").read_bytes())
            with patch("housing_watch.public_site.now_kst", return_value=datetime(2026, 10, 4, tzinfo=timezone.utc)):
                result = build_public_site(self.conn, temp)
            self.assertEqual(result["archives"], 2)
            self.assertEqual(len(json.loads((Path(temp) / "library.json").read_text(encoding="utf-8"))), 2)
            self.assertNotIn("New evidence", (Path(temp) / "archive/2026-10-03/index.html").read_text(encoding="utf-8"))

    def test_public_export_excludes_private_jobs_and_script_injection(self):
        self.conn.execute("INSERT INTO job_items(source_id,external_id,company_name,posting_title,url,first_seen_at,last_seen_at) VALUES ('private','1','Private company','Secret salary','https://private.example','now','now')")
        self.add_news("attack", "2026-10-03", "</script><script>alert(1)</script>")
        self.add_news("url", "2026-10-03", "Unsafe link")
        self.conn.execute("UPDATE news_items SET url='javascript:alert(1)' WHERE external_id='url'")
        with tempfile.TemporaryDirectory() as temp:
            build_public_site(self.conn, temp)
            content = (Path(temp) / "index.html").read_text(encoding="utf-8")
            library = (Path(temp) / "library.json").read_text(encoding="utf-8")
            self.assertNotIn("</script><script>alert", content)
            self.assertNotIn("Secret salary", library)
            self.assertNotIn("javascript:", library)

    def test_collection_failure_retains_existing_data(self):
        from housing_watch.ai_news import AINewsFetchError
        from housing_watch.news import NewsFetchError
        with patch("housing_watch.public_site.collect_ai_news", side_effect=AINewsFetchError("offline")), patch("housing_watch.public_site.collect_weekly_news", side_effect=NewsFetchError("offline")):
            health = collect_public_data(self.conn, {"sources": []})
        self.assertTrue(all(not item["ok"] for item in health))
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(build_public_site(self.conn, temp, health)["items"], 1)

    def test_shared_assets_resolve_from_main_topic_and_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            build_public_site(self.conn, temp)
            root = Path(temp)
            pages = [root / "index.html", root / "research/ai/index.html", *root.glob("archive/*/index.html")]
            for page in pages:
                content = page.read_text(encoding="utf-8")
                references = re.findall(r'(?:href|src)="([^"]+public_site\.(?:css|js)\?v=[^"]+)"', content)
                # The root references have no path prefix.
                references += re.findall(r'(?:href|src)="(public_site\.(?:css|js)\?v=[^"]+)"', content)
                self.assertEqual(len(references), 2, str(page))
                for reference in references:
                    asset = (page.parent / urlsplit(reference).path).resolve()
                    self.assertEqual(asset.parent, root.resolve())
                    self.assertTrue(asset.is_file(), str(asset))
                    self.assertIn("v=", reference)
                self.assertNotIn("__ASSET_", content)
                self.assertIn('id="briefing-data" type="application/json"', content)

    def test_public_render_does_not_read_private_profile_environment(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, {"SIGNAL_DESK_PROFILE_PATH": "private-do-not-read.md"}), patch("housing_watch.render.load_housing_profile") as loader:
            build_public_site(self.conn, temp)
            loader.assert_not_called()

    def test_backup_restores_database_and_old_briefings(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "source"
            conn = connect(root / "data/housing_watch.sqlite")
            init_db(conn)
            self.conn.backup(conn)
            build_public_site(conn, root / "site")
            batch_count = conn.execute("SELECT COUNT(*) FROM research_import_batches").fetchone()[0]
            revision_count = conn.execute("SELECT COUNT(*) FROM research_report_revisions").fetchone()[0]
            conn.close()
            archive = Path(temp) / "state.tar.gz"
            create_archive(root, archive)
            restored = Path(temp) / "restored"
            restore_archive(archive, restored)
            conn = connect(restored / "data/housing_watch.sqlite")
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM news_items").fetchone()[0], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM research_import_batches").fetchone()[0], batch_count)
            report_count = conn.execute("SELECT COUNT(*) FROM research_reports").fetchone()[0]
            self.assertEqual(report_count, 11)
            self.assertEqual(build_public_site(conn, restored / "site")["archives"], 1)
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM research_report_revisions").fetchone()[0], revision_count)
            conn.close()

    def test_restore_rejects_traversal_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            archive = Path(temp) / "bad.tar.gz"
            with tarfile.open(str(archive), "w:gz") as output:
                member = tarfile.TarInfo("site/../../outside.txt")
                member.size = 4
                output.addfile(member, io.BytesIO(b"test"))
            with self.assertRaises(ValueError):
                restore_archive(archive, Path(temp) / "destination")
            self.assertFalse((Path(temp) / "outside.txt").exists())

    def test_restore_selects_latest_snapshot_across_months(self):
        records = [{"tag_name": "signal-desk-data-2026-09", "assets": [{"name": "state-old.tar.gz", "id": 1, "created_at": "2026-09-30"}]},
                   {"tag_name": "signal-desk-data-2026-10", "assets": [{"name": "state-new.tar.gz", "id": 2, "created_at": "2026-10-03"}]}]
        self.assertEqual(latest_asset(records)[3], "state-new.tar.gz")
