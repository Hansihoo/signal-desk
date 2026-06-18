# Handoff

This document is the first stop for a future Codex agent.

## Project Summary

Signal Desk is a local-first update collection and briefing system.

The long-term goal is to collect multiple categories of important updates for Theo: housing, jobs, IT, stocks, and policy. The current implementation only covers the first MVP: Seoul/Gyeonggi housing subscription and public rental notices.

## Current State

Implemented:

- official-source housing collector,
- raw HTML snapshot storage,
- SQLite normalized storage,
- detail-page enrichment,
- local search/context output,
- Markdown report generation,
- mobile HTML rendering,
- PNG image export,
- automated review command,
- tests for parsers, detail extraction, rendering, and review checks.

Current source scope:

- Seoul Housing Portal LH public lease list for Seoul.
- Seoul Housing Portal LH public lease list for Gyeonggi.
- Seoul Housing Portal SH public lease list for Seoul.

Current generated output:

- `site/brief.html`
- `reports/brief.png`

These are ignored by git and should be regenerated locally.

## Most Important Commands

```powershell
python -m housing_watch collect
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch review --width 390
python -m unittest discover -s tests
```

## Current Product Decisions

- SQLite is the source of truth.
- Markdown/HTML/PNG are generated outputs.
- If price is not available from official HTML, show `원문/PDF 확인`.
- Do not infer eligibility or price from incomplete text.
- Housing cards must be useful without opening every link.
- The concise mobile image width is capped at `390px`.
- Current housing scope is Seoul and Gyeonggi only.

## Known Limitations

- SH notices often keep address, floor plan, detailed price, and unit breakdown in attached PDF/HWP files.
- LH pages expose useful address/area/supply data in HTML, but exact deposit/monthly rent often still requires the attached notice.
- The search scorer is semantic-lite, not embedding-based.
- No recurring automation has been registered yet.
- The Python package is still named `housing_watch` because the first MVP domain is housing.

## Next Best Work

1. Add PDF extraction for official notice attachments.
2. Add a source adapter for MyHome or 청년안심주택.
3. Generalize package naming once a second domain is implemented.
4. Add a source type for n8n/changedetection webhook imports.
5. Add recurring Codex automation after Theo chooses a schedule.

