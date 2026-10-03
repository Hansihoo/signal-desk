import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


HAPPY_YOUTH_MONTHLY_INCOME_LIMIT_2026 = 4_576_036
HAPPY_YOUTH_ASSET_LIMIT_2026 = 251_000_000
YOUTH_SAFE_HOUSING_ASSET_LIMIT_2026 = 251_000_000
NATIONAL_RENT_SINGLE_MONTHLY_INCOME_LIMIT_2026 = 3_432_027


@dataclass
class HousingProfile:
    source_path: str = ""
    birth_date: date = None
    age: int = 0
    annual_income_krw: int = 0
    monthly_income_krw: int = 0
    total_assets_krw: int = 0
    unmarried: bool = False
    student: bool = False
    has_car: bool = None
    home_ownership_known: bool = False
    owns_home: bool = None


@dataclass
class EligibilityDecision:
    status: str
    label: str
    reasons: list

    @property
    def reason_text(self):
        return "; ".join(self.reasons)


def load_housing_profile(path=None, today=None):
    profile_path = path or os.environ.get("SIGNAL_DESK_PROFILE_PATH")
    if not profile_path:
        return None
    text = Path(profile_path).read_text(encoding="utf-8")
    return parse_housing_profile(text, source_path=str(profile_path), today=today)


def parse_housing_profile(text, source_path="", today=None):
    today = today or date.today()
    birth_date = _parse_birth_date(text)
    age = _age_on(birth_date, today) if birth_date else 0
    annual_income = _parse_annual_income(text)
    total_assets = _parse_assets(text)
    return HousingProfile(
        source_path=source_path,
        birth_date=birth_date,
        age=age,
        annual_income_krw=annual_income,
        monthly_income_krw=annual_income // 12 if annual_income else 0,
        total_assets_krw=total_assets,
        unmarried=_looks_unmarried(text),
        student=_looks_student(text),
        has_car=False if "차 없음" in text else None,
    )


def apply_profile_filter(items, profile, hide_ineligible=True):
    if not profile:
        return [dict(item) for item in items], {"excluded": 0, "kept": len(items), "decisions": {}}
    visible = []
    decisions = {}
    excluded = 0
    for item in items:
        decision = evaluate_housing_item(item, profile)
        decisions[item.get("id") or item.get("external_id")] = decision
        if hide_ineligible and decision.status == "excluded":
            excluded += 1
            continue
        copied = dict(item)
        copied["_profile_status"] = decision.status
        copied["_profile_label"] = decision.label
        copied["_profile_reason"] = decision.reason_text
        visible.append(copied)
    return visible, {"excluded": excluded, "kept": len(visible), "decisions": decisions}


