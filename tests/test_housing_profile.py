import unittest
from datetime import date

from housing_watch.housing_profile import apply_profile_filter, evaluate_housing_item, parse_housing_profile


PROFILE_TEXT = """
# Profile

- 생년월일: 1988-11-20
- 가구: 미혼 1인가구
- 차량: 차 없음
- 연봉: 약 6,400 만 원

### 자산

| 항목 | 금액 |
| --- | --- |
| 주식 | 4,000만원 |
| 청약통장 | 1,300만원 |
| 현금 | 200만원 |
| 전세보증금 | 2억원 |
| 부채 | 없음 |
"""


class HousingProfileTests(unittest.TestCase):
    def test_parse_profile_extracts_housing_filter_inputs(self):
        profile = parse_housing_profile(PROFILE_TEXT, today=date(2026, 6, 20))

        self.assertEqual(profile.age, 37)
        self.assertEqual(profile.annual_income_krw, 64_000_000)
        self.assertEqual(profile.monthly_income_krw, 5_333_333)
        self.assertEqual(profile.total_assets_krw, 255_000_000)
        self.assertTrue(profile.unmarried)
        self.assertFalse(profile.has_car)

    def test_happy_housing_is_excluded_when_income_and_assets_exceed_youth_limits(self):
        profile = parse_housing_profile(PROFILE_TEXT, today=date(2026, 6, 20))
        item = {
            "title": "서울 행복주택 청년 입주자 모집",
            "category": "행복주택",
            "region": "서울",
            "eligibility": "청년",
        }

        decision = evaluate_housing_item(item, profile)

        self.assertEqual(decision.status, "excluded")
        self.assertIn("행복주택 청년 1인가구 기준", decision.reason_text)

    def test_national_rental_is_excluded_when_income_exceeds_single_household_limit(self):
        profile = parse_housing_profile(PROFILE_TEXT, today=date(2026, 6, 20))
        item = {
            "title": "경기 국민임대 예비입주자 모집",
            "category": "국민임대",
            "region": "경기",
        }

        decision = evaluate_housing_item(item, profile)

        self.assertEqual(decision.status, "excluded")
        self.assertIn("국민임대 1인가구 소득기준", decision.reason_text)

    def test_generic_notice_stays_visible_for_manual_review(self):
        profile = parse_housing_profile(PROFILE_TEXT, today=date(2026, 6, 20))
        items = [
            {"id": 1, "title": "서울 일반분양 무순위 청약", "category": "민영주택", "region": "서울"},
            {"id": 2, "title": "서울 행복주택 청년 모집", "category": "행복주택", "region": "서울"},
        ]

        visible, summary = apply_profile_filter(items, profile, hide_ineligible=True)

        self.assertEqual([item["id"] for item in visible], [1])
        self.assertEqual(summary["excluded"], 1)
        self.assertEqual(visible[0]["_profile_label"], "검토 가능")


if __name__ == "__main__":
    unittest.main()
