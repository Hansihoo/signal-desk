# AI 조사 검토 기록

## 2026-10-09 음성 보고서의 독자 목적·구현 역할 재검토

결과는 **변경 1편**이다. 현재 34편 중 `voice-agent-architectures`만 새 판으로 작성했다.
공식 8원문의 관련 절을 다시 읽었고, 다른 33편·모델 원문 14개는 이번 내용 검토 범위가 아니다.
‘변경 없음’으로 재검토 처리하지 않는다. [독자 질문·정확한 공식 URL·확인 절·지적과 수정](../VOICE_REPORT_REPAIR.2026-10-09.md)을 함께 읽는다.

아래는 실제 성공 확보 시각(UTC)과 원문 바이트 SHA256이다. 최초 전체 수집일과 원문 발표·갱신일은
이번 작업에서 독립 확인하지 못했으며, 이 성공 시각으로 소급 채우지 않는다. 관련 절의 내용 확인은
04:33–04:42 UTC에 수행했고, 공식 의미 검토자의 최종 재확인은 04:42:25 UTC다.
공식 기능·역할·과금 단위의 조사이며 단가표 전수 조사·실제 SDK 실행·한국어 성능/비용 실측은 아니다.

| 자료 | 성공 확보 시각 UTC | 원문 SHA256 |
| --- | --- | --- |
| voice-agents | 2026-10-09 04:33:06.391490 | e221e1192759d73cbf7a808ad5160573c6dbd2d9cb8d9370b2670b57d7446e8c |
| speech-to-text | 2026-10-09 04:33:06.516059 | 3b6b4bcc909d74f1c3f85ebbb20b1605c2c2b0dca4030ee3fa98b7ca4d105828 |
| text-to-speech | 2026-10-09 04:33:06.327997 | 997cf50802398fe2275a41cf4c8a697e3c9efc153e01c883d435ccf74b95650c |
| live | 2026-10-09 04:33:06.391490 | 3c0a25542ffaeec313e84bacff62f8d43e9c196abe697b13f04500208bd0fdee |
| live-delegation | 2026-10-09 04:33:06.724857 | 3d5fc3448f77bb81490bfd3147f35f4b63e06d684f1cef8f75a836b288ee02ca |
| realtime | 2026-10-09 04:33:06.691592 | a985aa1e7ee8a16238c0f54b7ae52421a3e1453ca63d3e714c6da7b15656c4c6 |
| gemini-live | 2026-10-09 04:33:07.324999 | 1188a2b6739f07437f73f22041a96f2b39a94d057ab10ab977c7a1c9c7adc20c |
| gemini-tokens | 2026-10-09 04:33:07.491659 | 328a89526f6b9ca429532966e7d5989610b0d3e0b7e7dcd6652499e8f3d8f3f8 |

공개 기준 JSON은 첫 4MiB 제한 응답에서 잘려 파싱에 실패했다. 이 바이트도 보존하고,
명시적 큰 제한으로 재확보한 04:33:26.950713 UTC 응답을 실제 기준본으로 사용했다.
공식 8원문은 이 실패와 무관하게 성공 확보됐고 원문 지문 8개 및 기준본 지문을 재확인했다.
파일 확보는 전문 전수 정독을 뜻하지 않는다. 실제 확인 범위는 연결된 기록의 관련 절이다.

독립 첫 화면 검토의 Revise(모호한 비교), 이어진 본문 Revise(기존 코드와 Realtime의 잘못된 대립),
공식 의미 Revise(세션 시간·별도 백엔드 과금 누락)를 실제 수정했다. 최종 불변 입력은
`33cf73c8b66c5d13bfd04780e979c39e96b57bc6e165afcd1cffaf2766a5d907`이며 각각의 범위에서
재판정 Pass다. 이는 사람 독자의 이해 승인이나 이전 34편 전부의 재승인을 뜻하지 않는다.
출력 검사와 공개 배포 결과는 작업 기록·보강 기록에서 따로 관리한다.

