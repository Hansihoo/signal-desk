# Operations

## Manual Refresh

Run this when Theo asks for fresh housing updates:

```powershell
python -m housing_watch collect
python -m housing_watch report
python -m housing_watch render
python -m housing_watch export-image --width 430 --height 1200
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch review --width 390
```

## Development Verification

Run this before committing:

```powershell
python -m py_compile housing_watch\cli.py housing_watch\db.py housing_watch\sources.py housing_watch\details.py housing_watch\render.py housing_watch\review.py housing_watch\search.py
python -m unittest discover -s tests
python -m housing_watch collect
python -m housing_watch search "서울 행복주택 청년" --limit 3
python -m housing_watch context "이번 주 서울 행복주택에서 볼 만한 공고" --limit 3
python -m housing_watch report
python -m housing_watch render
python -m housing_watch brief --limit 5 --width 390 --height 1500
python -m housing_watch review --width 390
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

### Review fails on region scope

Likely causes:

- source params changed,
- stale records from old source ids remain,
- config interest regions changed.

Actions:

- run `python -m housing_watch collect`,
- inspect `config/sources.json`,
- inspect `prune_items_outside_sources` and `prune_items_outside_regions`.

## Recurring Automation Draft

Use after Theo chooses a schedule:

```text
매주 월요일 오전에 Signal Desk 주택 데이터를 갱신해줘.
C:\Users\Theo\Documents\issue 에서 collect, report, render, export-image, brief, review를 실행하고,
review가 실패하면 실패 항목을 고친 뒤 다시 검증해줘.
최종 결과는 reports/brief.png 와 search/context 요약을 기준으로 알려줘.
```

