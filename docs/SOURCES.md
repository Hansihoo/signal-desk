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
