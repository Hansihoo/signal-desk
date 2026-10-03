# Handoff

This document is the first stop for a future Codex agent.

## Project Summary

Signal Desk is a local-first update collection and briefing system.

The long-term goal is to collect multiple categories of important updates for Theo: housing, jobs, AI/IT, stocks, and policy. The current implementation has the first housing MVP, a weekly big-news MVP, an AI developer-news MVP, and a jobs briefing/import MVP.

## Current State

Implemented:

- official-source housing collector,
- raw HTML snapshot storage,
- SQLite normalized storage,
- detail-page enrichment,
- optional local-profile housing filtering,
- local search/context output,
- Markdown report generation,
- mobile HTML rendering,
- PNG image export,
- tabbed mobile desk rendering,
- weekly big-news collection with GDELT-first and Korean Google News RSS fallback,
- AI developer news collection with OpenAI, Hugging Face, GitHub release feeds, and Google News AI search fallback,
- `issues` command for Theo's `이슈 뽑아줘` request, scoped to the latest 7 days by default,
- 3-page expandable AI Developer Brief rendering,
- career job JSON import, normalized `job_items`, and jobs tab rendering,
- Saramin Open API live job fetch when `SIGNAL_DESK_SARAMIN_KEY` is configured,
- automated review command,
- searchable public dashboard and dated briefing archive at https://hansihoo.github.io/signal-desk/,
- multi-topic research homepage, independent topic pages, and configurable public RSS/Atom research feeds,
- daily GitHub Actions collection and Pages deployment with durable release snapshots,
- tests for parsers, detail extraction, rendering, and review checks.

Current source scope:

- Seoul Housing Portal LH public lease list for Seoul.
- Seoul Housing Portal LH public lease list for Gyeonggi.
- Seoul Housing Portal SH public lease list for Seoul.

Current generated output:

- `site/index.html`, `site/library.json`, `site/status.json`
- `site/topics.json` and `site/research/<topic-id>/index.html`
- `site/archive/YYYY-MM-DD/briefing.json` and `index.html`
- `site/brief.html`
- `reports/brief.png`
- `site/desk.html`
- `reports/desk-summary.png`
- `reports/desk-weekly-news.png`
- `reports/desk-jobs.png`
- `site/ai-news.html`
- `reports/ai-news-page1.png`
- `reports/ai-news-page2.png`
- `reports/ai-news-page3.png`

These are ignored by git and should be regenerated locally.

## Most Important Commands

```powershell
python -m housing_watch collect
python -m housing_watch publish --collect
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch news --source auto --limit 12 --width 645 --height 1500
python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500
python -m housing_watch ai-news --limit 18 --per-page 6 --width 645 --height 1500
python -m housing_watch jobs --input config/jobs.example.json --no-image
python -m housing_watch desk --tab summary --width 645 --height 1500
python -m housing_watch desk --tab jobs --width 645 --height 1500
python -m housing_watch review --width 390
python -m unittest discover -s tests
```

When `SIGNAL_DESK_SARAMIN_KEY` is configured:

```powershell
python -m housing_watch jobs --fetch saramin --no-image
```

## Current Product Decisions

- The public product is a main research library containing extensible topics. Existing AI/housing/news are initial examples.
- Add topic metadata and RSS/Atom feeds in `config/research_topics.json`; see `RESEARCH_HUB.md` for the contract and hosting limits.
- No public accounts, user-input forms, or analytics SDKs are required. The hosting provider still records security access logs.

- SQLite is the source of truth.
- Markdown/HTML/PNG are generated outputs.
- If price is not available from official HTML, show `원문/PDF 확인`.
- Do not infer eligibility or price from incomplete text.
- Optional housing profile filtering is conservative: hide only clear mismatches and keep ambiguous cases visible.
- Theo's private profile file is an input path or environment variable, not repository data.
- Housing cards must be useful without opening every link.
- The concise mobile image width is capped at `390px`.
- The tabbed desk is wider by default at `645px`; the concise `brief` remains `390px`.
- Housing desk cards use a longer snapshot layout for location, area, supply, price, schedule, conditions, and profile notes.
- Current housing scope is Seoul and Gyeonggi only.
- The tabbed desk separates `summary`, `housing`, and `weekly-news`; only the selected tab is visible in exported images.
- The weekly big-news collector stores Korean briefing fields in `news_items`.
- AI developer news also uses `news_items`, but source ids are scoped with the `ai_` prefix and rendered separately through `site/ai-news.html`.
- When Theo says `이슈 뽑아줘`, run `python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500`, then summarize the grouped terminal output.
- AI Developer Brief cards are collapsed by default; title/summary are visible first, while impact/detail/action/source link appear after expanding.
- AI Developer Brief is always organized into three pages: model/platform, development/open-source, and research/flow.
- GDELT gives better original article URLs but can return HTTP 429. `--source auto` falls back to Korean Google News RSS.
- Real non-Korean machine translation requires an optional LibreTranslate-compatible endpoint through `--translate-url`.
- Career jobs use `job_items`; visible cards must stay limited to company, posting title, work, requirements, preferred qualifications, location, 10-year salary estimate, deadline, and link.
- `salary_10y` is separately researched and should keep its basis in `salary_basis`; do not infer salary without a basis.
- Saramin live collection requires `SIGNAL_DESK_SARAMIN_KEY`; the source defaults are in `config/job_sources.json`.

## Known Limitations

- SH notices often keep address, floor plan, detailed price, and unit breakdown in attached PDF/HWP files.
- LH pages expose useful address/area/supply data in HTML, but exact deposit/monthly rent often still requires the attached notice.
- The search scorer is semantic-lite, not embedding-based.
- Daily collection is active on GitHub Actions at approximately 08:17 Asia/Seoul; no separate local Codex automation is required.
- Public feed collection and dated briefings are implemented; independent deep research and cross-topic analysis remain future work.
- See `PUBLISHING.md` for state recovery, public-data boundaries, manual refresh, and pausing the workflow. Two cloud runs verified restore, accumulation, and deployment on 2026-10-03.
- The Python package is still named `housing_watch` because the first MVP domain is housing.
- Saramin list API does not expose full detailed responsibilities/requirements/preferred qualifications, so the adapter summarizes list fields and links to the original posting.
- WorkNet and official company career-page adapters are not implemented yet.
- Profile filtering uses static 2026 기준 values in `housing_watch/housing_profile.py`; update these when official annual limits change.
- AI source feeds are pragmatic RSS/Atom inputs. If OpenAI, Hugging Face, GitHub, or Google News changes feed shape, update `housing_watch/ai_news.py` and `tests/test_ai_news.py`.

## Next Best Work

1. Add PDF extraction for official notice attachments.
2. Add a source adapter for MyHome or 청년안심주택.
3. Add WorkNet and official company career-page adapters for `job_items`.
4. Add a source type for n8n/changedetection webhook imports.
5. Monitor the GitHub collection workflow; add separate Codex deep-research automation only when a distinct analysis task is requested.
6. Integrate `news_items` into search/context if Theo wants to ask Codex detailed questions across all domains.
7. Add optional Korean translation/summarization for non-Korean AI titles when a local or configured model is available.
8. Generalize package naming now that housing is no longer the only domain.
9. Move profile eligibility thresholds into a versioned config or collected official reference table.