공개 반영은 source66b3c8b/Pages37885324722 성공이며 04:47:04.844656 UTC의 HTTP·JSON 확인에서
34현재/88판과 이전87행·다른33편·모델14원문이 정확히 보존됐다. 별도 실제390px 읽기 동선도 확인했다.
배포·화면 생성 시각은 위 원문 확보·내용 검토 시각을 새로 만드는 근거가 아니다.

작성 기준: [AI 조사 운영](../AI_RESEARCH_OPERATIONS.md). 양식 추가일: 2026-10-09.
수동 조사와 향후 반복 검토의 실제 결과를 기록하는 작업 문서다. 아래 행은 이번에 실제로
확보·읽은 자료만 나타내며 전체 영역의 조사 완료를 뜻하지 않는다. 정규화 데이터의 원본은 기존 SQLite다.

## 실행 범위와 결과

| 실제 작업 시각·시간대 | 영역·독자 질문 | 확인한 출처·기간·범위 | 결과 | 공백·다음 확인 |
| --- | --- | --- | --- | --- |
| 2026-10-09 00:26–00:49 KST | 집필·독자 학습: 낯선 기술을 제목·요약부터 이해하게 쓰려면? | 공개 스킬 3개와 Google·Diátaxis·Microsoft·IES 지침의 원문 6개 | 신규: research-teaching 스킬 생성·설치, 프로젝트 지침 연결 | 사람·독립 에이전트의 실제 독해 시험은 미실시. 전체 스킬팩을 설치한 것은 아님 |
| 2026-10-09 00:26–00:49 KST | MCP Apps: 화면·외부 조회·선택 전달이 어떻게 이어지는가? | 공식 구조·Apps 개요·지원·Quickstart·사양·발표 6개와 현재 공개 보고서 | 변경: 같은 ID의 revision 5, 제목·정의·선행 개념·공고 사례·조건 보강 | 실제 SDK/개별 계정 연결은 미실시. 다른 19편은 기존 판 유지 |

결과는 신규 / 변경 / 변경 없음 / 수집 실패 / 검토 미실행으로 구분한다.
부분 성공이면 확인한 범위와 실패·미검토 범위를 나눠 적는다. 실패 기간의 누락도 다음 확인에 남긴다.

## 날짜와 원문 검토 근거

| 정확한 원문 URL | 발표·수정일과 근거·정밀도 | 실제 최초 수집 | 최근 성공 수집 | 실제 내용 검토 시각·확인 범위 | 측정 기간·적용일 | 상태·다음 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture | 문서 경로의 사양 기준 2026-07-28; 원문 게시·최종 수정일 미확인 | 전체 최초 미확인; 이번 확보 2026-10-08T15:26:06.029404+00:00 | 이번 확보 시각과 같음 | 2026-10-09 00:49 KST: AI 앱·모델·서버 역할, 조회 왕복 | 해당 경로의 MCP 구조 | 원문 확보·내용 대조 성공. 전체 최초 시각을 이번 날짜로 대체하지 않음 |
| https://apps.extensions.modelcontextprotocol.io/api/documents/overview.html | 게시·수정일 미확인 | 전체 최초 미확인; 이번 확보 2026-10-08T15:26:06.352868+00:00 | 이번 확보 시각과 같음 | 2026-10-09 00:49 KST: Server/Host/View, 화면 파일·결과·통신 경계 | 읽은 문서 버전 | 성공; 원고의 양식/값 비유와 대조 |
| https://modelcontextprotocol.io/extensions/apps/overview | 게시·수정일 미확인 | 전체 최초 미확인; 이번 확보 2026-10-08T15:26:06.256960+00:00 | 이번 확보 시각과 같음 | 2026-10-09 00:49 KST: Client support 목록·별도 웹앱 비교 | 확인 시점의 문서 안내; 계정별 실사용은 아님 | 성공; 현재 안내와 1월 발표 목록 구분 |
| https://raw.githubusercontent.com/modelcontextprotocol/ext-apps/main/specification/2026-01-26/apps.mdx | 사양 판 2026-01-26; 파일 최종 수정일 미확인 | 전체 최초 미확인; 이번 확보 2026-10-08T15:26:06.376034+00:00 | 이번 확보 시각과 같음 | 2026-10-09 00:49 KST: tools/call, ui/message와 ui/update-model-context, 후속 대화·호스트 지연 조건 | 읽은 사양 판 | 성공; 문맥 갱신을 즉시 답변 요청으로 바꾸지 않음 |
| https://apps.extensions.modelcontextprotocol.io/api/documents/quickstart.html | 게시·수정일 미확인 | 전체 최초 미확인; 이번 확보 2026-10-08T15:26:06.415315+00:00 | 이번 확보 시각과 같음 | 2026-10-09 00:49 KST: Node.js 20+, MCP 선행 경험, 시간 표시/새 요청 | 읽은 제작 예제 | 원문 대조 성공; SDK 실행은 미실시 |
| https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/ | 발표 2026-01-26: 원문 날짜·제목 기준, 일 단위 | 전체 최초 미확인; 이번 확보 2026-10-08T15:38:09.545319+00:00 | 이번 확보 시각과 같음 | 2026-10-09 00:49 KST: 조작 가능한 업무 화면의 기본 기능·동기 | 발표 당시 내용 | 성공; 발표 당시 지원 환경으로 현재 조건을 단정하지 않음 |

