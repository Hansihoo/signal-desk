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

