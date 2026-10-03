# Automation Plan

## Active implementation direction

GitHub Actions performs daily public-source collection at 08:17 Asia/Seoul and deploys
GitHub Pages. Release assets preserve SQLite and dated briefings between runners.
See `PUBLISHING.md` and `PROJECT_STATUS.md` for setup and verification status. The Codex/n8n
prompts below remain optional alternatives for separate local or deeper analysis work.

This is the automation plan for Signal Desk's current housing MVP.

## MVP Manual Loop

```powershell
python -m housing_watch collect
python -m housing_watch report
python -m housing_watch render
python -m housing_watch export-image
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch review --width 390
```

## Codex Automation Prompt Draft

Use this after the MVP is verified and Theo wants a recurring Codex automation:

```text
매주 월요일 오전에 Signal Desk workspace에서 청약 주택 데이터를 수집하고,
검색 인덱스와 리포트를 갱신한 다음, 이번 주 신규/모집중/마감임박 공고를 요약해줘.
실행 명령은 python -m housing_watch collect, report, render, export-image, brief --limit 5 --width 390 --height 1500, review --width 390 순서로 사용해.
결과는 reports/latest.md, site/latest.html, reports/latest.png, site/brief.html, reports/brief.png 를 기준으로 설명해줘.
review가 실패하면 실패 항목을 먼저 고치고 다시 검증해줘.
```

## n8n Integration Later

n8n should be used when a fixed source needs frequent monitoring.

Suggested division:

- n8n: fixed source polling, webhooks, changedetection notifications.
- Housing Watch: normalized storage, search, report, HTML/image rendering.
- Codex: interpretation, prioritization, and answering Theo's questions.

Future webhook ingestion shape:

```json
{
  "source_id": "n8n_custom_source",
  "title": "공고 제목",
  "url": "https://example.com/notice",
  "agency": "기관명",
  "category": "행복주택",
  "region": "서울",
  "status": "모집중",
  "published_at": "2026-06-18",
  "deadline_at": "2026-07-01",
  "raw_text": "원문 또는 변경 내용"
}
```

## API-Key Sources

Public data APIs should remain optional. Add required environment variables to docs before enabling them.

Example:

```powershell
$env:DATA_GO_KR_SERVICE_KEY="..."
python -m housing_watch collect --source lh_openapi_lease_notice
```
