# Operations

## Manual Refresh

Run this when Theo asks for fresh housing updates:

```powershell
python -m housing_watch collect
python -m housing_watch report
python -m housing_watch render
python -m housing_watch export-image --width 430 --height 1200
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch news --source auto --limit 12 --width 645 --height 1500
python -m housing_watch issues --days 7 --limit 18 --per-page 6 --page 1 --width 645 --height 1500
python -m housing_watch desk --tab summary --width 645 --height 1500
python -m housing_watch review --width 390
```

When Theo says `이슈 뽑아줘`, run:

```powershell
python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500
```

Then report the grouped terminal summary and mention `site/ai-news.html` plus `reports/ai-news-page1.png`.

Run profile-filtered housing/summary outputs when Theo wants impossible housing notices hidden:

```powershell
$env:SIGNAL_DESK_PROFILE_PATH="D:\path\to\profile.md"
python -m housing_watch brief --width 390 --height 1500
python -m housing_watch desk --tab summary --width 645 --height 1500
python -m housing_watch desk --tab housing --width 645 --height 1500
```

Run this too when `SIGNAL_DESK_SARAMIN_KEY` is configured:

```powershell
python -m housing_watch jobs --fetch saramin --no-image
```

Generate all three AI briefing page images from the latest local AI news rows:

```powershell
python -m housing_watch issues --no-collect --days 7 --per-page 6 --page 1 --width 645 --height 1500 --image reports/ai-news-page1.png
python -m housing_watch issues --no-collect --days 7 --per-page 6 --page 2 --width 645 --height 1500 --image reports/ai-news-page2.png
python -m housing_watch issues --no-collect --days 7 --per-page 6 --page 3 --width 645 --height 1500 --image reports/ai-news-page3.png
python -m housing_watch issues --no-collect --days 7 --per-page 6 --page 1 --width 645 --height 1500 --no-image
```

## Development Verification

Run this before committing:

```powershell
python -m py_compile housing_watch\__main__.py housing_watch\cli.py housing_watch\db.py housing_watch\sources.py housing_watch\details.py housing_watch\render.py housing_watch\desk.py housing_watch\news.py housing_watch\ai_news.py housing_watch\ai_brief.py housing_watch\jobs.py housing_watch\review.py housing_watch\search.py
python -m unittest discover -s tests
python -m housing_watch collect
python -m housing_watch search "서울 행복주택 청년" --limit 3
python -m housing_watch context "이번 주 서울 행복주택에서 볼 만한 공고" --limit 3
python -m housing_watch report
python -m housing_watch render
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch news --source auto --limit 12 --width 645 --height 1500
python -m housing_watch issues --days 7 --limit 18 --per-page 6 --width 645 --height 1500
python -m housing_watch jobs --input config/jobs.example.json --no-image
python -m housing_watch desk --tab summary --width 645 --height 1500
python -m housing_watch desk --tab housing --width 645 --height 1500
python -m housing_watch desk --tab weekly-news --width 645 --height 1500
python -m housing_watch desk --tab jobs --width 645 --height 1500
python -m housing_watch desk --tab summary --profile "D:\path\to\profile.md" --width 645 --height 1500
python -m housing_watch review --width 390
```

When a Saramin key is available, also run:

```powershell
python -m housing_watch jobs --fetch saramin --no-image
```

## Troubleshooting

### Collection returns zero items

Likely causes:

- source HTML changed,
- source site is down,
- parser no longer matches table structure.

Actions:

- inspect newest file under `data/raw/`,
- update parser in `housing_watch/sources.py`,
- add or update parser tests.

### Brief image export fails

Likely causes:

- Edge/Chrome is not installed in expected Windows paths,
- browser headless mode changed.

Actions:

- inspect `_find_browser()` in `housing_watch/render.py`,
- run `python -m housing_watch brief --no-image` to isolate HTML generation.

### News collection falls back from GDELT

Likely cause:

- GDELT returned HTTP 429 or temporarily rejected the query.

Actions:

- keep `--source auto` so the command falls back to Korean Google News RSS,
- wait before retrying GDELT because the service asks clients to limit request frequency,
- use `--source google-news` when a Korean briefing is more important than original article URLs,
- configure `--translate-url` with a LibreTranslate-compatible endpoint if non-Korean GDELT titles should be translated automatically.

### Jobs tab is empty

Likely causes:

- no normalized jobs JSON has been imported yet,
- a future API adapter failed before writing `job_items`,
- imported records were missing company, posting title, or URL.

Actions:

- run `python -m housing_watch jobs --input config/jobs.example.json --no-image` to verify the pipeline,
- set `SIGNAL_DESK_SARAMIN_KEY` before running `python -m housing_watch jobs --fetch saramin --no-image`,
- inspect `data/raw/jobs/` for the latest raw snapshot,
- validate that each record has 회사명, 공고명, 하는일, 자격요건, 우대사항, 지역, 10년차 연봉, 마감일, and 링크.

### AI briefing is empty or thin

Likely causes:

- one or more RSS/Atom feeds are temporarily unavailable,
- GitHub release feeds have no recent releases,
- Google News RSS throttled or changed its response,
- a source moved its feed URL.

Actions:

- rerun with `python -m housing_watch issues --days 7 --limit 18 --per-page 6 --no-image` and inspect source warnings,
- inspect the latest raw bundle under `data/raw/ai_news/`,
- update `housing_watch/ai_news.py` source URLs or parsing tests when a feed structure changes,
- use `--no-collect` to re-render the last good local rows while debugging collection.

### Saramin live fetch fails

Likely causes:

- `SIGNAL_DESK_SARAMIN_KEY` is not set,
- the API key is not approved yet,
- the daily API limit was exceeded,
- query params in `config/job_sources.json` are invalid.

Actions:

- verify the key in the current shell with `$env:SIGNAL_DESK_SARAMIN_KEY`,
- run with a narrow keyword first, for example `python -m housing_watch jobs --fetch saramin --keyword "C++ 엔진" --no-image`,
- inspect the raw snapshot under `data/raw/jobs/` when the request succeeds,
- keep API keys out of git and `.env` out of commits.

### Review fails on region scope

Likely causes:

- source params changed,
- stale records from old source ids remain,
- config interest regions changed.

Actions:

- run `python -m housing_watch collect`,
- inspect `config/sources.json`,
- inspect `prune_items_outside_sources` and `prune_items_outside_regions`.

### Profile-filtered housing tab is empty

Likely causes:

- all current notices are clear mismatches for the supplied profile,
- the profile parser misread income, assets, birth date, or household status,
- annual eligibility limits changed after the static 2026 기준 was added.

Actions:

- rerun with `--show-profile-excluded` to inspect hidden-card reasons,
- verify the profile path with `$env:SIGNAL_DESK_PROFILE_PATH`,
- inspect `housing_watch/housing_profile.py` and update thresholds/tests when official limits change.

## Recurring Automation Draft

Use after Theo chooses a schedule:

```text
매주 월요일 오전에 Signal Desk 주택 데이터를 갱신해줘.
C:\Users\Theo\Documents\issue 에서 collect, report, render, export-image, brief, review를 실행하고,
review가 실패하면 실패 항목을 고친 뒤 다시 검증해줘.
최종 결과는 reports/brief.png 와 search/context 요약을 기준으로 알려줘.
```