작성 지침·스킬·현재 보고서의 나머지 10개 원문도 같은 조사에서 확보했다. 전체 16개 URL과
정확한 수집 시각·해시·원문 경로는 기존
`data/raw/research_teaching_2026_10_09/manifest.json`에 있다. 새로 확인한 최신 성공 시각을
기존 전체 최초 수집 시각으로 소급하지 않는다. 이번 원고의 검토일은 `checked_on=2026-10-09`다.

모르는 날짜는 미확인으로 적는다. 피드 관찰·원문 확보·내용 검토를 구분하며 렌더링 날짜로 갱신하지 않는다.
실패는 최근 성공일을 덮어쓰지 않는다. 기존 자료의 최초 수집일을 현재로 소급하지 않는다.
원문을 보존한 경우 실제 기존 snapshot 경로를 연결하되 비공개 자료·자격 증명은 남기지 않는다.
원문·시각 근거가 많아지면 호환성이 검증된 공통 데이터 계약으로 이관한다.

## 발견한 후보와 선정 판단

| 후보·독자 질문 | 근거 URL·확인 날짜 | 조사 영역·관련 보고서 | 게시·보류 이유 | 반대 근거·미확인 조건 | 다음 작업 |
| --- | --- | --- | --- | --- | --- |
| 문서만으로 질문에 답하는 독자 관점 검토 | [Anthropic doc-coauthoring](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md), 2026-10-09 | 집필·MCP Apps | 해당 원칙을 자체 스킬에 참고. 사용자 인터뷰·매 단계 확인 흐름은 그대로 적용하지 않음 | 독립 독자 검토는 이번 작업에서 수행하지 않음 | 후속 집필부터 두 가지 읽기와 실제 수정 기록 |
| 근거·공백의 종합과 인용 | [OpenAI Notion research documentation](https://github.com/openai/skills/blob/main/skills/.curated/notion-research-documentation/SKILL.md), 2026-10-09 | 집필·근거 관리 | 현재 Git/SQLite에 맞는 근거 관리만 참고 | Notion 작업 도구와 플랫폼을 도입하지 않음 | 기존 데이터 계약과 날짜 기록 유지 |
| 구현 계획용 writing-plans | [Superpowers writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md), 2026-10-09 | 집필 후보 | 보류: 실제 목적은 소프트웨어 구현 계획으로 교재 집필과 다름 | 스킬 이름만 보고 글쓰기용으로 간주하지 않음 | 이번 설치 대상에서 제외 |

고정 출처 밖에서 발견한 주제와 아직 빠진 질문도 기록한다. 재인용·중복·확인일만 갱신된 글은 새 내용과 구분한다.

## 원고와 검증 기록

원고별 독자 질문·선행 지식·이해하거나 끝낼 결과를 적고 게시했다면 보고서 ID·불변 판을 연결한다.
근거·의미 검토, 이해 가능성 자체검토, 예제 실제 실행, 기술 출력 검증, 실제 독자 시험을 별도 기록한다.
수행하지 않은 검사는 미실시로 남긴다. 구조 검증 통과나 장 수 증가를 독자 이해의 근거로 적지 않는다.

2026-10-09 MCP Apps revision 5: 편집 목적과 제목/요약만 읽기·본문/변형 문제의 집필자 자체검토는
[스킬 조사·적용 기록](../RESEARCH_TEACHING_SKILL.2026-10-09.md)에 있다. 공식 원문 의미 대조,
106 테스트·내부 참조·실제 모바일/데스크톱 출력 검증은 별도 수행했다. 독립 에이전트 검토,
실제 사람의 독해 시험, SDK 실행, 계정별 연결 시험은 미실시다. 다른 19편의 독해 승인은 남아 있다.

공개 기술 확인: source422d896 / Pages37805827869 성공. 2026-10-09 01:06:59 KST의
HTTP/JSON 비교에서 MCP 입력 일치·다른19편/이전52판 보존·전체20편/53판을 확인했다.
참고/학습 주소와 CSS·빈 데이터 비표시도 확인했다. 공개 조작 검사를 직접 수행한 것은 아니다.

## AI 집필의 정보 가치와 번역 영향 조사 2026-10-09

독자 질문: AI가 자연스러운 요약을 넘어 개발자·관리자에게 배울 내용이 있는 글을 쓰게 하려면 어떻게 해야 하는가?

결과는 신규 수동 분석이다. 6개 원문을 확보하여 방법·평가·해당 한계를 선택해 읽고 기존 34개 글 검토와 대조했다. 영어 초안과 한국어 번역의 직접 비교, 실제 독자 시험, 논문 재현, 보고서 재작성은 수행하지 않았다. 수집기 연결·정규화 DB 입력·반복 자동화 완료를 뜻하지 않는다.

| 정확한 원문 URL | 발표·수정일과 근거·정밀도 | 실제 최초 수집 | 최근 성공 수집 | 실제 내용 검토 시각·확인 범위 | 측정 기간·적용일 | 상태·다음 확인 |
| --- | --- | --- | --- | --- | --- | --- |
| https://aclanthology.org/2024.naacl-long.347.pdf | 2024-06: NAACL 표지·월 단위 | 전체 최초 미확인; 이번 snapshot 시작 2026-10-09T01:16:06.634502+00:00 | 2026-10-09T01:16:10.190395+00:00 | 2026-10-09 10:23:14 KST: 사전 질문·자료 수집, 비교 방법, 20쌍/편집자 10명의 평가와 비관련 사실 연결 한계 | 해당 논문 실험; 현재 모델 평가 아님 | 원문 확보·선택 내용 검토 성공; 모든 부록/원 코드/벤치마크 재현 미실시 |
| https://aclanthology.org/2023.emnlp-main.398.pdf | 2023-12: EMNLP 표지·월 단위 | 전체 최초 미확인; 이번 snapshot 시작 2026-10-09T01:16:06.636503+00:00 | 2026-10-09T01:16:08.827104+00:00 | 2026-10-09 10:23:14 KST: 유창성/정확성/인용 평가 구분, 주장-근거 지원 범위와 자동 평가 한계 | 해당 논문 과제; 현재 성능으로 일반화하지 않음 | 원문 확보·선택 내용 검토 성공; 모든 부록/원 코드/벤치마크 재현 미실시 |
| https://arxiv.org/html/2503.05244v1 | 2025-03-07: arXiv v1 제출·일 단위 | 전체 최초 미확인; 이번 snapshot 시작 2026-10-09T01:16:06.637503+00:00 | 2026-10-09T01:16:07.210038+00:00 | 2026-10-09 10:23:14 KST: 요청별 기준, 300개 사람 비교, 영어·중국어 범위, 일치율과 학습 효과 구분 | 이번에 읽은 v1; 최신 모델 순위 검토 아님 | 원문 확보·선택 내용 검토 성공; 모든 부록/원 코드/벤치마크 재현 미실시 |
| https://arxiv.org/html/2506.11763v1 | 2025-06-13: arXiv v1 제출·일 단위 | 전체 최초 미확인; 이번 snapshot 시작 2026-10-09T01:16:06.638503+00:00 | 2026-10-09T01:16:07.043583+00:00 | 2026-10-09 10:23:14 KST: 100과제/22분야, RACE/FACT, 자동 생성 기준 보고서·평가 모델과 범위 한계 | 기준 보고서 2025-04; 평가 방법 검토 | 원문 확보·선택 내용 검토 성공; 모든 부록/원 코드/벤치마크 재현 미실시 |
| https://arxiv.org/html/2606.01252v1 | 2026-05-31: arXiv v1 표기·일 단위 | 전체 최초 미확인; 이번 snapshot 시작 2026-10-09T01:16:06.843338+00:00 | 2026-10-09T01:16:07.280674+00:00 | 2026-10-09 10:23:14 KST: 뉴스 200개/24언어, 모델·평가 조건, 한국어 포함 방식 비교와 한계 | 이번 논문 실험; 프로젝트 번역 원인 실험 아님 | 원문 확보·선택 내용 검토 성공; 모든 부록/원 코드/벤치마크 재현 미실시 |
| https://ies.ed.gov/ncee/wwc/Docs/PracticeGuide/20072004.pdf | 2007-09: 지침 표지·월 단위 | 전체 최초 미확인; 이번 snapshot 시작 2026-10-09T01:16:06.903051+00:00 | 2026-10-09T01:16:14.533818+00:00 | 2026-10-09 10:23:14 KST: 권고 2 풀이 사례/연습 Moderate, 권고 7 깊은 설명 Strong, 기초 지식 조건 | 여러 학습 실험 종합; AI 한국어 교재 실험 아님 | 원문 확보·선택 내용 검토 성공; 모든 부록/원 코드/벤치마크 재현 미실시 |

전체 최초 수집은 미확인으로 유지한다. 이번 snapshot의 exact URL·수집 시각·원문 SHA와 선택 확인 범위는 data/raw/research_teaching_2026_10_09/ai-writing-research.2026-10-09.sources.json에 보존했다. 원문 텍스트 추출은 읽을 준비이며 전체 내용 검토와 같은 상태로 간주하지 않는다.

선정: 질문을 통한 사전 조사, 주장-근거 대조, 과제에 따른 내용 평가, 풀이 사례와 깊은 설명, 언어 간 요약 손실을 프로젝트용 분석에 참고했다. 모두를 합친 프롬프트의 효과는 아직 검증하지 않았다. [연구 분석과 적용 제안](../AI_WRITING_RESEARCH.2026-10-09.md).

보류·부분 확인:

- https://pmc.ncbi.nlm.nih.gov/articles/PMC11244532/ : 창작 다양성 논문의 본문 열람은 캡차로 실패. 검색으로 발견했으나 이번 6개 원문 근거에는 포함하지 않았다. 실패를 변경 없음으로 기록하지 않는다.
- https://www.science.org/doi/10.1126/science.adh2586 : 직무 글쓰기 실험은 검색의 초록·서지 범위에서 발견. 본문 검토는 미실행이며 이번 내용 평가의 근거로 사용하지 않았다.
- https://www2.statmt.org/wmt26/papers.html : Lost in Mimicry 논문 목록은 확인했으나 원문 PDF 검토 미실행. 번역투에 관한 성능·교정 효과는 이번 결론에 포함하지 않았다.

핵심 공백: 현재 원고의 생성 과정과 영문 초안이 없어 번역의 직접 원인을 확정할 수 없다. 문서 검색 AI의 실제 검색 후보/원문/선택/답변을 확보한 한 편으로 개선 전후를 비교하고 독자의 적용·설명 결과를 확인하는 것이 다음 검증이다. 기존 보고서·스킬·날짜 스키마는 이번 분석에서 수정하지 않았다.

## 전수 원고 보강의 원문 의미 대조 2026-10-09

독자 질문: AI 업무를 직접 구성하거나 도입을 검토하는 개발자·관리자가 이 글에서 무엇을
이해하고 자신의 조건에 적용할 수 있는가? 요약 전에 필요한 원리·조건·수치를 다시 확인했다.
전체20편은 새 판, 수입 모델14편은 원문을 유지한 별도 해설로 보강했다.
[각 원고의 목적·실제 수정·독립 판정](../RESEARCH_AUTHORING_REPAIR.2026-10-09.md).

날짜 기록의 한계: 아래 공식13편 핵심 대조는2026-10-09 02:47–02:57 UTC(11:47–11:57 KST)
검토 구간에서 수행했다. URL별 정확 획득/읽기 완료 시각과 로컬 원문 파일은 미보존이다.
구간을 각 URL의 acquired_at로 소급하지 않는다. 전체 최초 수집일도 미확인으로 유지한다.
웹·브라우저 도구 출력은 실제 읽기 근거지만 로컬 원문 snapshot과 별개다. 추가 FDE/Upwork 대조
뒤 clock 기록03:14:40 UTC, OSS-Fuzz 정의 추가 대조 뒤03:26:52 UTC,
최종20편 JSON 의미 대조 뒤03:31:59 UTC. 개별 URL의 정확 획득 시각으로 바꾸지 않는다.

| 정확한 URL·원문 묶음 | 원문 발표·수정일·측정 기간 | 실제 확인 범위·수집/검토 상태 | 미확인·실패·다음 확인 |
| --- | --- | --- | --- |
| https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits ; https://docs.github.com/en/billing/concepts/product-billing/github-actions | 원문 최종 수정일 미확인; 이번 확인 시점의 정책 본문 | 저장소 권장/게시사이트1GB·월100GB soft·빌드 조건 및 Actions 공개 저장소 조건 | 계정별 청구/트래픽 실측 없음 |
| https://aws.amazon.com/startups/credits/ ; https://aws.amazon.com/awscredits/ | Credit Terms 표기2026-09-24; 크레딧은 실제 승인·유효기간 적용 | Founders/Portfolio·Org ID·누적 승인·유효 대상/잔액/만료와 현금 계산 조건 | 실제 신청/승인/결제 없음 |
| https://aws-cds-partner.devpost.com/rules | 마감2026-10-28 13:00PDT →10-29 05:00KST | APN 등록 조직·제출 서비스·영상3분의 규칙, 수락/전달 구분 | 실제 참가·메일 전송 없음 |
| https://nlnet.nl/news/2026/20260903-call.html ; https://nlnet.nl/restack/guideforapplicants/ ; https://nlnet.nl/restack/eligibility/ ; https://nlnet.nl/foundation/policies/generativeAI/ | 공고2026-09-03, 마감11-03 12CET; GenAI정책v1.1 2026-01-26 | 공개 인터넷 기반 기술·€50k 첫지원·지역/예외·제안서와 AI프로젝트 정책 구분 | 개별 지원자 자격·예외 승인 미확인; 정책 개정 예정은 완료로 쓰지 않음 |
| https://bughunters.google.com/blog/ossvrp-rule-updates-2026 ; https://bughunters.google.com/about/rules/about-this-section | 개정글2026-03-19; 관련 프로그램4-09/7-06 적용 | OT2/OT3·Product/Other범위·비공개 목록. 웹/정적 추출·browser-client 실패 뒤 CUA 원문 성공, 직후 clock02:50:56UTC | 전체OSS중단으로 일반화 금지; 비공개OT2 전수목록 미확인 |
| https://openai.com/index/safety-bug-bounty/ ; https://bugcrowd.com/engagements/openai-safety | Bugcrowd 수정 표기2026-08-07T18:31:30Z | 발표 성공, Bugcrowd 웹 추출 실패 뒤 CUA 성공. OpenAI-side fixability·자기계정·50% 특정 제삼자 경로 | 실제 공격·제출 없음; 제삼자MCP 자체 문제를 OpenAI적격으로 단정하지 않음 |
| https://docs.github.com/en/apps/github-marketplace/creating-apps-for-github-marketplace/requirements-for-listing-an-app ; https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/differences-between-github-apps-and-oauth-apps ; https://docs.github.com/en/apps/github-marketplace/using-the-github-marketplace-api-in-your-app/handling-new-purchases-and-free-trials | 게시·수정일 미확인; 이번 문서 조건 | 설치 계정/저장소·100/200목록조건·구매와 기능권한 분리 | 실제 등록·구매·webhook 없음 |
| https://www.upwork.com/research/in-demand-skills-2026 ; https://investors.upwork.com/news-releases/news-release-details/upworks-demand-skills-2026-demand-top-ai-skills-more-doubles-ai ; https://openai.com/careers/forward-deployed-software-engineer-sf-san-francisco/ | 연구 발표2026-02-04, 측정2025 미국계약 수입 vs2024; FDE 게시일 미확인 | 수입지표/완료·계약 표현차이·고객 현장 배치 역할. 추가 원문 대조 뒤clock03:14:40UTC | 개인임금·한국시장·현재 전체고용 수치 아님; 입사/납품 실행 없음 |
| https://blog.tally.so/in-2026-were-optimizing-for-quality-not-revenue/ ; https://tally.so/pricing ; https://tally.so/changelog ; https://docs.stripe.com/billing/subscriptions/analytics | 2026년1월 자기보고MRR$358k·팀10; 변경기록7-08/8-04/9-11 | 매출·현금/월환산 정의·기능 발표 시간 순서. changelog웹 timeout후CUA성공/clock02:56:44UTC; Stripe관련절clock02:56:01UTC | 실제수익성·전환/이탈 데이터·가격 선택상태미확인, 변경기능이1월매출의 원인 아님 |
| https://www.mss.go.kr/site/smba/ex/bbs/View.do?bcIdx=1070813&cbIdx=310&parentSeq=1070813 ; https://www.mss.go.kr/common/board/Download.do?bcIdx=1070813&cbIdx=310&streFileNm=9712229c-8781-401b-a1dc-e22d443569bc.pdf ; https://www.bizinfo.go.kr/sii/siia/selectSIIA200Detail.do?pblancId=PBLN_000000000125978 | 마감2026-10-30 18KST·사업24개월 | 웹MIME실패후PDF8쪽 메모리 다운로드/읽기. 재확보02:52:49.418035UTC·534118bytes·SHA cedbce55531ccd72ccd39384bcdd9a96b56e93bb4e37a3e273ee49cce73c67c6. 선행과제완료/60점·기관역할·성과·39억원상한/정부≤75%·기관≥25%중현금≥10% | 로컬PDF미보존,ZIP양식1~3미열람·실제회사자격미확인 |
| https://www.nipa.kr/home/bsnsAll/0/nttList?bbsNo=4&bsnsDtlsIemNo=580&tab=2 |3-30 종료공고 | 지원·공급 역할과 지난 공고 구분 | 열린사업으로 쓰지 않음 |
| https://www.polarisoffice.com/ko/solution/datainsight ; https://www.polarisoffice.com/business-blog/introduction-office-solutions | 게시·수정일 미확인 | 공개 문서객체구조화·RAG기능 소개와 가상 업무의 오류/수정시간 계산 | 제품성능·고객효과 실측 없음,사내기밀 사용 없음 |
| https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/overview ; https://www.hancom.com/news/article/detail/13778?type=news ; https://news.adobe.com/news/2025/08/acrobat-studio-delivers-new-ai-powered-home-for-productivity-creativity | MS수정2026-09-30; 한컴7-02 beta/하반기계획; Adobe2025-08-19 발표 | 제품 연결 범위·발표/계획/제공상태, 계약추출→정책→초안/승인 사례 | 실제 계정별 이용/현재가격/고객효과 미확인 |
| https://artificialanalysis.ai/methodology/coding-agents-benchmarking/ ; https://artificialanalysis.ai/methodology/intelligence-benchmarking ; https://github.com/theo-s-han/research-analysis#통합-모델-비교-갱신 | CodingIndexv1.5·303과제113/66/124·3시도; 원문 전체최종수정일 미확인 | 동일가중3평가·시도당비용/시간·AA-LCR/Automation·기존모델출처 운영. 약02:52–02:54 관련절,개별정확시각미보존 | 원자료표 웹접근 실패;14공급자의 모든 원전 사양·가격 전수검토 아님 |

집필자가 추가 확인한 기술 원문은 아래와 같다. 실제2026-10-09 관련절을 읽었으나 정확URL별 획득
시각/로컬snapshot은 미보존이다. 기존 최초/최근 수집을 오늘로 덮어쓰지 않았다.

| 원문 URL | 확인 지식·범위 | 적용·한계 |
| --- | --- | --- |
| https://developers.openai.com/api/docs/guides/tools-file-search | include=file_search_call.results와 기본 인용/후보 반환 차이 | 실제유료검색요청 없이 원리 설명 |
| https://ai.google.dev/gemini-api/docs/function-calling | Interactions steps function_call·name/arguments/id·앱실행·function_result/previous_interaction_id | 기존generate_content와섞지않음;API실행미실시 |
| https://developers.openai.com/api/docs/guides/voice-agents | 단계형STT/업무/TTS·Realtime/GPTLive역할 | 한국어품질/지연 측정없음 |
| https://developers.openai.com/api/docs/deprecations ; https://developers.openai.com/api/docs/guides/migrate-to-responses | 모델수명과endpoint이전·messages/items·응답파싱 | 모든새모델성능/가격검증아님 |
| https://www.palantir.com/docs/foundry/ontology/overview | 객체·속성·관계·행동/함수의 뜻 | ontology제품구축/권한실습미실시 |
| https://google.github.io/oss-fuzz/ ; https://google.github.io/oss-fuzz/reference/glossary/ | fuzz-target·재현입력·프로젝트편입 | 공격/퍼저실행없음 |
| https://arxiv.org/abs/2401.04088 ; https://huggingface.co/docs/transformers/kv_cache | Mixtral2024-01-08 초록의token별전문가·47B전체/13B활성예;key/value재사용·메모리·offload관련절 | 모델 검토자도 정의대조;전체MoE모델사양/PC실행미검증 |

수입 원자료14편은 기존 공개snapshot `all-education-review.public.json`에서 HTML·공유자산·날짜를
읽어 각 해설과 전체지문을 결합했다. 이snapshot은 위 공식13편 원문파일을 보존한 자료가 아니다.
`checked_on=2026-10-09`는 이 해설의 내용검토일이며 원자료의 공란 기준일이나 공급자 최신가격
확인일을 소급해 채운 것이 아니다. 새지원조건/기술명만늘리는 대신 질문→원리/조건→같은값의사례→
다른조건의풀이를 보강했다. 임금·국내고용전체/제품실측/비공개프로그램 목록은 근거가 부족해 보류했다.

최종20편 배치17c0d1b6…: 별도교육20편 Pass,공식핵심13편 Pass.
별도모델14편 배치9a0ae0b0…: 첫5Pass/9Revise 후수정·재검토14Pass.
구현지문·원문보존·낡은해설차단·역사연결도 별도Pass. 실제사람학습·SDK·API·보상신청·공격·
제품구매시험은 미실시. 기술출력검사는 내용판정과 구분하여 작업기록에 남긴다.

공개 반영 source38f473b/Pages37881082742 성공.2026-10-09 03:53:08.699451 UTC의
공개 자료 확인에서34최종입력/87판·이전53행/원자료14행의 전체 보존,54주소200·표시페이지수·
제목/설명/참고앵커를 검증했다. 실제390px 공개 검색→RAG·Enter펼치기·해설→원자료도 별도 통과했다.
배포/화면 재생성을 공식 원문의 새로운 내용 수집·검토 시각으로 간주하지 않는다.
