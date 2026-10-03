import hashlib
import html
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path

from .db import record_snapshot, upsert_news_items
from .timeutil import compact_timestamp, iso_utc


GDELT_DOC_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
GOOGLE_NEWS_TOP_KO_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
GOOGLE_NEWS_WORLD_KO_URL = "https://news.google.com/rss/headlines/section/topic/WORLD?hl=ko&gl=KR&ceid=KR:ko"
USER_AGENT = "SignalDesk/0.1 (+local personal briefing)"


class NewsFetchError(Exception):
    pass


def collect_weekly_news(
    conn,
    source="auto",
    limit=12,
    raw_dir="data/raw/news",
    translate_url=None,
    translate_key=None,
):
    failures = []
    result = None
    if source in ("auto", "gdelt"):
        try:
            result = fetch_gdelt_news(limit=limit, raw_dir=raw_dir, translate_url=translate_url, translate_key=translate_key)
        except (NewsFetchError, OSError, ValueError, urllib.error.URLError) as exc:
            failures.append("gdelt: %s" % exc)
            if source == "gdelt":
                raise

    if not result and source in ("auto", "google-news"):
        result = fetch_google_news_ko(limit=limit, raw_dir=raw_dir, translate_url=translate_url, translate_key=translate_key)

    if not result:
        raise NewsFetchError("no news source returned items")

    stats = upsert_news_items(conn, result["items"], source_ids=["gdelt_weekly", "google_news_top_ko", "google_news_world_ko"])
    record_snapshot(conn, result["source_id"], result["raw_path"], len(result["items"]))
    conn.commit()
    return {
        "source_id": result["source_id"],
        "raw_path": result["raw_path"],
        "fetched": len(result["items"]),
        "inserted": stats["inserted"],
        "updated": stats["updated"],
        "deduped": stats.get("deduped", 0),
        "failures": failures,
    }


def fetch_gdelt_news(limit=12, raw_dir="data/raw/news", translate_url=None, translate_key=None):
    query = " OR ".join(
        [
            "economy",
            "politics",
            "election",
            "market",
            "technology",
            "entertainment",
            "war",
            "health",
            "climate",
        ]
    )
    params = {
        "query": query,
        "mode": "artlist",
        "format": "json",
        "timespan": "1w",
        "maxrecords": str(max(limit * 3, 30)),
        "sort": "HybridRel",
    }
    url = GDELT_DOC_URL + "?" + urllib.parse.urlencode(params)
    data = _read_url(url)
    raw_path = _write_raw(raw_dir, "gdelt_weekly", data, ".json")
    try:
        payload = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise NewsFetchError("invalid GDELT JSON: %s" % exc)

    articles = payload.get("articles") or []
    if not articles:
        raise NewsFetchError("GDELT returned no articles")

    items = []
    seen = set()
    for index, article in enumerate(articles):
        title = article.get("title") or ""
        url = article.get("url") or ""
        if not title or not url:
            continue
        title_ko = _translate_if_needed(title, translate_url, translate_key)
        key = _dedupe_key(title_ko or title)
        if key in seen:
            continue
        seen.add(key)
        source_name = article.get("domain") or _domain(url)
        category = categorize_news("%s %s" % (title, title_ko))
        items.append(
            {
                "source_id": "gdelt_weekly",
                "external_id": _hash(url or title),
                "title": title,
                "title_ko": title_ko,
                "url": url,
                "source_name": source_name,
                "source_url": "https://%s" % source_name if source_name else "",
                "category": category,
                "language": article.get("language") or "",
                "country": article.get("sourcecountry") or "",
                "published_at": _parse_gdelt_seen_date(article.get("seendate") or ""),
                "summary_ko": summarize_news(title_ko, category, source_name, "GDELT"),
                "score": max(1, 120 - index * 2),
                "raw_payload": json.dumps(article, ensure_ascii=False, sort_keys=True),
                "content_hash": _hash(json.dumps(article, ensure_ascii=False, sort_keys=True)),
                "collected_at": iso_utc(),
            }
        )
        if len(items) >= limit:
            break

    if not items:
        raise NewsFetchError("GDELT articles could not be normalized")
    return {"source_id": "gdelt_weekly", "raw_path": raw_path, "items": items}


