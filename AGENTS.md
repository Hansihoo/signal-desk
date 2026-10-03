# Signal Desk Agent Instructions

## Project Goal

Signal Desk is Theo's local-first personal signal dashboard.

It collects important updates in advance, keeps them searchable for Codex, and renders concise mobile briefings. The first MVP domain is housing subscription/public rental notices for Seoul and Gyeonggi.

## Before Changing Code

Read these files first:

- `README.md`
- `docs/HANDOFF.md`
- `docs/ARCHITECTURE.md`
- `docs/MVP_GOALS.md`
- `PROJECT_STATUS.md`

Then state:

- goal
- work type
- impact scope
- risk
- verification plan

## Development Rules

- Keep the MVP incremental. Add one source or feature at a time.
- Prefer official sources first.
- Keep raw fetched data under `data/raw/`.
- Keep normalized data in SQLite. Markdown, HTML, and PNG are generated outputs.
- Do not commit generated DBs, raw snapshots, reports, PNGs, or HTML output.
- Do not hardcode API keys, cookies, sessions, or personal credentials.
- If a website structure changes, update parser logic and add or update tests.
- If UI or briefing changes, run `brief`, `review`, and inspect `reports/brief.png`.
- Update `PROJECT_STATUS.md` when feature status changes.
- Update `docs/ai/WORK_LOG.md` for meaningful implementation or verification work.
- Keep docs useful for a future Codex agent that cannot inspect your memory.

## Common Commands

```powershell
python -m housing_watch collect
python -m housing_watch search "서울 행복주택 청년" --limit 3
python -m housing_watch context "이번 주 서울 행복주택에서 볼 만한 공고" --limit 3
python -m housing_watch report
python -m housing_watch render
python -m housing_watch export-image --width 430 --height 1200
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch news --source auto --limit 12 --width 645 --height 1500
python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500
python -m housing_watch ai-news --limit 18 --per-page 6 --width 645 --height 1500
python -m housing_watch jobs --input config/jobs.example.json --no-image
python -m housing_watch desk --tab summary --width 645 --height 1500
python -m housing_watch desk --tab jobs --width 645 --height 1500
python -m housing_watch desk --tab summary --profile "D:\path\to\profile.md" --width 645 --height 1500
python -m housing_watch review --width 390
python -m unittest discover -s tests
```

## Theo Natural Requests

- When Theo says `이슈 뽑아줘`, treat it as: collect the latest 7 days of AI developer issues, render the 3-page AI Developer Brief, and report the grouped text summary.
- Default command:

```powershell
python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500
```

- If only refreshing from already collected rows, use `--no-collect`.
- Mention the generated `site/ai-news.html` and `reports/ai-news-page1.png` path in the final response.

## Completion Contract

A meaningful housing MVP change is not complete until:

- tests pass,
- data collection works,
- search/context output is usable,
- report/render output is generated,
- concise mobile briefing is generated,
- tabbed desk briefing is generated when a multi-topic or summary UI changed,
- `review` passes,
- image output is visually inspected when UI changed,
- docs/status are synchronized.

## Commit Messages

When creating commits for Theo, use Korean commit messages:

```text
[Tag] Korean summary

- Korean detail about what changed or was verified.
- Korean detail about support work or follow-up.
```
