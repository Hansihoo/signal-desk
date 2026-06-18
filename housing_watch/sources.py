import json
import os
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

from .details import enrich_item_from_detail
from .textutil import clean_text, content_hash, first_date, stable_space
from .timeutil import compact_timestamp, iso_utc


USER_AGENT = "HousingWatch/0.1 (+local research MVP)"


class FetchError(RuntimeError):
    pass


class TableParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rows = []
        self._in_tr = False
        self._in_cell = False
        self._cell_parts = []
        self._cells = []
        self._links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self._in_tr = True
            self._cells = []
            self._links = []
        elif self._in_tr and tag in ("td", "th"):
            self._in_cell = True
            self._cell_parts = []
        elif self._in_tr and tag == "a" and attrs.get("href"):
            self._links.append(attrs["href"])

    def handle_data(self, data):
        if self._in_cell:
            self._cell_parts.append(data)

    def handle_endtag(self, tag):
        if self._in_tr and tag in ("td", "th") and self._in_cell:
            self._cells.append(clean_text(" ".join(self._cell_parts)))
            self._cell_parts = []
            self._in_cell = False
        elif tag == "tr" and self._in_tr:
            if self._cells:
                self.rows.append({"cells": list(self._cells), "links": list(self._links)})
            self._in_tr = False
            self._cells = []
            self._links = []


def fetch_url(url, params=None):
    target = url
    if params:
        target = "%s?%s" % (url, urlencode(params))
    request = Request(target, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        body = response.read()
    return body.decode(charset, errors="replace")


def save_raw_snapshot(source_id, payload, suffix="html"):
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    safe_source = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in source_id)
    path = raw_dir / ("%s-%s.%s" % (compact_timestamp(), safe_source, suffix))
    path.write_text(payload, encoding="utf-8")
    return str(path)


def parse_seoul_housing_table(source, html_text):
    parser = TableParser()
    parser.feed(html_text)
    layout = source.get("layout", "lh")
    items = []

    for row in parser.rows:
        cells = [stable_space(cell) for cell in row["cells"] if stable_space(cell)]
        if not cells or cells[0] == "번호":
            continue

        if layout == "lh":
            item = _parse_lh_row(source, cells, row["links"])
        elif layout == "sh":
            item = _parse_sh_row(source, cells, row["links"])
        else:
            item = None

        if item:
            items.append(item)
    return items


def _best_link(base_url, links):
    for link in links:
        if link.startswith("javascript:") or link.startswith("#"):
            continue
        return urljoin(base_url, link)
    return base_url


def _parse_lh_row(source, cells, links):
    if len(cells) < 7:
        return None
    number, category, title, region, published, deadline, status = cells[:7]
    if not number.isdigit():
        return None
    url = _best_link(source["url"], links)
    raw_text = " ".join(cells)
    external_id = "%s:%s" % (source["id"], number)
    return _normalized_item(source, external_id, title, url, category, region, status, published, deadline, raw_text)


def _parse_sh_row(source, cells, links):
    if len(cells) < 7:
        return None
    number, category, title, published, deadline, status, department = cells[:7]
    if not number.isdigit():
        return None
    url = _best_link(source["url"], links)
    region = source.get("region", "서울")
    raw_text = " ".join(cells + [department])
    external_id = "%s:%s" % (source["id"], number)
    return _normalized_item(source, external_id, title, url, category, region, status, published, deadline, raw_text)


def _normalized_item(source, external_id, title, url, category, region, status, published, deadline, raw_text):
    title = clean_text(title)
    published = first_date(published)
    deadline = first_date(deadline)
    summary = "%s %s %s %s" % (source.get("agency", ""), region, category, status)
    return {
        "source_id": source["id"],
        "external_id": external_id,
        "title": title,
        "url": url,
        "agency": source.get("agency", ""),
        "category": clean_text(category),
        "region": clean_text(region),
        "status": clean_text(status),
        "published_at": published,
        "deadline_at": deadline,
        "summary": clean_text(summary),
        "raw_text": clean_text(raw_text),
        "content_hash": content_hash([source["id"], external_id, title, url, raw_text]),
        "collected_at": iso_utc(),
    }


def fetch_source(source):
    kind = source.get("kind")
    if kind == "seoul_housing_table":
        html_text = fetch_url(source["url"], source.get("params"))
        raw_path = save_raw_snapshot(source["id"], html_text, "html")
        items = parse_seoul_housing_table(source, html_text)
        if source.get("collect_details", True):
            items = enrich_items_with_details(source, items)
        return {
            "source_id": source["id"],
            "raw_path": raw_path,
            "items": items,
        }
    if kind == "lh_openapi":
        return fetch_lh_openapi(source)
    raise FetchError("Unsupported source kind: %s" % kind)


def enrich_items_with_details(source, items):
    enriched = []
    for item in items:
        url = item.get("url")
        if not url or not url.startswith("http"):
            enriched.append(item)
            continue
        try:
            detail_html = fetch_url(url)
            detail_key = "%s-%s" % (source["id"], item["external_id"].split(":")[-1])
            save_raw_snapshot(detail_key, detail_html, "detail.html")
            enrich_item_from_detail(item, detail_html)
            item["detail_collected_at"] = iso_utc()
            item["content_hash"] = content_hash(
                [
                    item.get("source_id", ""),
                    item.get("external_id", ""),
                    item.get("title", ""),
                    item.get("url", ""),
                    item.get("raw_text", ""),
                    item.get("detail_summary", ""),
                ]
            )
        except Exception as exc:
            item["detail_summary"] = "상세 수집 실패: %s" % exc
        enriched.append(item)
    return enriched


def fetch_lh_openapi(source):
    env_name = source.get("requires_env", "DATA_GO_KR_SERVICE_KEY")
    service_key = os.environ.get(env_name)
    if not service_key:
        raise FetchError("%s requires environment variable %s" % (source["id"], env_name))

    params = {
        "serviceKey": service_key,
        "PG_SZ": "50",
        "PAGE": "1",
        "_type": "json",
    }
    payload = fetch_url(source["url"], params)
    raw_path = save_raw_snapshot(source["id"], payload, "json")
    data = json.loads(payload)
    items = []
    rows = data.get("dsList", []) or data.get("response", {}).get("body", {}).get("items", [])
    for index, row in enumerate(rows):
        title = row.get("PAN_NM") or row.get("panNm") or row.get("title") or ""
        if not title:
            continue
        external_id = "%s:%s" % (source["id"], row.get("PAN_ID") or row.get("panId") or index)
        url = row.get("DTL_URL") or row.get("url") or "https://apply.lh.or.kr/"
        items.append(
            _normalized_item(
                source,
                external_id,
                title,
                url,
                row.get("AIS_TP_CD_NM") or row.get("category") or "",
                row.get("CNP_CD_NM") or row.get("region") or "",
                row.get("PAN_SS") or row.get("status") or "",
                row.get("PAN_NT_ST_DT") or row.get("published_at") or "",
                row.get("CLSG_DT") or row.get("deadline_at") or "",
                json.dumps(row, ensure_ascii=False),
            )
        )
    return {"source_id": source["id"], "raw_path": raw_path, "items": items}
