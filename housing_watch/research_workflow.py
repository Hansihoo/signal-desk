"""Question-led research, separate from the stable report-v1/render contract.

Mechanical provenance checks are necessary, not a claim of semantic truth.
Every releasable run also needs first-screen and evidence-aware body reviews.
"""

import hashlib
import ipaddress
import json
import re
import socket
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .research_data import validate_report
from .timeutil import iso_utc

VERSION = "question-research-1"
CACHE_VERSION = VERSION + "-application-dates"
PROFILES = {
    "technology": {
        "question": "어떤 문제를 어떻게 해결하며, 다른 조건에서는 언제 실패하는가?",
        "requires": ["concept", "mechanism", "worked_example", "limitation"],
        "method": "선행 개념을 정의하고 동일한 입력의 처리·출력·실패를 추적한다. 예시와 실행한 실습을 구별한다.",
    },
    "market": {
        "question": "무엇의 수요가 얼마나 변했고 실제 고객은 무엇을 얼마에 요구하는가?",
        "requires": ["measurement", "actual_case", "price", "limitation"],
        "method": "통계의 모집단·기간·단위를 보존하고 실제 발주/기업 사례를 비교한다. 제시 예산·체결 금액·판매 호가를 구별한다.",
    },
    "opportunity": {
        "question": "누가 어떤 문제에 돈을 지불하며, 비용과 진입 장벽을 감안해 성립하는가?",
        "requires": ["customer_problem", "actual_case", "price", "barrier"],
        "method": "고객 문제와 실제 지불/발주 근거, 비용·경쟁·진입 조건을 연결한다. 수요와 수익성을 동일시하지 않는다.",
    },
    "comparison": {
        "question": "독자의 같은 작업에서 어떤 선택지가 어떤 조건에 적합한가?",
        "requires": ["capability", "price", "comparable_case", "limitation"],
        "method": "같은 작업·버전·측정 조건으로 비교한다. 공급사 기능표와 직접 실행한 성능 측정을 구별한다.",
    },
    "news": {
        "question": "언제 무엇이 바뀌었고 이전 방식과 비교해 누구에게 어떤 영향이 있는가?",
        "requires": ["change", "previous_state", "impact", "limitation"],
        "method": "발표일·적용일과 이전 조건을 확인한다. 발표·출시·계정별 사용 가능 상태를 구별한다.",
    },
}
EVIDENCE_KINDS = {"official_document", "measurement", "buyer_posting", "completed_case",
                  "seller_offer", "benchmark", "worked_example"}
