# Housing MVP Goals

This document describes the current housing MVP inside Signal Desk.

## Objective

청약 주택 MVP는 Theo가 Codex에게 “요즘 볼 만한 청약/공공임대 소식 알려줘”라고 물었을 때, 이미 수집된 로컬 데이터에서 빠르게 답하고 모바일로 전달 가능한 간결한 시각 자료를 만들 수 있어야 한다.

## In Scope

- 공식 소스에서 청약/공공임대 공고 수집.
- 원본 스냅샷 보관.
- SQLite 정규화 저장.
- Codex 질문용 검색/context 출력.
- Markdown 리포트 생성.
- 모바일용 간결 HTML 브리핑 생성.
- 모바일 전달용 PNG 이미지 추출.
- 개발 후 자동 검토 명령으로 품질 확인.

## Out of Scope for MVP

- 모든 주택 공고 사이트 완전 커버.
- 유료 API 또는 비공개 세션이 필요한 수집.
- 투자/청약 당첨 가능성 판단.
- 사용자 개인정보 기반 자격 판정 자동화.
- 운영 서버 배포.

## Done Criteria

MVP 작업은 아래 항목이 모두 통과해야 완료로 본다.

```powershell
python -m housing_watch collect
python -m housing_watch search "서울 행복주택 청년" --limit 3
python -m housing_watch context "이번 주 서울 행복주택에서 볼 만한 공고" --limit 3
python -m housing_watch report
python -m housing_watch render
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch review --width 390
python -m unittest discover -s tests
```

## Development Loop

Every meaningful change should follow this loop:

```text
Develop
-> Run tests
-> Generate concise briefing
-> Run review
-> Inspect image if UI changed
-> Fix issues
-> Repeat until review passes
```

Do not treat a feature as complete just because code was written. It is complete only when data, search, report, HTML, image, and review checks all pass for the relevant scope.

## Mobile Briefing Rules

- Default concise image width: `390px`.
- Default concise image height: `1500px`.
- Default concise card count: `5`.
- Cards must prioritize active notices before closed notices.
- Each card should show status, D-day, title, address, area, supply, price, eligibility, agency, category, region, and schedule.
- Long titles must wrap inside the card.
- HTML must include a mobile viewport.
- PNG width must not exceed the requested width.
