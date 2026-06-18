from collections import Counter
from datetime import datetime
from pathlib import Path

from .db import all_items, latest_snapshots
from .timeutil import iso_utc, week_id


ACTIVE_STATUSES = {"모집중", "접수중", "공고중", "정정공고중"}


def build_report(conn):
    items = all_items(conn)
    active = [item for item in items if item.get("status") in ACTIVE_STATUSES]
    top_items = sorted(items, key=_priority)[:12]
    status_counts = Counter(item.get("status") or "상태없음" for item in items)
    region_counts = Counter(item.get("region") or "지역없음" for item in items)
    snapshots = latest_snapshots(conn, 5)

    lines = [
        "# %s 청약 주택 관심 리포트" % week_id(),
        "",
        "- 생성시각: `%s`" % iso_utc(),
        "- 전체 공고: `%d`" % len(items),
        "- 모집/접수/공고중: `%d`" % len(active),
        "",
        "## 먼저 볼 것",
        "",
    ]

    if top_items:
        lines.append("| 제목 | 기관 | 유형 | 지역 | 상태 | 게시일 | 마감일 | 중요도 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for item in top_items:
            lines.append(
                "| [%s](%s) | %s | %s | %s | %s | %s | %s | %s |"
                % (
                    _escape_table(item.get("title")),
                    item.get("url") or "",
                    item.get("agency") or "",
                    item.get("category") or "",
                    item.get("region") or "",
                    item.get("status") or "",
                    item.get("published_at") or "",
                    item.get("deadline_at") or "",
                    item.get("importance") or 0,
                )
            )
    else:
        lines.append("아직 수집된 공고가 없습니다.")

    lines.extend(["", "## 상태 요약", ""])
    for status, count in status_counts.most_common():
        lines.append("- `%s`: %d" % (status, count))

    lines.extend(["", "## 지역 요약", ""])
    for region, count in region_counts.most_common():
        lines.append("- `%s`: %d" % (region, count))

    lines.extend(["", "## 최근 수집 스냅샷", ""])
    for snapshot in snapshots:
        lines.append(
            "- `%s` `%s` items=%s path=%s"
            % (
                snapshot.get("fetched_at"),
                snapshot.get("source_id"),
                snapshot.get("item_count"),
                snapshot.get("raw_path"),
            )
        )

    lines.extend(
        [
            "",
            "## 주의",
            "",
            "이 리포트는 로컬 수집 데이터 기준입니다. 실제 신청 전에는 반드시 공식 링크의 원문 공고를 확인하세요.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(conn):
    report_text = build_report(conn)
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    weekly_path = reports_dir / ("%s.md" % week_id())
    latest_path = reports_dir / "latest.md"
    weekly_path.write_text(report_text, encoding="utf-8")
    latest_path.write_text(report_text, encoding="utf-8")
    return {"weekly": str(weekly_path), "latest": str(latest_path)}


def _escape_table(value):
    return (value or "").replace("|", "\\|").replace("\n", " ")


def _priority(item):
    active_rank = 0 if item.get("status") in ACTIVE_STATUSES else 1
    region_rank = _region_rank(item.get("region"))
    deadline = item.get("deadline_at") or "9999-99-99"
    return (active_rank, region_rank, -(item.get("importance") or 0), deadline, -(item.get("id") or 0))


def _region_rank(region):
    region = region or ""
    if "서울" in region:
        return 0
    if "경기" in region:
        return 1
    return 2
