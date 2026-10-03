# Tabbed Briefing

Signal Desk can now render a tabbed mobile briefing that separates domains while keeping one shareable HTML surface.

## Command

```powershell
python -m housing_watch news --source auto --limit 12 --width 645 --height 1500
python -m housing_watch desk --tab summary --width 645 --height 1500
python -m housing_watch desk --tab housing --width 645 --height 1500
python -m housing_watch desk --tab weekly-news --width 645 --height 1500
python -m housing_watch desk --tab jobs --width 645 --height 1500
```

Outputs:

- HTML: `site/desk.html`
- PNG: `reports/desk-summary.png`, `reports/desk-housing.png`, `reports/desk-weekly-news.png`, or `reports/desk-jobs.png`

Use `--no-image` to render HTML only.

## Tabs

- `summary`: the important-only view across available domains. It currently mixes career jobs, top weekly news, and urgent housing notices.
- `housing`: the Seoul/Gyeonggi housing notice view with a wider visual snapshot for address, area, supply, and price, followed by condition, agency, region, schedule, profile note, and review point.
- `weekly-news`: broad weekly big news cards from `news_items`. The MVP tries GDELT first and falls back to Korean Google News RSS.
- `jobs`: career job cards from `job_items` with company, posting title, work, requirements, preferred qualifications, location, 10-year salary estimate, deadline, and link target.

## Export Model

The HTML includes all tabs, but only the selected tab is active when the file is rendered. Headless browser screenshot export captures that active state, so the resulting image contains the selected tab content rather than every domain at once.

Default desk image width is `645px` for wider mobile HTML viewing and selected-tab image export.

## Design Contract

- The desk should feel like a concise mobile document: masthead, issue metadata, compact table-like metrics, and article-style notice blocks.
- Keep the first viewport as the usable briefing, not a landing page.
- Do not mix unrelated domains in the same card list.
- Keep each card self-contained enough that Theo can decide whether to ask Codex a follow-up.
- Keep generated HTML/PNG ignored by git.
- Feed important weekly news items back into the `summary` tab.
