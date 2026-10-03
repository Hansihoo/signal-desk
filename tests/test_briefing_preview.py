import tempfile
import unittest
from pathlib import Path

from housing_watch.briefing_preview import build_briefing_preview, storage_scenarios


class BriefingPreviewTests(unittest.TestCase):
    def test_storage_units_and_report_values_agree(self):
        self.assertEqual([row[2] for row in storage_scenarios(years=1)], [26, 52, 520])
        self.assertEqual([row[2] for row in storage_scenarios(years=5)], [130, 260, 2600])
        self.assertEqual([row[2] for row in storage_scenarios()], [260, 520, 5200])
        with tempfile.TemporaryDirectory() as temp:
            root = build_briefing_preview(temp, {"items": [], "topics": []})
            report = (root / "report.html").read_text(encoding="utf-8")
            self.assertIn("260 MB", report)
            self.assertIn("520 MB", report)
            self.assertIn("5.2 GB", report)
            self.assertIn("가정 계산 · 실측 아님", report)
            self.assertIn("단일 보관 가정과 다릅니다", report)
            self.assertNotIn("__CHART_ROWS__", report)

    def test_preview_escapes_source_titles_and_omits_unsafe_records(self):
        snapshot = {"topics": [{"id": "ai", "name": "AI 개발"}], "items": [
            {"id": "safe", "topic_id": "ai", "title": '<script>alert("x")</script>',
             "url": "https://example.org/source", "category": 'A&B', "published_at": "2026-10-03"},
            {"id": "unsafe", "topic_id": "ai", "title": "Unsafe record",
             "url": "javascript:alert(1)", "published_at": "2026-10-04"}]}
        with tempfile.TemporaryDirectory() as temp:
            root = build_briefing_preview(temp, snapshot)
            home = (root / "index.html").read_text(encoding="utf-8")
            self.assertNotIn('<script>', home)
            self.assertNotIn("Unsafe record", home)
            self.assertIn('&lt;script&gt;', home)
            self.assertIn("section=A%26B&amp;report=safe", home)
            self.assertTrue((root / "briefing.css").is_file())


if __name__ == "__main__":
    unittest.main()
