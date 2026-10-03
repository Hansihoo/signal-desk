# Architecture

## Intent

Signal Desk is a local-first research pipeline. It prepares important updates before Theo asks Codex questions.

The first implemented domain is housing notices. The architecture should stay broad enough for jobs, IT news, stocks, and policy updates.

The source of truth is SQLite, not Markdown.

```text
Official sources / fixed watches / future APIs
  -> source adapters
  -> raw snapshots
  -> normalized SQLite items
  -> search/context commands
  -> Markdown report
  -> mobile HTML briefing
  -> optional PNG export
```

## Core Design

### Source Adapters

Each source adapter fetches one source and normalizes rows into a shared item shape.

Current adapter:

- `seoul_housing_table`: parses Seoul Housing Portal table pages for LH/SH notices.
- `weekly_news`: tries GDELT DOC 2.0, then falls back to Korean Google News RSS for weekly big-news candidates.
- `ai_news`: collects AI developer news from RSS/Atom feeds and a Google News AI search fallback.
- `manual_jobs_json`: imports normalized career job candidates from JSON until API/company adapters are added.
- `jobs_saramin`: fetches senior career job candidates from Saramin Open API when `SIGNAL_DESK_SARAMIN_KEY` is configured.

Future adapters:

- `lh_openapi`: public data API for LH notices.
- `myhome_openapi`: public housing recruitment notices from MyHome.
- `changedetection_webhook`: changes detected from pages without stable APIs.
- `n8n_webhook`: records pushed from n8n workflows.
- `rss_reader_import`: entries imported from Miniflux/FreshRSS/Newscope-style source managers.
- `jobs_worknet`, `jobs_company_careers`: future job source adapters that should emit the existing `job_items` shape.
- `news_rss`: future IT/news RSS source adapter.
- `opendart`: future Korean disclosure source adapter.

### Storage

`data/housing_watch.sqlite` stores the current MVP data:

- `items`: normalized notices.
- `news_items`: normalized weekly big-news candidates.
- `news_items` rows with `ai_` source ids: normalized AI developer news candidates.
- `job_items`: normalized career job candidates with Theo-facing card fields and salary estimate fields.
- `raw_snapshots`: fetch metadata and raw snapshot paths.
- `items_fts`: optional FTS5 search index when SQLite supports it.

Markdown and HTML are regenerated from the database.

### Search

Search is hybrid:

- SQLite FTS5 when available.
- Lightweight semantic scoring based on token overlap and Korean character n-grams.

The semantic-lite scorer is intentionally dependency-free. Later, it can be replaced or supplemented with embeddings.

### Reporting

Reports are derived outputs:

- `reports/YYYY-WW.md`: weekly Markdown report.
- `reports/latest.md`: latest Markdown report copy.
- `site/latest.html`: mobile-first visual briefing.
- `reports/latest.png`: optional screenshot output.
- `site/brief.html`: concise mobile briefing for sharing.
- `reports/brief.png`: concise mobile image capped to the requested width.
- `site/desk.html`: tabbed mobile desk with important summary, housing, and future weekly news tabs.
- `reports/desk-*.png`: selected-tab screenshots for mobile sharing, including `desk-jobs.png`.
- `site/ai-news.html`: 3-page expandable AI Developer Brief.
- `reports/ai-news-page*.png`: selected AI briefing page screenshots.

### Review Loop

`python -m housing_watch review --width 390` checks whether the generated data and concise briefing are ready to share.

The review command intentionally focuses on operational quality:

- local DB has items,
- active notices exist,
- official links are present,
- concise HTML has a mobile viewport and max-width,
- long text has wrapping protection,
- concise card count stays small,
- PNG width does not exceed the mobile delivery width.

## Why This Shape

This follows the same broad pattern used by RSS readers, monitoring systems, and AI news curators:

```text
fetch -> normalize -> persist -> classify/search -> render/deliver
```

It keeps each piece replaceable. For example, n8n can later handle collection while this project keeps storage, search, and reporting.

## Public publishing and persistence

`research_topics.py` loads the topic registry from `config/research_topics.json` and
dispatches existing collectors or generic RSS/Atom feeds. The homepage is an all-topic
library; `research/<id>/index.html` provides independent topic pages. Public export uses
stable topic IDs and labels. Generic feeds store excerpts without AI-specific interpretation.
News deduplication uses explicit source groups to preserve repeated titles across topics.
Daily snapshots retain their original catalog as well as records; older JSON stays unchanged.

The public shell is split into `public_site.html`, `public_site.css`, and `public_site.js`.
Its left outline navigates main, topic, category, and source-note document views. Categories
and report IDs use query parameters on existing topic pages, avoiding an HTML file per record.
Archived query routes render only saved items. Shared assets use relative root paths and
content-hash cache keys. Review/conclusion document sections are pending placeholders.

`public_site.py` adds public-source refresh and a static searchable dashboard. Only
selected AI/news/housing fields enter the public library; local job/profile data is excluded.
Daily JSON briefing snapshots under `site/archive/` preserve the first successful briefing
for each Korean date. Historical HTML is rebuilt from those saved snapshots.

GitHub Actions restores accumulated state from monthly GitHub Release assets, refreshes
public sources, runs validation, saves a new immutable state asset, and deploys a Pages artifact.
`cloud_state.py` validates restore paths, backs up SQLite consistently, and records monthly
successful operations. Generated data never enters source commits. See `PUBLISHING.md`.

## Naming Note

The repo is `signal-desk`, but the current Python package is still `housing_watch` because the first MVP domain was housing. Jobs, weekly news, and AI news now share that package. Rename or generalize it only when the import/CLI churn is worth the cleanup.
