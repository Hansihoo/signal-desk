import struct
from pathlib import Path

from .db import all_items
from .render import ACTIVE_STATUSES


def review_project(conn, html_path="site/brief.html", image_path="reports/brief.png", max_width=390):
    items = all_items(conn)
    active = [item for item in items if item.get("status") in ACTIVE_STATUSES]
    scoped_regions = ["서울", "서울특별시", "경기", "경기도"]
    checks = []

    checks.append(_check("database has items", bool(items), "%d items" % len(items)))
    checks.append(_check("database has active notices", bool(active), "%d active" % len(active)))
    checks.append(_check("items have official links", all((item.get("url") or "").startswith("http") for item in items), "checked %d urls" % len(items)))
    checks.append(_check("items stay in Seoul/Gyeonggi scope", all(_region_in_scope(item.get("region"), scoped_regions) for item in items), _region_summary(items)))

    html_file = Path(html_path)
    html_text = html_file.read_text(encoding="utf-8") if html_file.exists() else ""
    checks.append(_check("brief html exists", html_file.exists(), str(html_file)))
    checks.append(_check("brief html has viewport", 'name="viewport"' in html_text, "mobile viewport"))
    checks.append(_check("brief html has max width", ("max-width: %dpx" % max_width) in html_text, "expected %dpx" % max_width))
    checks.append(_check("brief html wraps long text", "overflow-wrap: anywhere" in html_text, "overflow guard"))
    checks.append(_check("brief html is concise", html_text.count('class="notice"') <= 5, "%d cards" % html_text.count('class="notice"')))
    checks.append(_check("brief html has decision labels", all(label in html_text for label in ["주소", "면적", "공급", "가격", "조건"]), "address/area/supply/price/eligibility"))

    image_file = Path(image_path)
    width_height = png_dimensions(image_file) if image_file.exists() else None
    checks.append(_check("brief image exists", image_file.exists(), str(image_file)))
    if width_height:
        width, height = width_height
        checks.append(_check("brief image width capped", width <= max_width, "%dx%d <= %dpx" % (width, height, max_width)))
    else:
        checks.append(_check("brief image width capped", False, "no PNG dimensions"))

    ok = all(check["ok"] for check in checks)
    return {"ok": ok, "checks": checks}


def format_review(result):
    lines = ["Housing Watch Review: %s" % ("PASS" if result["ok"] else "FAIL"), ""]
    for check in result["checks"]:
        mark = "OK" if check["ok"] else "FAIL"
        lines.append("- [%s] %s: %s" % (mark, check["name"], check["detail"]))
    return "\n".join(lines)


def png_dimensions(path):
    path = Path(path)
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or not header.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    return struct.unpack(">II", header[16:24])


def _check(name, ok, detail):
    return {"name": name, "ok": bool(ok), "detail": detail}


def _region_in_scope(region, scoped_regions):
    value = region or ""
    return any(wanted and (wanted in value or value in wanted) for wanted in scoped_regions)


def _region_summary(items):
    counts = {}
    for item in items:
        region = item.get("region") or "-"
        counts[region] = counts.get(region, 0) + 1
    return ", ".join("%s=%s" % (region, count) for region, count in sorted(counts.items()))
