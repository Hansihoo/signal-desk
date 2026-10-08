import hashlib
import html
import json
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path

from .db import record_snapshot, upsert_news_items
from .model_research import collect_model_research
from .model_ledger import collect_model_ledger
from .model_pages import collect_model_pages
from .timeutil import compact_timestamp, iso_utc, now_utc


USER_AGENT = "SignalDesk/0.1 (+local personal briefing)"
GOOGLE_NEWS_AI_TERMS = (
    '"OpenAI" OR "Anthropic" OR Claude OR Gemini OR DeepMind OR '
    '"Mistral AI" OR Llama OR DeepSeek OR xAI OR "Hugging Face"'
)


AI_FEEDS = [
    {
        "id": "ai_openai_news",
        "name": "OpenAI News",
        "feed_url": "https://openai.com/news/rss.xml",
        "home_url": "https://openai.com/news/",
        "tier": "official",
        "score_base": 150,
    },
    {
        "id": "ai_huggingface_blog",
        "name": "Hugging Face Blog",
        "feed_url": "https://huggingface.co/blog/feed.xml",
        "home_url": "https://huggingface.co/blog",
        "tier": "official/community",
        "score_base": 138,
    },
    {
        "id": "ai_vllm_releases",
        "name": "vLLM releases",
        "feed_url": "https://github.com/vllm-project/vllm/releases.atom",
        "home_url": "https://github.com/vllm-project/vllm",
        "tier": "open-source",
        "score_base": 126,
        "category_hint": "오픈소스",
    },
    {
        "id": "ai_llama_cpp_releases",
        "name": "llama.cpp releases",
        "feed_url": "https://github.com/ggml-org/llama.cpp/releases.atom",
        "home_url": "https://github.com/ggml-org/llama.cpp",
        "tier": "open-source",
        "score_base": 124,
        "category_hint": "오픈소스",
    },
    {
        "id": "ai_ollama_releases",
        "name": "Ollama releases",
        "feed_url": "https://github.com/ollama/ollama/releases.atom",
        "home_url": "https://github.com/ollama/ollama",
        "tier": "open-source",
        "score_base": 122,
        "category_hint": "오픈소스",
    },
    {
        "id": "ai_langchain_releases",
        "name": "LangChain releases",
        "feed_url": "https://github.com/langchain-ai/langchain/releases.atom",
        "home_url": "https://github.com/langchain-ai/langchain",
        "tier": "open-source",
        "score_base": 119,
        "category_hint": "AI 개발",
    },
    {
        "id": "ai_langgraph_releases",
        "name": "LangGraph releases",
        "feed_url": "https://github.com/langchain-ai/langgraph/releases.atom",
        "home_url": "https://github.com/langchain-ai/langgraph",
        "tier": "open-source",
        "score_base": 118,
        "category_hint": "AI 개발",
    },
    {
        "id": "ai_llama_index_releases",
        "name": "LlamaIndex releases",
        "feed_url": "https://github.com/run-llama/llama_index/releases.atom",
        "home_url": "https://github.com/run-llama/llama_index",
        "tier": "open-source",
        "score_base": 116,
        "category_hint": "AI 개발",
    },
    {
        "id": "ai_litellm_releases",
        "name": "LiteLLM releases",
        "feed_url": "https://github.com/BerriAI/litellm/releases.atom",
        "home_url": "https://github.com/BerriAI/litellm",
        "tier": "open-source",
        "score_base": 114,
        "category_hint": "API/플랫폼",
    },
    {
        "id": "ai_promptfoo_releases",
        "name": "promptfoo releases",
        "feed_url": "https://github.com/promptfoo/promptfoo/releases.atom",
        "home_url": "https://github.com/promptfoo/promptfoo",
        "tier": "open-source",
        "score_base": 112,
        "category_hint": "AI 개발",
    },
]


class AINewsFetchError(Exception):
    pass