def fetch_google_news_ko(limit=12, raw_dir="data/raw/news", translate_url=None, translate_key=None):
    feeds = [
        ("top", "google_news_top_ko", GOOGLE_NEWS_TOP_KO_URL, None, 120),
        ("world", "google_news_world_ko", GOOGLE_NEWS_WORLD_KO_URL, "국제", 119),
    ]
    items = []
    raw_feeds = []
    for name, source_id, url, category_hint, score_base in feeds:
        data = _read_url(url)
        raw_feeds.append({"name": name, "source_id": source_id, "url": url, "body": data.decode("utf-8", "replace")})
        items.extend(
            parse_google_news_rss(
                data,
                limit=limit,
                translate_url=translate_url,
                translate_key=translate_key,
                source_id=source_id,
                category_hint=category_hint,
                score_base=score_base,
            )
        )
    raw_data = json.dumps({"feeds": raw_feeds}, ensure_ascii=False, sort_keys=True).encode("utf-8")
    raw_path = _write_raw(raw_dir, "google_news_ko_bundle", raw_data, ".json")
    items = _dedupe_items(items)[: max(limit * 2, limit)]
    if not items:
        raise NewsFetchError("Google News RSS returned no items")
    return {"source_id": "google_news_ko_bundle", "raw_path": raw_path, "items": items}


def parse_google_news_rss(
    data,
    limit=12,
    translate_url=None,
    translate_key=None,
    source_id="google_news_top_ko",
    category_hint=None,
    score_base=120,
):
    root = ET.fromstring(data)
    items = []
    seen = set()
    for index, node in enumerate(root.findall("./channel/item")):
        raw_title = html.unescape(node.findtext("title") or "").strip()
        link = (node.findtext("link") or "").strip()
        guid = (node.findtext("guid") or link or raw_title).strip()
        source_node = node.find("source")
        source_name = (source_node.text or "").strip() if source_node is not None else _source_from_title(raw_title)
        source_url = source_node.attrib.get("url", "") if source_node is not None else ""
        title = _strip_source_suffix(raw_title, source_name)
        if not title or not link:
            continue
        title_ko = _translate_if_needed(title, translate_url, translate_key)
        key = _dedupe_key(title_ko or title)
        if key in seen:
            continue
        seen.add(key)
        category = category_hint or categorize_news(title_ko or title)
        description_text = _rss_description_text(node.findtext("description") or "")
        items.append(
            {
                "source_id": source_id,
                "external_id": _hash(title_ko or title),
                "title": title,
                "title_ko": title_ko,
                "url": link,
                "source_name": source_name,
                "source_url": source_url,
                "category": category,
                "language": "Korean",
                "country": "KR",
                "published_at": _parse_rss_date(node.findtext("pubDate") or ""),
                "summary_ko": summarize_news(title_ko, category, source_name, "Google News", description_text),
                "score": max(1, score_base - index * 3),
                "raw_payload": ET.tostring(node, encoding="unicode"),
                "content_hash": _hash(raw_title + link),
                "collected_at": iso_utc(),
            }
        )
        if len(items) >= limit:
            break
    return items


def categorize_news(text):
    value = text.lower()
    categories = [
        ("정치", ["대통령", "국회", "정부", "정당", "선거", "장관", "외교", "국정", "politic", "election", "minister"]),
        ("경제", ["경제", "증시", "금리", "환율", "시장", "주식", "부동산", "기업", "원유", "관세", "economy", "market", "stock", "oil"]),
        ("국제", ["미국", "중국", "일본", "러시아", "우크라", "이란", "이스라엘", "유럽", "war", "trump", "china", "iran"]),
        ("사회", ["사회", "경찰", "검찰", "법원", "사고", "폭염", "비", "재난", "교육", "health", "court"]),
        ("기술", ["ai", "인공지능", "반도체", "기술", "테크", "챗gpt", "openai", "chip", "technology"]),
        ("연예", ["연예", "배우", "가수", "아이돌", "드라마", "영화", "방송", "entertainment", "music", "film"]),
        ("스포츠", ["스포츠", "축구", "야구", "농구", "월드컵", "sport", "football", "baseball"]),
    ]
    for category, keywords in categories:
        if any(keyword in value for keyword in keywords):
            return category
    return "종합"


def summarize_news(title_ko, category, source_name, channel, description_text=""):
    headline = _clean_headline(title_ko or description_text or "")
    if not headline:
        return "%s 분야의 주요 뉴스 후보입니다. 세부 내용과 후속 보도를 함께 확인해야 합니다." % category
    detail = _category_followup(category, headline)
    return "핵심은 %s 입니다. %s" % (headline, detail)