REVIEW_CRITERIA = {"question_answered", "analysis", "evidence", "readability", "factuality", "reader_outcome"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def nonempty(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected nonempty text")
    return value


def make_plan(request):
    """Explicit classification: never guess a market purpose from a tool name.

    A custom profile must declare its own evidence method/requirements. Concrete
    questions can be supplied; otherwise the reader's own question is the core.
    """
    for field in ("id", "topic_id", "reader", "reader_question", "outcome", "research_type"):
        nonempty(request.get(field))
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", request["id"]):
        raise ValueError("Invalid report ID")
    profile = request.get("custom_profile") if request["research_type"] == "custom" else PROFILES.get(request["research_type"])
    if not profile or not profile.get("requires") or not profile.get("method"):
        raise ValueError("Choose a research_type or define a custom_profile; ambiguous subjects need an explicit purpose")
    questions = request.get("questions") or [{"id": "core", "question": request["reader_question"], "requires": profile["requires"]}]
    ids = set()
    for question in questions:
        qid = nonempty(question.get("id"))
        nonempty(question.get("question"))
        if qid in ids or not question.get("requires") or not all(isinstance(x, str) and x.strip() for x in question["requires"]):
            raise ValueError("Questions need unique IDs and evidence requirements")
        ids.add(qid)
    required = {x for q in questions for x in q["requires"]}
    if set(profile["requires"]) - required:
        raise ValueError("Questions omit profile requirements; use an explicitly narrower custom profile")
    sources = request.get("sources", [])
    seen = set()
    for source in sources:
        sid = nonempty(source.get("id"))
        nonempty(source.get("title"))
        validate_url(source.get("url"), resolve=False)
        if sid in seen or source.get("kind") not in EVIDENCE_KINDS:
            raise ValueError("Sources need unique IDs and a supported evidence kind")
        seen.add(sid)
    return {"version": VERSION, "request": request, "questions": questions, "method": profile["method"]}


def validate_url(url, resolve=True):
    parts = urlsplit(nonempty(url))
    if parts.scheme not in ("http", "https") or not parts.hostname or parts.username or parts.password:
        raise ValueError("Only public HTTP(S) sources without credentials")
    if parts.port not in (None, 80, 443):
        raise ValueError("Nonstandard source port")
    if resolve:
        addresses = socket.getaddrinfo(parts.hostname, parts.port or (443 if parts.scheme == "https" else 80))
        if not addresses or any(not ipaddress.ip_address(x[4][0]).is_global for x in addresses):
            raise ValueError("Private/local source addresses are not allowed")
    return url


class _Redirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "nav", "header", "footer", "noscript"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "nav", "header", "footer", "noscript"):
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def extract_text(body, content_type):
    if "html" in content_type:
        parser = _Text()
        parser.feed(body)
        body = " ".join(parser.parts)
    return " ".join(body.split())


def fetch_original(source, max_bytes=2000000):
    validate_url(source["url"])
    with build_opener(_Redirects()).open(Request(source["url"], headers={"User-Agent": "SignalDeskResearch/1.0"}), timeout=20) as response:
        body = response.read(max_bytes + 1)
        content_type = response.headers.get_content_type()
        if len(body) > max_bytes:
            raise ValueError("Original exceeds collection byte budget")
        if content_type not in ("text/html", "text/plain", "application/json", "text/markdown"):
            raise ValueError("Unsupported original type; PDF/attachments need explicit extraction")
        final = response.geturl()
        # A job disappearing into a category page is not the same original.
        if urlsplit(final).path.rstrip("/") != urlsplit(source["url"]).path.rstrip("/"):
            raise ValueError("Original redirected to a different page; review required")
        return body, content_type + ";charset=" + (response.headers.get_content_charset() or "utf-8"), final


def ensure_store(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS research_originals (
        url TEXT PRIMARY KEY, document TEXT NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS research_generation_cache (
        cache_key TEXT PRIMARY KEY, document TEXT NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS research_workflow_runs (
        id TEXT PRIMARY KEY, document TEXT NOT NULL, created_at TEXT NOT NULL)""")


def collect_originals(conn, sources, raw_root, max_fetches=6, max_age_hours=24, fetcher=fetch_original):
    """Failed refreshes never become fresh evidence; body-hash cache keeps history.

    Cache reuse is explicit and preserves the acquisition date. A network success
    updates last_successful_collection even if the body itself is unchanged.
    """
    ensure_store(conn)
    root = Path(raw_root)
    if not root.is_dir():
        raise ValueError("Use an existing registered raw output directory")
    results, fetches = [], 0
    for source in sources:
        previous = conn.execute("SELECT document FROM research_originals WHERE url=?", (source["url"],)).fetchone()
        old = json.loads(previous[0]) if previous else None
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(old["last_successful_collection"].replace("Z", "+00:00"))).total_seconds() / 3600 if old else float("inf")
        if old and age < max_age_hours:
            results.append(dict(old, id=source["id"], title=source["title"], kind=source["kind"], status="cached"))
            continue
        if fetches >= max_fetches:
            results.append(dict(source, status="not_collected", error="fetch budget exhausted"))
            continue
        fetches += 1
        try:
            body, mime, final = fetcher(source)
            charset = mime.split("charset=", 1)[1].split(";", 1)[0].strip() if "charset=" in mime else "utf-8"
            try:
                text = extract_text(body.decode(charset, errors="replace"), mime)
            except LookupError:
                raise ValueError("Unsupported original character encoding")
            if len(text) < 100:
                raise ValueError("Original content missing/too short")
            sha = hashlib.sha256(body).hexdigest()
            path = root / (sha + ".raw")
            if not path.exists():
                path.write_bytes(body)
            now = iso_utc()
            item = dict(source, final_url=final, content_hash=sha, text=text, text_hash=digest(text), raw_path=str(path.resolve()),
                        first_collected=old["first_collected"] if old else now,
                        last_successful_collection=now, published_on=source.get("published_on"),
                        reviewed_at=None, status="unchanged" if old and old["content_hash"] == sha else "collected")
            conn.execute("INSERT OR REPLACE INTO research_originals VALUES (?, ?)", (source["url"], canonical(item)))
            results.append(item)
        except (OSError, ValueError) as exc:
            # No stale text is offered to the analyst after a failed attempt.
            results.append(dict(source, status="failed", attempted_at=iso_utc(), error=type(exc).__name__))
    conn.commit()
    return results, fetches


def issue(stage, code, detail):
    return {"stage": stage, "code": code, "detail": detail}


def evidence_issues(plan, sources, analysis):
    issues = []
    source_map = {s["id"]: s for s in sources if s.get("status") in ("collected", "unchanged", "cached", "imported_original")}
    for source in source_map.values():
        if digest(source.get("text")) != source.get("text_hash") or not source.get("last_successful_collection"):
            issues.append(issue("research", "original_integrity", source["id"]))
    evidence = analysis.get("evidence", [])
    ids, valid = set(), {}
    for e in evidence:
        eid = e.get("id")
        if not eid or eid in ids:
            issues.append(issue("analysis", "evidence_id", "Missing/duplicate evidence ID"))
            continue
        ids.add(eid)
        source = source_map.get(e.get("source_id"))
        quote = " ".join(e.get("quote", "").split())
        if not source or len(quote) < 8 or quote not in source["text"] or e.get("source_hash") != source["content_hash"]:
            issues.append(issue("research", "original_support", eid))
            continue
        if not e.get("meaning") or not e.get("limits") or not e.get("supports"):
            issues.append(issue("analysis", "meaning_and_limits", eid))
            continue
        # Kind is collector metadata, never the model's self-declared rewrite.
        kind = source["kind"]
        if "actual_case" in e["supports"] and kind not in ("buyer_posting", "completed_case"):
            issues.append(issue("research", "actual_case_type", eid))
            continue
        if "price" in e["supports"]:
            price_type = e.get("price_type")
            expected = {"buyer_posting": "posted_budget", "seller_offer": "asking_price", "completed_case": "paid_amount"}.get(kind)
            if not price_type or (expected and price_type != expected):
                issues.append(issue("analysis", "price_type", eid))
                continue
        if "measurement" in e["supports"]:
            if not all(e.get("measurement", {}).get(k) for k in ("population", "period", "unit", "comparison")):
                issues.append(issue("research", "measurement_scope", eid))
                continue
        valid[eid] = e
    for q in plan["questions"]:
        answer = next((a for a in analysis.get("answers", []) if a.get("question_id") == q["id"]), None)
        if not answer or not answer.get("answer") or not answer.get("reasoning") or not answer.get("limits"):
            issues.append(issue("analysis", "unanswered_question", q["id"]))
            continue
        selected = [valid[x] for x in answer.get("evidence_ids", []) if x in valid]
        missing = set(q["requires"]) - {tag for e in selected for tag in e["supports"]}
        if missing:
            issues.append(issue("research", "missing_evidence", q["id"] + ": " + ", ".join(sorted(missing))))
    for gap in analysis.get("gaps", []):
        issues.append(issue("research", "analyst_gap", str(gap)))
    return issues


def report_nodes(report, path=""):
    """All content objects that carry citation/kind metadata, including table rows."""
    if isinstance(report, dict):
        if "source_ids" in report:
            yield path, report
        for key, value in report.items():
            yield from report_nodes(value, path + "/" + key)
    elif isinstance(report, list):
        for index, value in enumerate(report):
            yield from report_nodes(value, path + "/" + str(index))


def pointer(document, path):
    current = document
    for part in path.strip("/").split("/"):
        current = current[int(part)] if isinstance(current, list) else current[part]
    return current


def draft_issues(plan, sources, analysis, draft):
    report = draft.get("report", {})
    try:
        validate_report(report)
    except (ValueError, KeyError, TypeError) as exc:
        return [issue("writing", "report_contract", str(exc))]
    issues = []
    request = plan["request"]
    if report["id"] != request["id"] or report["topic_id"] != request["topic_id"]:
        issues.append(issue("writing", "report_identity", "Report changed the requested identity"))
    by_source = {s["id"]: s for s in sources}
    for ref in report["references"]:
        if ref["id"] not in by_source or ref["url"] != by_source[ref["id"]]["url"]:
            issues.append(issue("research", "reference_url", ref["id"]))
    by_evidence = {e["id"]: e for e in analysis.get("evidence", [])}
    claims = {c.get("path"): c for c in draft.get("claims", [])}
    for path, node in report_nodes(report):
        claim = claims.get(path)
        if not claim or claim.get("kind") not in ("fact", "inference", "example"):
            issues.append(issue("writing", "unmapped_claim", path))
            continue
        if node.get("kind") == "example" and claim["kind"] != "example":
            issues.append(issue("writing", "example_label", path))
        if node.get("kind") == "fact" and claim["kind"] != "fact":
            issues.append(issue("writing", "fact_label", path))
        if (path.startswith("/metrics/") or re.fullmatch(r"/tables/\d+/rows/\d+", path)) and claim["kind"] != "fact":
            issues.append(issue("writing", "fact_label", path))
        ids = claim.get("evidence_ids", [])
        if claim["kind"] != "example" and (not ids or any(x not in by_evidence for x in ids)):
            issues.append(issue("research", "claim_evidence", path))
        linked = {by_evidence[x]["source_id"] for x in ids if x in by_evidence}
        if set(node["source_ids"]) - linked:
            issues.append(issue("analysis", "citation_alignment", path))
        disclosed_note = path.startswith("/caveats/") and not node["source_ids"]
        if claim["kind"] == "example" and node.get("kind") not in ("example", "judgment") and not disclosed_note:
            issues.append(issue("writing", "example_as_fact", path))
    for q in plan["questions"]:
        paths = draft.get("answer_paths", {}).get(q["id"], [])
        if not paths:
            issues.append(issue("writing", "answer_not_in_report", q["id"]))
        for path in paths:
            try:
                if not pointer(report, path):
                    raise ValueError("empty")
            except (KeyError, IndexError, TypeError, ValueError):
                issues.append(issue("writing", "invalid_answer_path", path))
    # Regression terms are a specific repair cue, not a universal readability score.
    if any(term in report["title"] + report["deck"] for term in ("수요 신호", "실체 납품 업무")):
        issues.append(issue("writing", "opaque_first_screen", "Explain the actual customer/work rather than compressed labels"))
    return issues


def review_issues(review, expected_hash, first_screen=False, document=None):
    if review.get("input_hash") != expected_hash:
        return [issue("writing", "stale_review", "Review does not match its input")]
    criteria = {"readability", "question_answered", "reader_outcome"} if first_screen else REVIEW_CRITERIA
    checks = review.get("checks", {})
    issues = []
    for criterion in criteria:
        check = checks.get(criterion, {})
        if check.get("passed") is not True or not check.get("reason") or not check.get("locations"):
            issues.append(issue("writing", "review_" + criterion, check.get("reason") or "Missing reason/locations"))
        if document is not None:
            for location in check.get("locations", []):
                try:
                    path = "/" + location.lstrip("/")
                    try:
                        pointer(document, path)
                    except (KeyError, IndexError, TypeError, ValueError):
                        pointer(document["draft"]["report"], path)
                except (KeyError, IndexError, TypeError, ValueError, AttributeError):
                    issues.append(issue("writing", "review_location", str(location)))
    for finding in review.get("issues", []):
        if finding.get("stage") not in ("research", "analysis", "writing") or not finding.get("detail"):
            issues.append(issue("writing", "invalid_review_issue", "Reviewer returned an invalid issue"))
        else:
            issues.append(finding)
    return issues


def first_screen(report):
    return {key: report[key] for key in ("title", "description", "deck")}


def body_review_input(plan, sources, analysis, draft):
    return {"plan": plan, "sources": model_sources(sources), "analysis": analysis, "draft": draft}


def model_sources(sources):
    # Operation timestamps/cache status are receipts, not new substantive facts.
    # Unchanged originals can reuse analysis/reviews without refreshing checked_on.
    fields = ("id", "title", "url", "kind", "content_hash", "text", "text_hash", "published_on", "review_scope")
    return [{k: s.get(k) for k in fields} for s in sources
            if s.get("status") in ("collected", "unchanged", "cached", "imported_original")]


def quality_issues(package):
    if package.get("version") != VERSION:
        return [issue("writing", "package_version", "Unsupported quality package")]
    if package.get("status") not in (None, "ready") or package.get("issues"):
        return [issue("writing", "workflow_not_ready", "A stopped/blocked run cannot be released")]
    plan, sources, analysis, draft = (package[k] for k in ("plan", "sources", "analysis", "draft"))
    make_plan(plan["request"])
    if plan != make_plan(plan["request"]):
        return [issue("analysis", "plan_binding", "Plan differs from the request/profile")]
    problems = evidence_issues(plan, sources, analysis) + draft_issues(plan, sources, analysis, draft)
    if problems:
        return problems
    problems += review_issues(package.get("first_screen_review", {}), digest(first_screen(draft["report"])), True, first_screen(draft["report"]))
    body_input = body_review_input(plan, sources, analysis, draft)
    problems += review_issues(package.get("body_review", {}), digest(body_input), document=body_input)
    return problems


def verify_release(reports, packages):
    if len(reports) != len(packages):
        raise ValueError("Quality packages must cover every released report")
    by_id = {p["draft"]["report"]["id"]: p for p in packages}
    if len(by_id) != len(packages):
        raise ValueError("Duplicate quality report")
    for report in reports:
        package = by_id.get(report["id"])
        if not package or digest(report) != digest(package["draft"]["report"]):
            raise ValueError("Quality receipt does not bind the released report")
        issues = quality_issues(package)
        if issues:
            raise ValueError("Research quality gate: " + canonical(issues))


def run_research(conn, request, provider, raw_root, limits=None, fetcher=fetch_original, searcher=None):
    """Bounded orchestration. No provider/search is called implicitly by publish.

    Provider protocol: identity + generate(stage, payload, max_output_tokens).
    Search protocol: searcher(question, domains) -> candidate source metadata.
    Both are injectable so routing/expense/failure paths have offline regressions.
    """
    # An auto-classified request is validated using a temporary planning profile;
    # it never reaches collection until a concrete method has been selected.
    if request.get("research_type") == "auto":
        planning_requirements = [tag for q in (request.get("questions") or []) for tag in q.get("requires", [])]
        plan = make_plan(dict(request, research_type="custom", custom_profile={
            "method": "Select research method before collection",
            "requires": planning_requirements or ["reader_question"],
        }))
    else:
        plan = make_plan(request)
    limits = dict({"fetches": 6, "calls": 10, "searches": 1, "rounds": 2,
                   "output_tokens": 10000, "input_chars": 120000, "max_age_hours": 24}, **(limits or {}))
    if any(type(x) not in (int, float) or x < 0 for x in limits.values()):
        raise ValueError("Nonnegative budgets required")
    ensure_store(conn)
    usage = {"calls": 0, "cache_hits": 0, "fetches": 0, "searches": 0, "web_search_calls": 0, "input_tokens": 0, "output_tokens": 0}
    events, collected, analysis, draft, screen, review = [], [], None, None, None, None

    def generate(stage, payload):
        identity = nonempty(provider.identity)
        key = digest({"version": CACHE_VERSION, "provider": identity, "stage": stage, "input": payload,
                      "max_output_tokens": limits["output_tokens"]})
        cached = conn.execute("SELECT document FROM research_generation_cache WHERE cache_key=?", (key,)).fetchone()
        if cached:
            usage["cache_hits"] += 1
            return json.loads(cached[0])
        if usage["calls"] >= limits["calls"]:
            raise ValueError("Model call budget exhausted")
        if len(canonical(payload)) > limits["input_chars"]:
            raise ValueError("Model input budget exceeded; narrow original excerpts explicitly")
        usage["calls"] += 1  # Failed/refused/incomplete requests also consume the call budget.
        response = provider.generate(stage, payload, int(limits["output_tokens"]))
        for k in ("input_tokens", "output_tokens", "web_search_calls"):
            usage[k] += response.get("usage", {}).get(k, 0)
        document = response["document"]
        if not isinstance(document, dict):
            raise ValueError("Provider output must be a JSON object")
        if stage == "write" and isinstance(document.get("report"), dict):
            # The application knows when this draft was actually authored/reviewed;
            # a model must not guess the evidence-check date. Cache hits retain it.
            document["report"]["checked_on"] = iso_utc()[:10]
        conn.execute("INSERT OR REPLACE INTO research_generation_cache VALUES (?, ?)", (key, canonical(document)))
        conn.commit()
        return document

    problems = []
    route = "research"
    try:
        if request.get("research_type") == "auto" or request.get("plan_questions", not request.get("questions")):
            planned = generate("plan", {"request": request, "profiles": PROFILES})
            chosen = planned["research_type"] if request["research_type"] == "auto" else request["research_type"]
            refined = dict(request, research_type=chosen, questions=planned["questions"])
            if chosen == "custom":
                refined["custom_profile"] = planned.get("custom_profile", request.get("custom_profile"))
            plan = make_plan(refined)
            events.append({"stage":"plan", "method":plan["method"], "questions":plan["questions"]})
        for round_index in range(int(limits["rounds"])):
            events.append({"round": round_index + 1, "stage": route, "issues": problems})
            if route == "research":
                candidates = request.get("sources", []) if not collected else []
                if not candidates and (searcher or getattr(provider, "discovery_enabled", False)) and usage["searches"] < limits["searches"]:
                    domains = request.get("allowed_domains", [])
                    if not domains:
                        raise ValueError("Supplemental discovery needs allowed_domains")
                    usage["searches"] += 1
                    if searcher:
                        candidates = searcher(request["reader_question"] + " " + canonical(problems), domains)
                    else:
                        candidates = generate("discover", {"question": request["reader_question"], "gaps": problems,
                                                           "allowed_domains": domains})["sources"]
                    known = {s["url"] for s in collected}
                    candidates = [s for s in candidates if s["url"] not in known and any(
                        urlsplit(s["url"]).hostname == d or (urlsplit(s["url"]).hostname or "").endswith("." + d) for d in domains)]
                    # Same contract for discovered sources; search text is never original evidence.
                    make_plan(dict(plan["request"], sources=candidates))
                    if {s["id"] for s in candidates} & {s["id"] for s in collected}:
                        raise ValueError("Discovered source IDs collide with existing sources")
                if not candidates:
                    break
                new, count = collect_originals(conn, candidates, raw_root, max_fetches=int(limits["fetches"] - usage["fetches"]),
                                                max_age_hours=limits["max_age_hours"], fetcher=fetcher)
                collected += new
                usage["fetches"] += count
            good = [s for s in collected if s.get("status") in ("collected", "cached", "unchanged")]
            if not good:
                problems = [issue("research", "originals_unavailable", "No original could be read; do not substitute search snippets")]
                route = "research"
                continue
            if route in ("research", "analysis") or analysis is None:
                analysis = generate("analyze", {"plan": plan, "sources": model_sources(good), "repair": problems})
                problems = evidence_issues(plan, good, analysis)
                if problems:
                    route = "research" if any(x["stage"] == "research" for x in problems) else "analysis"
                    continue
            draft = generate("write", {"plan": plan, "sources": model_sources(good), "analysis": analysis, "previous_draft": draft, "repair": problems})
            problems = draft_issues(plan, good, analysis, draft)
            if not problems:
                screen_input = first_screen(draft["report"])
                screen = generate("review_first_screen", screen_input)
                problems = review_issues(screen, digest(screen_input), True, screen_input)
                review_input = body_review_input(plan, good, analysis, draft)
                review = generate("review_body", review_input)
                problems += review_issues(review, digest(review_input), document=review_input)
            if not problems:
                break
            route = next((stage for stage in ("research", "analysis", "writing") if any(p["stage"] == stage for p in problems)), "writing")
    except (ValueError, OSError, KeyError, TypeError) as exc:
        problems = problems + [issue(route, "execution_stopped", str(exc))]
    if not draft and not problems:
        problems = [issue("research", "no_result", "No generation round was permitted/completed")]
    package = {"version": VERSION, "plan": plan, "sources": collected, "analysis": analysis, "draft": draft,
               "first_screen_review": screen, "body_review": review, "usage": usage, "events": events,
               "issues": problems, "status": "blocked" if problems or not draft else "ready", "created_at": iso_utc()}
    if package["status"] == "ready":
        final_issues = quality_issues(package)
        if final_issues:
            package.update(status="blocked", issues=final_issues)
    run_id = digest(package)
    conn.execute("INSERT OR REPLACE INTO research_workflow_runs VALUES (?, ?, ?)", (run_id, canonical(package), package["created_at"]))
    conn.commit()
    return package