def evaluate_housing_item(item, profile):
    text = _item_text(item)
    reasons = []

    if _is_only_target(text, ["고령자"], ["청년", "일반", "무순위"]):
        reasons.append("고령자 전용 공고로 보이며 프로필 연령과 불일치")
    if _is_only_target(text, ["신혼부부", "예비신혼", "한부모", "다자녀"], ["청년", "일반", "무순위"]):
        reasons.append("신혼/한부모/다자녀 전용 공고로 보이며 프로필 가구조건과 불일치")
    if _is_only_target(text, ["대학생", "취업준비생"], ["청년", "일반", "무순위"]):
        reasons.append("대학생/취업준비생 전용 공고로 보이며 프로필과 불일치")
    if "주거급여수급자" in text and "청년" not in text and "일반" not in text:
        reasons.append("주거급여수급자 전용 공고로 보이며 프로필 소득정보와 불일치")

    if "행복주택" in text:
        if profile.age and not (19 <= profile.age <= 39) and "청년" in text:
            reasons.append("행복주택 청년 연령 기준 범위 밖")
        if profile.monthly_income_krw > HAPPY_YOUTH_MONTHLY_INCOME_LIMIT_2026:
            reasons.append("프로필 연봉 기준 월소득이 행복주택 청년 1인가구 기준을 초과")
        if profile.total_assets_krw > HAPPY_YOUTH_ASSET_LIMIT_2026:
            reasons.append("프로필 추정 총자산이 행복주택 청년 자산기준을 초과")

    if "청년안심주택" in text or "역세권청년주택" in text or "역세권 청년주택" in text:
        if profile.age and not (19 <= profile.age <= 39):
            reasons.append("청년안심주택 청년 연령 기준 범위 밖")
        if profile.unmarried is False:
            reasons.append("청년안심주택 청년형 미혼 조건과 불일치")
        if profile.total_assets_krw > YOUTH_SAFE_HOUSING_ASSET_LIMIT_2026:
            reasons.append("프로필 추정 총자산이 청년안심주택 청년 자산기준을 초과")

    if "국민임대" in text and profile.monthly_income_krw > NATIONAL_RENT_SINGLE_MONTHLY_INCOME_LIMIT_2026:
        reasons.append("프로필 연봉 기준 월소득이 국민임대 1인가구 소득기준을 초과")

    if reasons:
        return EligibilityDecision("excluded", "프로필상 제외", reasons)

    checks = []
    if profile.owns_home is None:
        checks.append("무주택 여부")
    if profile.monthly_income_krw:
        checks.append("공고별 소득 산정")
    if profile.total_assets_krw:
        checks.append("공고별 자산 산정")
    if not checks:
        checks.append("공고문 세부조건")
    return EligibilityDecision("possible", "검토 가능", ["확인 필요: " + ", ".join(checks)])


def summarize_profile_filter(profile):
    if not profile:
        return ""
    parts = []
    if profile.age:
        parts.append("만 %d세" % profile.age)
    if profile.monthly_income_krw:
        parts.append("월소득 약 %s" % _money_short(profile.monthly_income_krw))
    if profile.total_assets_krw:
        parts.append("자산 약 %s" % _money_short(profile.total_assets_krw))
    return " · ".join(parts)


def _item_text(item):
    return " ".join(
        str(item.get(key) or "")
        for key in (
            "title",
            "agency",
            "category",
            "region",
            "summary",
            "eligibility",
            "detail_summary",
            "detail_text",
            "raw_text",
        )
    )


def _is_only_target(text, target_keywords, broad_keywords):
    return any(keyword in text for keyword in target_keywords) and not any(keyword in text for keyword in broad_keywords)


def _parse_birth_date(text):
    match = re.search(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", text)
    if not match:
        match = re.search(r"(\d{4})[-./]\s*(\d{1,2})[-./]\s*(\d{1,2})", text)
    if not match:
        return None
    return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))


def _parse_annual_income(text):
    match = re.search(r"연봉\s*:\s*약?\s*([0-9,]+)\s*만\s*원", text)
    if not match:
        return 0
    return int(match.group(1).replace(",", "")) * 10_000


def _parse_assets(text):
    total = 0
    in_asset_section = False
    for line in text.splitlines():
        if line.strip().startswith("### 자산"):
            in_asset_section = True
            continue
        if in_asset_section and line.strip().startswith("### "):
            break
        if not in_asset_section or "|" not in line:
            continue
        if "항목" in line or "---" in line or "부채" in line:
            continue
        total += _parse_money(line)
    return total


def _parse_money(value):
    value = value.replace(",", "")
    total = 0
    for amount, unit in re.findall(r"([0-9]+)\s*(억|만)", value):
        number = int(amount)
        if unit == "억":
            total += number * 100_000_000
        elif unit == "만":
            total += number * 10_000
    return total


def _looks_unmarried(text):
    return (
        "미혼" in text
        or "1인가구" in text
        or "혼자 살" in text
        or "인연을 찾" in text
        or ("결혼" in text and "배우자" not in text)
    )


def _looks_student(text):
    return "대학 재학" in text or ("학생" in text and "개발자" not in text)


def _age_on(birth_date, today):
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))


def _money_short(value):
    if value >= 100_000_000:
        whole = value / 100_000_000
        return "%.2f억" % whole
    if value >= 10_000:
        return "%d만원" % (value // 10_000)
    return "%d원" % value