def collect_ai_news(conn, limit=24, raw_dir="data/raw/ai_news", days=7):
    limit = max(1, int(limit or 1))
    days = max(1, int(days or 1))
    sources = AI_FEEDS + [_google_news_source(days), _model_news_source(days)]
    raw_feeds = []
    failures = []
    items = []
    per_feed_limit = max(8, min(25, limit))
    collected_at = now_utc()

    for source in sources:
        try:
            data = _read_url(source["feed_url"])
            raw_feeds.append(
                {
                    "source_id": source["id"],
                    "url": source["feed_url"],
                    "body": data.decode("utf-8", "replace"),
                }
            )
            parsed = parse_ai_feed(data, source, limit=per_feed_limit)
            items.extend(filter_recent_ai_items(parsed, days=days, now=collected_at))
        except (AINewsFetchError, OSError, ValueError, ET.ParseError, urllib.error.URLError) as exc:
            failures.append("%s: %s" % (source["id"], exc))

    items = _rank_items(_dedupe_items(items))[:limit]
    model_result = None
    try:
        model_result = collect_model_research(conn, raw_dir=str(Path(raw_dir) / "model_research"))
    except (OSError, ValueError, urllib.error.URLError) as exc:
        failures.append("ai_theo_model_research: %s" % exc)
    ledger_result = None
    try:
        ledger_result = collect_model_ledger(conn, raw_dir=str(Path(raw_dir) / "model_ledger"))
    except (OSError, ValueError, urllib.error.URLError) as exc:
        failures.append("ai_model_ledger: %s" % exc)
    pages_result = None
    try:
        pages_result = collect_model_pages(conn, raw_dir=str(Path(raw_dir) / "model_pages"))
        failures.extend("ai_model_pages: " + failure for failure in pages_result["failures"])
    except (OSError, ValueError, urllib.error.URLError) as exc:
        failures.append("ai_model_pages: %s" % exc)
    if not items and not model_result and not ledger_result and not pages_result:
        raise AINewsFetchError("no AI news source returned items: " + "; ".join(failures))

    raw_data = json.dumps(
        {
            "collected_at": iso_utc(),
            "days": days,
            "feed_count": len(raw_feeds),
            "failures": failures,
            "feeds": raw_feeds,
        },
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    raw_path = _write_raw(raw_dir, "ai_news_bundle", raw_data, ".json")
    stats = upsert_news_items(conn, items, source_ids=[source["id"] for source in sources])
    record_snapshot(conn, "ai_news_bundle", raw_path, len(items))
    conn.commit()
    return {
        "source_id": "ai_news_bundle",
        "raw_path": raw_path,
        "fetched": len(items) + (model_result["fetched"] if model_result else 0),
        "days": days,
        "inserted": stats["inserted"] + (model_result["inserted"] if model_result else 0),
        "updated": stats["updated"] + (model_result["updated"] if model_result else 0),
        "deduped": stats.get("deduped", 0),
        "failures": failures,
        "model_research": model_result,
        "model_ledger": ledger_result,
        "model_pages": pages_result,
    }


def parse_ai_feed(data, source, limit=8):
    root = ET.fromstring(data)
    if _local_name(root.tag) == "rss":
        return _parse_rss_feed(root, source, limit)
    if _local_name(root.tag) == "feed":
        return _parse_atom_feed(root, source, limit)
    return []


def filter_recent_ai_items(items, days=7, now=None, include_undated=True):
    if not days:
        return list(items)
    now = now or now_utc()
    cutoff = now - timedelta(days=max(1, int(days)))
    recent = []
    for item in items:
        published_at = item.get("published_at") or ""
        published_dt = _parse_datetime(published_at)
        if published_dt is None:
            if include_undated:
                recent.append(item)
            continue
        if published_dt >= cutoff:
            recent.append(item)
    return recent


def categorize_ai_news(text, source_id=""):
    value = ("%s %s" % (source_id, text or "")).lower()
    categories = [
        ("안전", ["safety", "security", "privacy", "red team", "policy", "misuse", "jailbreak"]),
        (
            "LLM 모델",
            [
                "gpt",
                "claude",
                "gemini",
                "gemma",
                "llama",
                "mistral",
                "qwen",
                "deepseek",
                "grok",
                "model",
                "reasoning",
                "multimodal",
            ],
        ),
        (
            "API/플랫폼",
            ["api", "sdk", "pricing", "deprecation", "platform", "tool calling", "function calling", "mcp", "gateway"],
        ),
        (
            "오픈소스",
            ["github", "release", "vllm", "llama.cpp", "ollama", "litellm", "promptfoo", "transformers"],
        ),
        ("연구", ["research", "paper", "benchmark", "arxiv", "eval", "evaluation", "dataset"]),
        ("AI 개발", ["agent", "rag", "retrieval", "langchain", "langgraph", "llamaindex", "coding", "prompt"]),
        ("시장/정책", ["funding", "partnership", "acquisition", "regulation", "law", "copyright", "enterprise"]),
    ]
    for category, keywords in categories:
        if any(keyword in value for keyword in keywords):
            return category
    return "AI 개발"


def summarize_ai_news(title, summary_text, category, source_name):
    title = _clean_text(title)
    summary_text = _clean_text(summary_text)
    base = title or summary_text or "AI 업데이트"
    if len(base) > 96:
        base = base[:95].rstrip() + "..."
    return "%s: %s. 개발자는 모델/API 변화, 의존 오픈소스 업데이트, 비용·호환성 영향 여부를 확인하면 좋습니다." % (
        category,
        base,
    )


def developer_impact(title, summary_text, category, source_name):
    text = ("%s %s" % (title or "", summary_text or "")).lower()
    if category == "LLM 모델":
        return "모델 선택지, 벤치마크 기준, 프롬프트·평가 세트 재검토에 영향을 줄 수 있습니다."
    if category == "API/플랫폼":
        return "SDK, 엔드포인트, 가격, 호출 방식이 바뀔 수 있어 통합 코드와 운영 비용을 확인해야 합니다."
    if category == "오픈소스":
        return "로컬 추론, 서빙, 평가, 에이전트 스택의 버전 고정과 업그레이드 판단에 바로 연결됩니다."
    if category == "연구":
        return "새로운 아키텍처, 평가 방식, 데이터셋이 제품 실험 백로그로 들어올 수 있습니다."
    if category == "안전":
        return "보안 리뷰, 정책 필터, 개인정보 처리, 레드팀 테스트 기준을 업데이트할 신호일 수 있습니다."
    if "mcp" in text:
        return "도구 연결과 에이전트 런타임 설계에 영향을 줄 수 있어 MCP 호환성을 확인할 만합니다."
    return "AI 제품 로드맵, 기술 선택, 모니터링 항목에 반영할 수 있는 일반 개발 신호입니다."


def action_needed(title, summary_text, category):
    text = ("%s %s" % (title or "", summary_text or "")).lower()
    if any(keyword in text for keyword in ["breaking", "deprecat", "migration", "remove", "security"]):
        return "사용 중인 버전과 릴리스 노트를 먼저 대조하고, 영향이 있으면 작은 재현 테스트를 만드세요."
    if category in ("오픈소스", "API/플랫폼"):
        return "현재 프로젝트 의존성과 겹치는지 확인하고, 필요하면 changelog와 이슈를 한 번 더 봅니다."
    if category == "LLM 모델":
        return "관심 모델이면 기존 프롬프트와 평가 샘플로 짧은 비교 실행을 준비하세요."
    if category == "연구":
        return "제품에 연결될 아이디어인지 판단하고, 실험 후보로 남길지 결정하세요."
    return "원문을 열어 실제 변경 범위와 후속 링크를 확인하세요."


def _parse_rss_feed(root, source, limit):
    channel = _first_child(root, "channel")
    nodes = _children(channel or root, "item")
    items = []
    seen = set()
    for index, node in enumerate(nodes):
        raw_title = html.unescape(_child_text(node, "title")).strip()
        link = _child_text(node, "link").strip()
        guid = _child_text(node, "guid").strip() or link or raw_title
        source_node = _first_child(node, "source")
        source_name = source["name"]
        source_url = source.get("home_url", "")
        if source_node is not None and _text(source_node):
            source_name = _text(source_node)
            source_url = source_node.attrib.get("url", source_url)
        title = _strip_source_suffix(raw_title, source_name)
        description = _html_to_text(_child_text(node, "description"))
        if not title or not link:
            continue
        key = _dedupe_key(title)
        if key in seen:
            continue
        seen.add(key)
        items.append(_make_item(source, title, link, guid, description, _child_text(node, "pubDate"), source_name, source_url, index))
        if len(items) >= limit:
            break
    return items


def _parse_atom_feed(root, source, limit):
    nodes = _children(root, "entry")
    items = []
    seen = set()
    for index, node in enumerate(nodes):
        title = html.unescape(_child_text(node, "title")).strip()
        link = _atom_link(node)
        guid = _child_text(node, "id").strip() or link or title
        description = _html_to_text(_child_text(node, "summary") or _child_text(node, "content"))
        published_at = _child_text(node, "published") or _child_text(node, "updated")
        if not title or not link:
            continue
        key = _dedupe_key(title)
        if key in seen:
            continue
        seen.add(key)
        items.append(
            _make_item(
                source,
                title,
                link,
                guid,
                description,
                published_at,
                source["name"],
                source.get("home_url", ""),
                index,
            )
        )
        if len(items) >= limit:
            break
    return items


def _make_item(source, title, link, guid, description, published_at, source_name, source_url, index):
    category = source.get("category_hint") or categorize_ai_news("%s %s" % (title, description), source["id"])
    detail = _clean_text(description)
    payload = {
        "source_tier": source.get("tier", ""),
        "developer_impact": developer_impact(title, description, category, source_name),
        "detail": detail or "원문 요약이 짧습니다. 링크를 열어 릴리스 노트와 후속 링크를 확인하세요.",
        "action_needed": action_needed(title, description, category),
        "feed_url": source.get("feed_url", ""),
        "home_url": source.get("home_url", ""),
    }
    content = json.dumps(
        {"title": title, "url": link, "summary": detail, "published_at": published_at},
        ensure_ascii=False,
        sort_keys=True,
    )
    return {
        "source_id": source["id"],
        "external_id": _hash("%s:%s" % (source["id"], guid)),
        "title": title,
        "title_ko": title,
        "url": link,
        "source_name": source_name,
        "source_url": source_url,
        "category": category,
        "language": "Korean" if _has_hangul(title + detail) else "English",
        "country": "",
        "published_at": _parse_date(published_at),
        "summary_ko": summarize_ai_news(title, detail, category, source_name),
        "score": max(1, int(source.get("score_base", 100)) - index * 2),
        "raw_payload": json.dumps(payload, ensure_ascii=False, sort_keys=True),
        "content_hash": _hash(content),
        "collected_at": iso_utc(),
    }


def _google_news_source(days=7):
    params = {
        "q": "%s when:%dd" % (GOOGLE_NEWS_AI_TERMS, max(1, int(days or 1))),
        "hl": "en-US",
        "gl": "US",
        "ceid": "US:en",
    }
    return {
        "id": "ai_google_news_llm",
        "name": "Google News AI search",
        "feed_url": "https://news.google.com/rss/search?" + urllib.parse.urlencode(params),
        "home_url": "https://news.google.com/",
        "tier": "news-search",
        "score_base": 105,
    }


def _model_news_source(days=7):
    query = ('(OpenAI OR Anthropic OR Google OR DeepMind OR Mistral OR DeepSeek OR xAI OR Qwen OR Meta) '
             '("new model" OR "model release" OR "model launch" OR "model update") when:%dd' % max(1, int(days or 1)))
    params = {"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"}
    return {
        "id": "ai_google_news_model_updates", "name": "Google News model updates",
        "feed_url": "https://news.google.com/rss/search?" + urllib.parse.urlencode(params),
        "home_url": "https://news.google.com/", "tier": "news-search",
        "category_hint": "LLM 모델", "score_base": 125,
    }


def _read_url(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=18) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read(300).decode("utf-8", "replace")
        if exc.code == 429:
            time.sleep(5)
        raise AINewsFetchError("HTTP %d from %s: %s" % (exc.code, _domain(url), body.strip()))


def _write_raw(raw_dir, prefix, data, suffix):
    path = Path(raw_dir) / ("%s_%s%s" % (prefix, compact_timestamp(), suffix))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return str(path)


def _rank_items(items):
    return sorted(
        items,
        key=lambda item: (
            item.get("score") or 0,
            item.get("published_at") or "",
            item.get("source_name") or "",
        ),
        reverse=True,
    )


def _dedupe_items(items):
    seen = set()
    deduped = []
    for item in _rank_items(items):
        key = _dedupe_key(item.get("title_ko") or item.get("title") or "")
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _parse_date(value):
    value = (value or "").strip()
    if not value:
        return ""
    dt = _parse_datetime(value)
    if dt is not None:
        return dt.replace(microsecond=0).isoformat()
    return value


def _parse_datetime(value):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return _as_utc(parsedate_to_datetime(value))
    except (TypeError, ValueError):
        pass
    cleaned = value.replace("Z", "+00:00")
    try:
        return _as_utc(datetime.fromisoformat(cleaned))
    except ValueError:
        return None


def _as_utc(value):
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _atom_link(node):
    links = _children(node, "link")
    if not links:
        return ""
    for link in links:
        if link.attrib.get("rel", "alternate") == "alternate" and link.attrib.get("href"):
            return link.attrib["href"]
    return links[0].attrib.get("href", "")


def _strip_source_suffix(title, source_name):
    if source_name and title.endswith(" - " + source_name):
        return title[: -len(" - " + source_name)].strip()
    if " - " in title:
        return title.rsplit(" - ", 1)[0].strip()
    return title


def _child_text(node, name):
    child = _first_child(node, name)
    return _text(child) if child is not None else ""


def _children(node, name):
    if node is None:
        return []
    return [child for child in list(node) if _local_name(child.tag) == name]


def _first_child(node, name):
    matches = _children(node, name)
    return matches[0] if matches else None


def _local_name(tag):
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _text(node):
    if node is None:
        return ""
    return "".join(node.itertext()).strip()


def _html_to_text(value):
    if not value:
        return ""
    parser = _TextHTMLParser()
    parser.feed(html.unescape(value))
    return _clean_text(" ".join(parser.text()))


def _clean_text(value):
    text = html.unescape(value or "")
    text = " ".join(text.replace("\n", " ").split())
    return text.strip(" -|")


def _dedupe_key(value):
    return "".join(ch for ch in (value or "").lower() if ch.isalnum())[:160]


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