def _category_followup(category, headline):
    if category == "정치":
        return "정책 추진력, 여야 반응, 국회 일정이나 지지율 변화로 이어지는지 확인하면 좋습니다."
    if category == "경제":
        return "시장 가격, 기업 비용, 투자심리나 소비자 부담에 어떤 영향을 주는지 보는 소식입니다."
    if category == "국제":
        return "외교 관계, 에너지·금융시장, 국내 정책 대응으로 번질 수 있는지 후속 흐름을 봐야 합니다."
    if category == "사회":
        if any(keyword in headline for keyword in ["비", "폭염", "더위", "날씨", "태풍", "호우"]):
            return "생활 안전, 교통, 출퇴근과 재난 대응에 직접 영향을 줄 수 있어 지역별 예보를 같이 봐야 합니다."
        return "생활 영향, 안전 대응, 수사·행정 조치가 뒤따르는지 확인해야 하는 사회 이슈입니다."
    if category == "기술":
        return "기업 전략, 서비스 변화, 반도체·AI 투자 흐름과 연결될 수 있는 기술 이슈입니다."
    if category == "연예":
        return "작품·인물·소속사 이슈가 대중 반응이나 업계 일정으로 이어지는지 보면 좋습니다."
    if category == "스포츠":
        return "경기 결과, 순위, 선수 이동이나 다음 일정에 영향을 줄 수 있는 소식입니다."
    return "이번 주 상위로 노출된 종합 이슈라서 관련 후속 기사와 실제 영향 범위를 확인하면 좋습니다."


def _translate_if_needed(text, translate_url=None, translate_key=None):
    if not text:
        return ""
    if _has_hangul(text):
        return text
    endpoint = translate_url or os.environ.get("SIGNAL_DESK_TRANSLATE_URL")
    api_key = translate_key or os.environ.get("SIGNAL_DESK_TRANSLATE_KEY")
    if not endpoint:
        return text
    try:
        return translate_text_libre(text, endpoint, api_key)
    except (OSError, ValueError, urllib.error.URLError):
        return text


def translate_text_libre(text, endpoint, api_key=None):
    url = endpoint.rstrip("/") + "/translate"
    payload = {
        "q": text,
        "source": "auto",
        "target": "ko",
        "format": "text",
    }
    if api_key:
        payload["api_key"] = api_key
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        body = json.loads(response.read().decode("utf-8"))
    translated = body.get("translatedText")
    if not translated:
        raise ValueError("LibreTranslate response did not include translatedText")
    return translated


def _read_url(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read(300).decode("utf-8", "replace")
        if exc.code == 429:
            time.sleep(5)
        raise NewsFetchError("HTTP %d from %s: %s" % (exc.code, _domain(url), body.strip()))


def _write_raw(raw_dir, prefix, data, suffix):
    path = Path(raw_dir) / ("%s_%s%s" % (prefix, compact_timestamp(), suffix))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return str(path)


def _strip_source_suffix(title, source_name):
    if source_name and title.endswith(" - " + source_name):
        return title[: -len(" - " + source_name)].strip()
    if " - " in title:
        return title.rsplit(" - ", 1)[0].strip()
    return title


def _source_from_title(title):
    if " - " not in title:
        return ""
    return title.rsplit(" - ", 1)[1].strip()


def _dedupe_items(items):
    seen = set()
    deduped = []
    for item in sorted(items, key=lambda value: value.get("score", 0), reverse=True):
        key = _dedupe_key(item.get("title_ko") or item.get("title") or "")
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _rss_description_text(value):
    if not value:
        return ""
    parser = _TextHTMLParser()
    parser.feed(html.unescape(value))
    return " ".join(parser.text()).strip()


def _clean_headline(value):
    text = html.unescape(value or "")
    text = " ".join(text.replace("\n", " ").split())
    text = text.replace("…", "...").replace("···", "...").replace("·", " ")
    text = text.strip(" -|")
    if len(text) <= 96:
        return text
    return text[:95].rstrip() + "…"


def _parse_rss_date(value):
    if not value:
        return ""
    try:
        return parsedate_to_datetime(value).replace(microsecond=0).isoformat()
    except (TypeError, ValueError):
        return value


def _parse_gdelt_seen_date(value):
    if not value:
        return ""
    for pattern in ("%Y%m%dT%H%M%SZ", "%Y%m%d%H%M%S"):
        try:
            return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.strptime(value, pattern))
        except ValueError:
            pass
    return value


def _dedupe_key(value):
    return "".join(ch for ch in value.lower() if ch.isalnum())[:120]


def _hash(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _domain(url):
    return urllib.parse.urlparse(url).netloc


def _has_hangul(text):
    return any("\uac00" <= ch <= "\ud7a3" for ch in text)


class _TextHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._parts = []

    def handle_data(self, data):
        data = data.strip()
        if data:
            self._parts.append(data)

    def text(self):
        return self._parts
