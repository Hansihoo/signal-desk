import os
import tempfile
import unittest
from pathlib import Path

from housing_watch.db import connect, init_db, upsert_items
from housing_watch.render import render_brief_html
from housing_watch.review import png_dimensions, review_project


class RenderReviewTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")
        init_db(self.conn)
        upsert_items(
            self.conn,
            [
                {
                    "source_id": "test",
                    "external_id": "1",
                    "title": "2026년 서울 행복주택 입주자 모집공고",
                    "url": "https://example.com/notice/1",
                    "agency": "SH",
                    "category": "행복주택",
                    "region": "서울",
                    "status": "모집중",
                    "published_at": "2026-06-18",
                    "deadline_at": "2026-07-01",
                    "summary": "SH 서울 행복주택 모집중",
                    "raw_text": "서울 행복주택 입주자 모집",
                    "content_hash": "abc",
                    "collected_at": "2026-06-18T00:00:00Z",
                }
            ],
            {"keywords": ["행복주택"], "regions": ["서울"], "preferred_statuses": ["모집중"]},
        )

    def test_brief_html_is_mobile_concise(self):
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "brief.html"
            render_brief_html(self.conn, str(html_path), item_limit=5, max_width=390)
            text = html_path.read_text(encoding="utf-8")
            self.assertIn('name="viewport"', text)
            self.assertIn("max-width: 390px", text)
            self.assertLessEqual(text.count('class="notice"'), 5)
            self.assertIn("overflow-wrap: anywhere", text)

    def test_review_passes_with_valid_png_width(self):
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "brief.html"
            png_path = Path(tmp) / "brief.png"
            render_brief_html(self.conn, str(html_path), item_limit=5, max_width=390)
            png_path.write_bytes(_minimal_png(390, 500))
            result = review_project(self.conn, str(html_path), str(png_path), max_width=390)
            self.assertTrue(result["ok"])

    def test_png_dimensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            png_path = Path(tmp) / "test.png"
            png_path.write_bytes(_minimal_png(320, 480))
            self.assertEqual(png_dimensions(png_path), (320, 480))


def _minimal_png(width, height):
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr_length = (13).to_bytes(4, "big")
    ihdr_type = b"IHDR"
    ihdr_data = width.to_bytes(4, "big") + height.to_bytes(4, "big") + b"\x08\x02\x00\x00\x00"
    fake_crc = b"\x00\x00\x00\x00"
    return signature + ihdr_length + ihdr_type + ihdr_data + fake_crc


if __name__ == "__main__":
    unittest.main()

