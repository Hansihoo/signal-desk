| Feature Name | Feature Description | Progress Status | Notes |
| --- | --- | --- | --- |
| Housing notice MVP | 청약/공공임대 공고를 수집, 저장, 검색, 리포트화하는 첫 MVP. | Done | 서울주거포털 LH/SH 웹 소스 수집 검증 완료: LH 10건, SH 8건. |
| Searchable local store | Codex 질문 대응을 위한 SQLite 저장소와 검색 기능. | Done | FTS5 가능 시 인덱싱하고, 표준 라이브러리 기반 semantic-lite 검색을 함께 사용. `search`와 `context` 검증 완료. |
| Mobile visual briefing | 모바일 공유용 HTML 브리핑과 이미지 추출. | Done | `site/latest.html` 생성 및 Edge headless 기반 `reports/latest.png` 추출 검증 완료. |
| Automation docs | Codex/n8n/changedetection 연동을 위한 운영 문서. | Done | 자동화는 문서화 먼저 완료. 실제 스케줄 등록은 사용자 승인 후 진행. |
| MVP completion contract | 중간에 멈추지 않도록 목표, 완료 기준, 반복 검토 루프를 문서화. | Done | `docs/MVP_GOALS.md` 추가. 완료 기준 명령과 모바일 브리핑 규칙 정의. |
| Concise mobile briefing | 청약 주택 소식을 390px 폭 모바일 이미지로 전달하는 간결 브리핑. | Done | `brief` 명령 추가. `site/brief.html`, `reports/brief.png` 생성 검증 완료. |
| Automated review loop | 개발 후 문제를 찾고 수정하기 위한 자체 검토 명령. | Done | `review` 명령 추가. 데이터, HTML, 카드 수, PNG 폭 제한 PASS. |
| Seoul/Gyeonggi scoped housing cards | 서울·경기 공고만 남기고 카드에 주소, 면적, 공급, 가격, 조건을 표시. | Done | LH 서울/경기 필터 소스 분리. 상세 HTML에서 소재지, 면적, 공급, 조건, 일정 추출. 가격은 HTML에 없으면 `원문/PDF 확인`으로 표시. |
| Codex handoff documentation | 코드를 보지 않아도 다음 Codex가 프로젝트 목표, 기능, 운영, 데이터 구조를 파악할 수 있는 문서 세트. | Done | `README.md`, `docs/HANDOFF.md`, `FEATURES.md`, `ROADMAP.md`, `OPERATIONS.md`, `DATA_MODEL.md`, `DECISIONS.md` 정리. |
