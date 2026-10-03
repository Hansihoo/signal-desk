| 업무 명 | 설명 | 진행상황 | 특이사항 |
| --- | --- | --- | --- |
| 개발 수익 기회 HTML 추가 | 첨부 명세를 새 리서치 분야의 분류·대시보드·보고서 양식으로 연결한다. | 진행 중 | 사용자가 HTML 틀·분류·요구사항 단계 선택. 8개 분류, 지표 수집 대기, 보상/검증 필드 분리, 공식 출처 후보, 단독 HTML 양식 다운로드. 실제 수집·DB·검증·필터·일일 보고서는 후속 범위. 테스트 49건·JS 구문 PASS; 배포/브라우저 검증 예정. |
| 보고서·트리 HTML 틀 | 메인→분야→하위 주제→개별 기록 탐색과 문서형 보고서 화면을 만든다. | 완료 | 공통 HTML/CSS/JS 분리, 요약·근거·검토·결론 틀과 고유 문서 링크 연결. unittest 46건, JS 구문·compileall·publish·brief·desk·review 및 이미지 확인 PASS. 클라우드 배포 37115050077 성공, 공개 245건. 데스크톱 경로·원문·차례, 430px 접이식 목차·키보드·검색/분야 필터·가로 넘침 없음, 보관본 내부 보고서 이동 확인. 클라우드 최초 165건/12:27:29 KST 유지, 로컬 보관 HTML은 자체 원본 JSON과 일치. 검토·결론은 작성 대기. |
| 다분야 리서치 메인 허브 | 주제별 독립 페이지, 분야 설정과 공개 RSS/Atom 수집을 연결한다. | 완료 | unittest 45건, publish/brief/desk/review/compileall PASS 및 이미지 확인. 분야별 중복 보존·스냅샷 불변 검증. 클라우드 2회 복원·수집·배포 성공(37113326705, 37113583835), 공개 230건. 세 분야 이동, 실제 검색, 보관 필터, 분야별 경고 분리·누적 기본 표시와 430px 가로 넘침 없음 확인. 무료 범위·호스팅 IP 기록은 GitHub 공식 문서 확인. |
| Git 기반 배포와 지속 수집 | 공개 자료 검색 화면, 날짜별 브리핑 보존, GitHub Pages 배포와 매일 수집을 연결한다. | 완료 | unittest 39건, 실제 수집과 search/context/report/render/brief/desk/review PASS 및 이미지 확인. 클라우드 2회 수집·배포 성공(run 37093169002, 37093390480), release 상태 복원·추가 백업, 165→177건 누적, 첫 일일 브리핑 보존 확인. 공개 사이트 검색·분야 필터·보관 페이지·430px 모바일 확인. |
| AI 이슈 7일치 기본 요청 세팅 | Theo가 `이슈 뽑아줘`라고 말하면 최근 7일 AI 개발자 이슈를 수집, 3페이지 브리핑, 텍스트 요약으로 알려주도록 명령과 문서를 고정한다. | 완료 | `issues`/`issue`/`이슈` CLI 별칭, `--days 7` 필터, 요약 출력, AGENTS/README/HANDOFF/OPERATIONS/FEATURES/상태 문서 갱신. |
| AI 개발자 브리핑 적용 | 유명 LLM, AI 개발 도구, 오픈소스 릴리스, 연구/안전 흐름을 3페이지 확장형 브리핑으로 수집·렌더링한다. | 완료 | `ai-news`, `ai_news.py`, `ai_brief.py`, `ai_%` 뉴스 분리, 문서/테스트 추가. 실제 18건 수집, 3페이지 PNG 생성, py_compile 및 unittest 31건 통과. |
| 청약 주택 MVP 스캐폴딩 | 로컬 수집, 검색, 리포트, HTML 브리핑 기반을 구성한다. | 완료 | 서울주거포털 LH 10건, SH 8건 수집. 검색/context/report/render/export-image 및 unittest 검증 완료. |
| MVP 목표와 검토 루프 보강 | 완료 기준, 간결 모바일 브리핑, 자동 검토 명령을 추가한다. | 완료 | `brief --width 390`, `review --width 390`, unittest 검증 완료. |
| 서울·경기 상세 카드 개선 | 카드만 보고 판단할 수 있도록 주소, 면적, 공급, 가격, 조건 정보를 표시한다. | 완료 | 서울/경기 소스 필터, 상세 HTML 추출, 390px 모바일 카드, review 지역/라벨 검증 추가. |
| Signal Desk 인수인계 문서화 | repo를 `signal-desk` 장기 프로젝트로 설명하고 다음 Codex가 이어받을 문서 체계를 만든다. | 완료 | README, AGENTS, HANDOFF, FEATURES, ROADMAP, OPERATIONS, DATA_MODEL, DECISIONS 문서 정리. |
| 탭형 모바일 데스크 준비 | 중요 요약, 청약, 주간 빅뉴스를 탭으로 분리하고 선택 탭만 이미지로 추출한다. | 완료 | `desk` 명령과 탭 렌더러 추가. unittest 8건, 탭별 HTML/PNG 생성, 이미지 육안 확인 완료. |
| 주간 빅뉴스 도구 조사 | 넓은 뉴스 수집을 직접 크롤링하기 전 사용할 오픈소스/공개 도구를 조사한다. | 완료 | GDELT, Media Cloud, Miniflux, FreshRSS, Newscope를 후보로 정리하고 `NEWS_TOOLS_RESEARCH.md` 작성. |
| 주간 빅뉴스 수집 MVP | 빅뉴스 후보를 가져와 한국어 카드로 정리하고 모바일 탭으로 렌더링한다. | 완료 | `news --source auto` 추가. GDELT 429 fallback으로 Google News RSS 수집, 출처 표시 제거, 요약 문장 강화, unittest 11건 통과. |
| 문서형 브리핑 디자인 적용 | 탭형 데스크를 모바일 문서 리포트처럼 읽히도록 타이포그래피와 카드 구조를 정리한다. | 완료 | 헤더, 탭, 지표, 뉴스/청약 블록을 문서형 디자인으로 변경. summary/housing/weekly-news 이미지 육안 확인. |
| 빅뉴스 정치 비중 조정 | 정치권 뉴스 우선순위를 낮추고 주간 빅뉴스 화면에 최대 2개까지만 표시한다. | 완료 | 비정치 뉴스를 먼저 채우고 남는 슬롯에만 정치 뉴스 최대 2개 표시. 현재 HTML은 정치 0개 표시, unittest 12건 통과. |
| 세계 빅뉴스 포함 | 한국 상위뉴스와 별도로 세계뉴스 피드를 함께 수집해 주간 빅뉴스 후보에 섞는다. | 완료 | Google News TOP+WORLD RSS 묶음 수집으로 변경. 22건 수집, 국제 뉴스 포함 이미지 확인, unittest 13건 통과. |
| 경력 이직 공고 브리핑 | 회사명, 공고명, 하는일, 자격요건, 우대사항, 지역, 10년차 연봉, 마감일, 링크 중심의 jobs 탭을 만든다. | 완료 | `job_items`, `jobs --input`, `desk --tab jobs`, 예시 JSON, 문서 추가. unittest 18건 통과. live 수집 어댑터는 후속 작업. |
| 사람인 채용 live 수집 | 사람인 Open API를 통해 경력직 후보를 수집하고 jobs 탭에 연결한다. | 완료 | `jobs --fetch saramin`, `config/job_sources.json`, 연봉 추정 매핑, 사람인 파서 테스트 추가. API 키 없을 때 실패 종료코드 확인, unittest 22건 통과. |
| 탭형 데스크 모바일 폭 개선 | 브라우저에서 너무 좁게 보이는 탭형 desk 화면을 모바일 HTML 화면답게 넓힌다. | 완료 | `desk/news/jobs` 기본 폭을 645px로 조정하고 중앙 정렬, 카드 여백, 지표 블록, 본문 타이포를 개선. |
| 프로필 기반 청약 필터 | Theo 로컬 프로필을 사용해 명확히 어려운 청약 공고를 브리핑에서 숨긴다. | 완료 | `housing_profile` 판정기, `brief`/`desk` 옵션, 테스트/문서 추가. collect, unittest 27건, review PASS, 프로필 적용 summary/housing/brief 이미지 확인 완료. |
| 청약 탭 상세 카드화 | 청약 탭을 더 긴 문서형 카드로 바꾸고 핵심 스냅샷 정보를 넣는다. | 완료 | 위치·면적·공급·가격 스냅샷, 2열 상세 필드, 확인 포인트 추가. unittest 27건, profile housing desk 이미지, summary 이미지, brief/review 검증 완료. |
