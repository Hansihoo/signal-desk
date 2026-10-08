import copy
import io
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from housing_watch.business_private import (
    PROJECT_ROOT, connect_private, import_private, private_root, render_private, validate_input,
)
from housing_watch.cli import main
from housing_watch.cloud_state import create_archive
from housing_watch.research_data import load_report_input


class BusinessPrivateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "private"
        self.conn = connect_private(self.root)
        self.addCleanup(self.conn.close)
        self.document = {"schema_version": 1, "records": [{
            "id": "pilot", "category": "영업 기회", "title": "private sentinel <script>",
            "status": "확인 필요", "checked_on": "2026-10-08", "next_action": "고객 조건 검토",
            "customer": "private customer sentinel", "pricing": "internal price sentinel",
        }]}

    def test_revisions_preserve_original_and_do_not_repeat_unchanged(self):
        self.assertEqual(import_private(self.conn, self.document)["inserted"], 1)
        self.assertEqual(import_private(self.conn, self.document)["unchanged"], 1)
        changed = copy.deepcopy(self.document)
        changed["records"][0]["status"] = "검토 중"
        self.assertEqual(import_private(self.conn, changed)["updated"], 1)
        original = self.conn.execute("SELECT document FROM business_revisions WHERE revision=1").fetchone()[0]
        self.assertEqual(json.loads(original)["status"], "확인 필요")

    def test_unsafe_location_and_public_connection_are_rejected_before_mutation(self):
        for root in (PROJECT_ROOT, PROJECT_ROOT / "data/private", PROJECT_ROOT / "site/private"):
            with self.assertRaises(ValueError):
                private_root(root)
        other_repo = Path(self.temp.name) / "git-work"
        (other_repo / ".git").mkdir(parents=True)
        with self.assertRaises(ValueError):
            private_root(other_repo / "hidden")
        public = sqlite3.connect(Path(self.temp.name) / "housing_watch.sqlite")
        try:
            with self.assertRaises(ValueError):
                import_private(public, self.document)
            self.assertFalse(public.execute("SELECT name FROM sqlite_master").fetchall())
        finally:
            public.close()

    def test_invalid_batch_is_atomic_and_private_input_is_not_a_public_report(self):
        invalid = copy.deepcopy(self.document)
        invalid["records"].append(dict(invalid["records"][0], id="invalid", status="unknown"))
        with self.assertRaises(ValueError):
            import_private(self.conn, invalid)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM business_records").fetchone()[0], 0)
        source = self.root / "input.json"
        source.write_text(json.dumps(self.document), encoding="utf-8")
        with self.assertRaises(ValueError):
            load_report_input(source)

    def test_private_cli_does_not_open_public_config_or_database(self):
        with patch("housing_watch.cli.connect", side_effect=AssertionError("public DB opened")), \
             patch("housing_watch.cli.load_config", side_effect=AssertionError("public config opened")), \
             redirect_stdout(io.StringIO()):
            self.assertEqual(main(["business-private", "--root", str(self.root)]), 0)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(["business-private", "--root", str(PROJECT_ROOT / "site")]), 1)

    def test_private_render_escapes_content_and_rejects_cross_workspace_output(self):
        import_private(self.conn, self.document)
        content = render_private(self.conn, self.root).read_text(encoding="utf-8")
        self.assertIn("&lt;script&gt;", content)
        self.assertNotIn("<script>private", content)
        self.assertIn("private customer sentinel", content)
        with self.assertRaises(ValueError):
            render_private(self.conn, Path(self.temp.name) / "wrong")

    def test_public_backup_refuses_private_tables_even_if_empty(self):
        public_root = Path(self.temp.name) / "public"
        (public_root / "data").mkdir(parents=True)
        (public_root / "site/archive").mkdir(parents=True)
        (public_root / "site/archive/index.json").write_text("[]")
        with closing(sqlite3.connect(public_root / "data/housing_watch.sqlite")) as conn:
            conn.execute("CREATE TABLE business_records (id TEXT)")
            conn.commit()
        with self.assertRaisesRegex(ValueError, "private business"):
            create_archive(public_root, Path(self.temp.name) / "public.tar.gz")
