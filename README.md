# Signal Desk

Signal Desk is a local-first personal signal dashboard.

It collects updates Theo cares about, stores them in a searchable local database, and turns them into concise mobile briefings that Codex can explain later.

Current MVP domain: **housing subscription and public rental notices** for Seoul and Gyeonggi.

Future domains:

- IT and AI news
- jobs and hiring notices
- stocks and disclosures
- youth housing and public policy updates

## Current Capabilities

- Collect Seoul/Gyeonggi housing notices from official public housing pages.
- Keep raw HTML snapshots for audit and parser recovery.
- Normalize notices into SQLite.
- Enrich cards from detail pages when official HTML exposes address, area, supply, eligibility, and schedule.
- Search locally from Codex-friendly commands.
- Generate Markdown reports.
- Generate mobile HTML briefings.
- Export mobile PNG briefing images with a fixed width.
- Run a self-review command before treating output as ready.

## Quick Start

```powershell
python -m housing_watch collect
python -m housing_watch search "서울 행복주택 청년" --limit 3
python -m housing_watch context "이번 주 서울 행복주택에서 볼 만한 공고" --limit 3
python -m housing_watch report
python -m housing_watch render
python -m housing_watch export-image --width 430 --height 1200
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch review --width 390
python -m unittest discover -s tests
```

Generated local outputs:

- DB: `data/housing_watch.sqlite`
- raw snapshots: `data/raw/`
- Markdown report: `reports/latest.md`
- full mobile HTML: `site/latest.html`
- full mobile image: `reports/latest.png`
- concise mobile HTML: `site/brief.html`
- concise mobile image: `reports/brief.png`

Generated files are ignored by git. Recreate them with the commands above.

## Repository Map

```text
AGENTS.md                Codex working rules for this repo
PROJECT_STATUS.md        Current feature progress ledger
config/sources.json      Enabled sources and interest scope
housing_watch/           Current MVP Python package
tests/                   Parser, detail extraction, render, and review tests
docs/                    Architecture, handoff, roadmap, operations, data model
data/raw/.gitkeep        Placeholder for local raw snapshots
reports/.gitkeep         Placeholder for local reports/images
site/.gitkeep            Placeholder for local HTML output
```

## Documentation Index

- [Handoff](docs/HANDOFF.md): where to start when another Codex resumes work.
- [Features](docs/FEATURES.md): what exists now and how each feature behaves.
- [Roadmap](docs/ROADMAP.md): planned expansion beyond housing notices.
- [Architecture](docs/ARCHITECTURE.md): pipeline shape and module responsibilities.
- [Data Model](docs/DATA_MODEL.md): SQLite fields and output contracts.
- [Operations](docs/OPERATIONS.md): commands, verification, and automation loop.
- [Sources](docs/SOURCES.md): current official sources and candidate sources.
- [MVP Goals](docs/MVP_GOALS.md): completion criteria for the housing MVP.

## Important Product Rule

Markdown and HTML are outputs. SQLite is the source of truth.

```text
sources
-> raw snapshots
-> normalized SQLite
-> search/context
-> report/HTML/image
-> Codex explanation
```

## Current Housing MVP Notes

Signal Desk currently focuses on Seoul and Gyeonggi housing notices.

The concise card should help Theo decide whether to open the official notice without asking follow-up questions. Each card attempts to show:

- status and D-day
- title
- address
- area in square meters and pyeong
- supply count
- price or `원문/PDF 확인`
- eligibility/conditions
- agency, category, region, and schedule

Some official pages expose price only inside PDF/HWP files. In that case, Signal Desk does not guess; it marks the field as `원문/PDF 확인`.

## Requirements

- Python 3.8+
- Windows Edge or Chrome for image export
- No Python package dependencies for the current MVP

