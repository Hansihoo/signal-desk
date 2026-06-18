# Roadmap

## Product Direction

Signal Desk should become Theo's personal update desk:

```text
fixed sources + broad research
-> local searchable database
-> Codex answers
-> mobile briefings
```

## Phase 1: Housing MVP

Status: Done.

- Seoul/Gyeonggi housing notices.
- SQLite local store.
- Search/context.
- Mobile card briefing.
- PNG export.
- Review loop.

## Phase 2: Better Housing Detail Quality

Goal: reduce "원문/PDF 확인" fields.

Candidate work:

- extract official PDF/HWP attachment URLs,
- parse PDFs for price tables and unit details,
- add per-complex cards when one notice contains many complexes,
- include application method and document submission window,
- add "must act by" field separate from official closing date.

## Phase 3: Automation

Goal: make weekly collection/reporting automatic.

Candidate work:

- create Codex weekly automation,
- optionally add n8n for fixed source polling,
- optionally add changedetection.io for pages without stable APIs,
- store automation run logs.

## Phase 4: Jobs

Candidate work:

- add source adapter for selected company career pages,
- add source adapter for search URLs from Saramin/JobKorea/Wanted when allowed,
- normalize fields: company, role, location, stack, deadline, apply URL.

## Phase 5: IT and AI News

Candidate work:

- RSS adapters for official blogs,
- Hacker News/API source,
- GitHub releases/trending source,
- summarize updates into "why Theo should care".

## Phase 6: Stocks and Disclosures

Candidate work:

- OpenDART adapter,
- KRX/public data adapter,
- normalize fields: ticker, company, disclosure type, date, risk/opportunity note,
- keep strict source attribution.

