# Weekly Big News Tool Research

This note records the first pass for adding a broad weekly news tab to Signal Desk.

## Recommendation

Do not start with a custom crawler.

Use a layered approach:

```text
broad public news data
-> RSS/feed source management
-> local normalization
-> dedupe and scoring
-> Signal Desk tabs and image export
```

For the first implementation, use GDELT as the broad candidate source and keep RSS tooling patterns available for fixed-source follow-up.

Implementation note: the current MVP tries GDELT first, but falls back to Korean Google News RSS when GDELT is rate-limited. Google News RSS is practical for Korean cards, but it is not the same as an official publisher API.

## Candidate Tools

### GDELT

- Site: <https://www.gdeltproject.org/>
- Data/API page: <https://www.gdeltproject.org/data.html>
- DOC 2.0 API note: <https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/>
- Why it matters: realtime open news data with JSON APIs, plus the Global Frontpage Graph that tracks homepage placement across many major outlets.
- Fit for Signal Desk: good first source for "what was broadly important this week" candidates.
- Caution: broad global data can be noisy. Signal Desk should score, dedupe, and keep links/source attribution.

### Media Cloud

- Site: <https://www.mediacloud.org/>
- Why it matters: open-source media research tooling built around a large global news database.
- Fit for Signal Desk: useful for research-grade aggregation and analysis when a stronger media dataset is needed.
- Caution: likely heavier than the first MVP tab. Treat as a candidate for phase two after GDELT proves useful.

### Miniflux

- Site: <https://miniflux.app/>
- API docs: <https://miniflux.app/docs/api.html>
- Why it matters: small self-hosted RSS reader with an API and token authentication.
- Fit for Signal Desk: good source manager if Theo later chooses fixed news/blog feeds.

### FreshRSS

- GitHub: <https://github.com/FreshRSS/FreshRSS>
- Website scraping docs: <https://freshrss.github.io/FreshRSS/en/users/11_website_scraping.html>
- Why it matters: RSS aggregator that can create feeds from pages without RSS using XPath/JSON scraping.
- Fit for Signal Desk: useful for sites that do not expose RSS, without writing one-off scrapers first.

### Newscope

- GitHub: <https://github.com/umputun/newscope>
- Why it matters: self-hosted RSS reader that scores articles with AI, extracts topics, learns from feedback, and can output filtered feeds.
- Fit for Signal Desk: useful reference for scoring, topic extraction, and feedback loops.

### Google News RSS fallback

- URL shape: `https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko`
- Why it matters: quickly returns Korean top-news candidates without an API key.
- Fit for Signal Desk: useful fallback when GDELT returns HTTP 429 and the immediate goal is a Korean mobile briefing.
- Caution: links may go through Google News rather than the original article URL. The RSS item exposes publisher name and often publisher homepage, but not always a direct article URL.

### LibreTranslate

- Docs: <https://docs.libretranslate.com/>
- Why it matters: open-source machine translation API compatible with self-hosting.
- Fit for Signal Desk: optional translation layer for non-Korean GDELT titles.
- Caution: public hosted instances may need API keys or have limits. A self-hosted endpoint is better for recurring automation.

## Proposed Signal Desk Shape

```text
weekly news collector
-> raw snapshots under data/raw/news/
-> normalized news_items table or shared signals table
-> source frequency and frontpage/rank scoring
-> local search/context
-> desk weekly-news tab
-> summary tab gets only high-scoring items
```

## First News MVP

- Period: last 7 days.
- Categories: economy, politics, society, international, culture/entertainment, technology.
- Output: 5 mobile cards from up to 12 collected candidates, each with Korean title, category, date, expanded Korean note, and a hidden card-level article link.
- Scoring inputs: source frequency, frontpage placement when available, recency, category diversity, and manual interest keywords.
- Avoid: summarizing from a single low-quality source or showing unverified social rumors.
