# Sources

## Enabled in MVP

### Seoul Housing Portal - LH public lease list

- URL: `https://housing.seoul.go.kr/site/main/lh/publicLease/list`
- Notes: Static table, API key not required.
- Fields: type, title, region, published date, deadline, status, link.
- Scope: use `cnpCdNm=seoul` and `cnpCdNm=gg`; other regions are pruned from the local store.
- Detail page enrichment: address, area, supply units, eligibility, and schedule are extracted when present.

### Seoul Housing Portal - SH public lease list

- URL: `https://housing.seoul.go.kr/site/main/sh/publicLease/07/list`
- Notes: Static table, API key not required.
- Fields: type, title, published date, deadline, status, department, link.
- Region defaults to Seoul.
- Detail page enrichment: supply units, eligibility, and schedule are extracted when present. Some SH notices keep address/price/area only inside attached PDFs, so cards show `원문/PDF 확인` when HTML does not expose the value.

## Candidate Sources

### LH public data API

- Public Data Portal item: `한국토지주택공사_분양임대공고문 조회 서비스`
- Requires public data service key and usage approval.
- Use when stable production collection is needed.

### MyHome public housing notices

- MyHome public data/open page.
- Useful for national public housing recruitment notices.

### changedetection.io

- Use for pages without API/RSS.
- Send changes into this project through a webhook or exported JSON.

### GDELT weekly news

- Implemented candidate source for the weekly big-news tab.
- Use GDELT DOC/API or Global Frontpage Graph data to collect broad news candidates from the last 7 days.
- Best first use: candidate discovery and source-frequency scoring, not final truth by itself.
- Current behavior: `news --source auto` tries GDELT first. If GDELT returns HTTP 429, the command falls back to Korean Google News RSS.

### Google News RSS fallback

- URL: `https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko`
- Use only as a pragmatic fallback or Korean top-news briefing source.
- The RSS gives Korean titles, publisher name, and often publisher homepage URL.
- Article links may go through Google News instead of the original publisher article.

### AI developer news feeds

Implemented as:

```powershell
python -m housing_watch ai-news --limit 18 --per-page 6 --width 645 --height 1500
```

Primary feeds:

- OpenAI News RSS: `https://openai.com/news/rss.xml`
- Hugging Face Blog RSS: `https://huggingface.co/blog/feed.xml`
- vLLM releases: `https://github.com/vllm-project/vllm/releases.atom`
- llama.cpp releases: `https://github.com/ggml-org/llama.cpp/releases.atom`
- Ollama releases: `https://github.com/ollama/ollama/releases.atom`
- LangChain releases: `https://github.com/langchain-ai/langchain/releases.atom`
- LangGraph releases: `https://github.com/langchain-ai/langgraph/releases.atom`
- LlamaIndex releases: `https://github.com/run-llama/llama_index/releases.atom`
- LiteLLM releases: `https://github.com/BerriAI/litellm/releases.atom`
- promptfoo releases: `https://github.com/promptfoo/promptfoo/releases.atom`

Fallback discovery feed:

- Google News RSS search for major AI/LLM terms, limited to recent items with `when:7d`.

Notes:

- These feeds are used for developer-facing signal discovery, not as a canonical record of every AI event.
- Open-source release feeds can be noisy; ranking and page grouping keep model/platform, development/open-source, and research/flow separated.
- Feed structure changes should be fixed in `housing_watch/ai_news.py` with tests in `tests/test_ai_news.py`.

### RSS source managers

- Candidate tools: Miniflux, FreshRSS, Newscope.
- Use after Theo chooses fixed news sources or feeds.
- FreshRSS can help turn pages without RSS into feed-like inputs using XPath/JSON scraping.

### Career jobs normalized JSON

- Implemented import shape for the jobs tab.
- Example: `config/jobs.example.json`.
- Use as the bridge format for Saramin, WorkNet, company career pages, n8n, or changedetection workflows.
- Required visible fields: 회사명, 공고명, 하는일, 자격요건, 우대사항, 지역, 10년차 연봉, 마감일, 링크.

### Saramin Open API

- Candidate broad hiring source.
- Implemented as `jobs --fetch saramin`.
- Requires `SIGNAL_DESK_SARAMIN_KEY`.
- Good fit for career-market discovery before filtering down to mid-sized/large companies and senior roles.
- Default config: `config/job_sources.json`.
- Current limitation: list API provides enough fields for discovery, but not full 상세 업무/자격/우대 text.

### WorkNet / Work24 Open API

- Candidate official hiring source.
- Requires public API key/approval.
- Good for structured public job postings; should still be filtered against Theo's career profile.

### Official company career pages

- Candidate high-signal source for large and mid-sized companies.
- Prefer official APIs, JSON endpoints, RSS, or stable static pages.
- For dynamic pages, use changedetection/n8n to detect changes and then normalize only the resulting posting details.
