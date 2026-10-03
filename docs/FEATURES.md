# Features

## Housing Notice Collection

Command:

```powershell
python -m housing_watch collect
```

What it does:

- fetches enabled official sources from `config/sources.json`,
- saves raw snapshots under `data/raw/`,
- parses table rows,
- follows official detail links,
- extracts detail fields when HTML exposes them,
- upserts normalized records into SQLite,
- removes disabled/renamed source records,
- removes records outside Seoul/Gyeonggi scope.

## Search and Codex Context

Commands:

```powershell
python -m housing_watch search "서울 행복주택 청년" --limit 3
python -m housing_watch context "이번 주 서울 행복주택에서 볼 만한 공고" --limit 3
```

Search returns human-readable lines.

Context returns structured source context for Codex answers. It includes address, area, supply, price status, eligibility, application period, summary, and official URL.

## Markdown Report

Command:

```powershell
python -m housing_watch report
```

Outputs:

- `reports/YYYY-WW.md`
- `reports/latest.md`

## Mobile HTML

Command:

```powershell
python -m housing_watch render
```

Output:

- `site/latest.html`

This is a fuller mobile dashboard.

## Concise Mobile Briefing

Command:

```powershell
python -m housing_watch brief --limit 5 --width 390 --height 1500
```

Outputs:

- `site/brief.html`
- `reports/brief.png`

The concise briefing is meant to be sent to a mobile device. It prioritizes active notices and shows decision fields directly in each card.

Optional profile filtering:

```powershell
python -m housing_watch brief --profile "D:\path\to\profile.md" --width 390 --height 1500
```

The profile file stays outside the repository. The filter hides only clearly impossible housing cards and keeps ambiguous cards visible with a short `프로필` reason.

## Weekly Big News

Command:

```powershell
python -m housing_watch news --source auto --limit 12 --width 645 --height 1500
```

What it does:

- tries GDELT DOC 2.0 first for original article URLs,
- falls back to a Korean Google News RSS bundle when GDELT is rate-limited or unavailable,
- combines Korean top news with the Korean Google News world section so global big news is represented,
- saves raw source responses under `data/raw/news/`,
- normalizes candidates into `news_items`,
- keeps Korean title/summary fields for the briefing,
- expands each visible summary with a short category-specific follow-up point,
- keeps source/publisher names out of the visible card to reduce clutter,
- ranks non-political news first and shows at most 2 politics cards in the weekly-news tab,
- renders the weekly-news tab and exports `reports/desk-weekly-news.png`.

Translation note:

- Korean RSS titles are stored directly as Korean briefing titles.
- Non-Korean GDELT titles can be translated through an optional LibreTranslate-compatible endpoint using `--translate-url`.
- Without a translation endpoint, non-Korean titles are preserved and the Korean summary remains title/category based.

## AI Developer News

Command:

```powershell
python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500
python -m housing_watch ai-news --limit 18 --per-page 6 --width 645 --height 1500
```

What it does:

- collects AI news from OpenAI News, Hugging Face Blog, selected GitHub release feeds, and a Google News AI/LLM search fallback,
- defaults the issue-pull workflow to the latest 7 days when Theo says `이슈 뽑아줘`,
- stores normalized records in `news_items` with `ai_` source ids,
- keeps raw feed snapshots under `data/raw/ai_news/`,
- classifies items into `LLM 모델`, `API/플랫폼`, `AI 개발`, `오픈소스`, `연구`, `안전`, or `시장/정책`,
- writes `site/ai-news.html`,
- exports the selected page image as `reports/ai-news-page{page}.png`,
- supports `--page 1`, `--page 2`, and `--page 3` for separate page screenshots,
- supports `--days N` so the rendered/reporting set stays scoped to the requested lookback window,
- supports `--no-collect` to re-render existing local AI news rows without hitting the network.

The HTML always has 3 pages:

- page 1: model/platform news,
- page 2: AI development and open-source news,
- page 3: research, safety, and market/policy signals.

Each card is collapsed by default. The visible state shows headline metadata, title, and developer summary. Expanding the card reveals developer impact, detail, suggested check, and the source link.

## Career Jobs

Command:

```powershell
python -m housing_watch jobs --input config/jobs.example.json --width 645 --height 1500
python -m housing_watch jobs --fetch saramin --width 645 --height 1500
```

What it does:

- imports normalized career job candidates from JSON,
- accepts Korean field names such as `회사명`, `공고명`, `하는일`, `자격요건`, `우대사항`, `지역`, `10년차 연봉`, `마감일`, and `링크`,
- stores records in `job_items`,
- keeps the original JSON snapshot under `data/raw/jobs/`,
- gives C++/engine/office/desktop career jobs a lightweight local fit score,
- fetches live Saramin candidates when `SIGNAL_DESK_SARAMIN_KEY` is set,
- filters out obvious new-grad postings and keeps configurable minimum-fit candidates,
- enriches `salary_10y` from a separate company salary estimate file when available,
- renders the `jobs` tab and exports `reports/desk-jobs.png`.

The visible card is intentionally narrow: company, posting title, work, requirements, preferred qualifications, location, 10-year salary estimate, deadline, and link target.

Live Saramin behavior:

- default keywords are in `config/job_sources.json`,
- default query excludes headhunting/dispatch postings through Saramin's `directhire` option,
- default query prioritizes listed-company postings with `stock=kospi,kosdaq`,
- API keys must be supplied through environment variables, never committed.

## Tabbed Signal Desk

Command:

```powershell
python -m housing_watch desk --tab summary --width 645 --height 1500
```

Outputs:

- `site/desk.html`
- `reports/desk-summary.png`

Other tab exports:

```powershell
python -m housing_watch desk --tab housing --width 645 --height 1500
python -m housing_watch desk --tab weekly-news --width 645 --height 1500
python -m housing_watch desk --tab jobs --width 645 --height 1500
```

The HTML contains tabs for important summary, housing, weekly big news, and career jobs. Screenshot export captures the selected active tab only.
The summary tab mixes career jobs, top weekly news cards, and the most urgent housing cards.
The housing tab uses a wider document-style card with a visual snapshot for location, area, supply, and price, then detailed schedule, condition, profile, and review-note rows.

Profile-filtered desk output:

```powershell
python -m housing_watch desk --tab summary --profile "D:\path\to\profile.md" --width 645 --height 1500
python -m housing_watch desk --tab housing --profile "D:\path\to\profile.md" --width 645 --height 1500
```

Use `--show-profile-excluded` when debugging hidden housing cards.

## Review

Command:

```powershell
python -m housing_watch review --width 390
```

Checks:

- DB has items.
- Active notices exist.
- Items have official links.
- Items stay in Seoul/Gyeonggi scope.
- Brief HTML exists.
- Brief HTML has mobile viewport.
- Brief HTML has max width.
- Long text wrapping is configured.
- Briefing remains concise.
- Decision labels are present.
- PNG exists.
- PNG width does not exceed requested width.
