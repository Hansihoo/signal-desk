import unittest

from housing_watch.details import enrich_item_from_detail


class DetailExtractionTests(unittest.TestCase):
    def test_lh_detail_fields(self):
        item = {
            "source_id": "test",
            "external_id": "test:1",
            "title": "화성시 행복주택 입주자격완화 예비입주자 모집",
            "summary": "LH 경기도 행복주택 공고중",
            "raw_text": "화성시 행복주택",
        }
        html = """
        <html><body>
        공고내용 공급정보 화성시 행복주택
        소재지 : 경기도 화성시 동탄대로24길 49
        전용면적(㎡) : 16.93~36.77
        총 세대수 : 182
        난방방식 : 지역난방
        입주예정월 : 2027.02
        신청자격 : 청년, 신혼부부, 고령자
        인터넷 접수 : 2026. 6. 25. 10:00 ~ 6. 27. 17:00
        </body></html>
        """
        enrich_item_from_detail(item, html)
        self.assertEqual(item["address"], "경기도 화성시 동탄대로24길 49")
        self.assertEqual(item["area_range_m2"], "16.93~36.77㎡")
        self.assertEqual(item["area_range_pyeong"], "5.1~11.1평")
        self.assertEqual(item["supply_units"], "182 세대")
        self.assertIn("청년", item["eligibility"])
        self.assertIn("접수", item["detail_summary"])


if __name__ == "__main__":
    unittest.main()

