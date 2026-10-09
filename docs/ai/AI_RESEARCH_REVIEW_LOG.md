# AI 조사 검토 기록

## 2026-10-09 질문 기반 생산 시범: 실제 발주와 RAG

내용 변경은2편이다. `upwork-ai-integration-demand`는 기업이 어떤 AI 개발을
외주로 맡기는지와 공개 예산의 의미를, `document-rag-grounding`은 문서를
찾는 단계와 답을 해석하는 단계의 오류 구분을 다룬다. 다른32편은 이번 원문
내용 검토 범위가 아니며 ‘변경 없음’으로 처리하지 않는다.

아래 UTC는 웹 도구에서 해당 원문 관련 절을 실제 확보한 영수증의 시각이다.
새 원문 묶음 안의 첫 확보이며 과거 전체 시스템의 최초 수집일을 소급한 값이
아니다. 과거 최초 수집일과 원문 발표/갱신일은 이번에 확정하지 못했다.
정확한 URL·선택 발췌·영수증 지문·확인 절은
[불변 품질 패키지](../../config/research_quality_pilot.2026-10-09.quality.json)에 보관한다.
전체 도구 영수증은 등록된 `data/raw/research_teaching_2026_10_09/`에 보존한다.
원문 전문 전수 정독이나 전체 데이터셋 다운로드를 뜻하지 않는다.

| 원문 | 성공 확보 UTC | 실제 내용 확인 범위와 미확인 조건 |
| --- | --- | --- |
| [Upwork In-Demand Skills 2026](https://www.upwork.com/research/in-demand-skills-2026) | 06:39:32.977 | 성장 수치와 방법론.2025/2024·미국 수요·체결 계약의 수입 합계·6범주·항목별최소10만달러 조건. 공고 수/개인 단가/한국 시장으로 해석하지 않음. |
| [상담 AI/RAG 실제 의뢰](https://www.upwork.com/freelance-jobs/apply/Engineer-Needed-Build-Production-Ready-Assistant-RAG-Chatbot_~022098462316766083390/) | 06:39:34.887 | Summary·가능 기능·요구 경력·제안 요청·US$1,500 고정 제시 예산. 상대 게시일 환산, 현재 모집 여부, 체결/완료액 미확인. |
| [Thruhike](https://www.upwork.com/success-stories/thruhike) | 06:39:36.895 | 공개 고객의 문제·해결·이메일/데이터/내부 업무. 플랫폼 홍보성 자기 보고; 프로젝트 금액·구현 원문·독립 효과 미확인. |
| [후기 분석 수행 사례](https://www.upwork.com/success-stories/machine-learning-expert-automate-complex-tasks) | 06:39:38.717 | 수행 업체Shapeion·익명 최종 고객·고객 후기 분석. 공급자를 발주 고객으로 바꾸지 않음. 프로젝트 금액·정확도 미확인. |
| [Azure AI Search RAG](https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview) | 06:39:41.346 | 정의·classic RAG·준비·권한 제한. 실제 계정 실행/성능 검증 미실시. |
| [Anthropic Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) | 06:39:43.188 | 전통 RAG·문맥 손실·문맥 보강·재정렬 방법. 공급사 벤치마크 수치 재사용/직접 재현 안 함. |

새 HTTP 수집 경로는07:01:06–07 UTC에 같은 Upwork 의뢰403 실패,
Azure·Anthropic 성공을 별도로 기록했다. 실패에 옛 원문을 새로 읽은 것처럼
제공하지 않았다. 일부 다른 의뢰는 목록 페이지로 이동해 제외했다. 검색 결과
요약을 예산·개발 조건의 증거로 사용하지 않았다.

독립 첫 화면 검토자는 제목/소개/deck만 읽었다. RAG의 구현 약속 제목과
모호한 비교 대상을 수정 후 재확인했다. 별도 Upwork 원문/본문 검토는 가능한
개발 범위를 확정 범위·보편적 필수 기능으로 바꾼 부분을 찾아 수정했으며,
최종 재확인06:51:18 UTC에 해당 범위Pass를 기록했다. RAG 원문/본문 검토도
필터 적용 전후 후보를 섞은 설명을 수정 후 재확인했다. 각 최종 파일 지문과
판정 사유·위치는 품질 패키지와 등록된 검토 영수증에 연결했다. 단순 유효 JSON,
형식 검사, 기존 판정으로 내용 검토를 대신하지 않았다.

자료 수집, 원문 의미/본문 검토, 첫 화면 이해 검토,128개 코드 시험과 화면 검사를
서로 구분한다. 실제 사람의 이해/학습 측정·유료 모델API·RAGAPI 실행·계약 결과와
시장 대표성 확인은 미실시다. 자동 생산 코드는 구현했지만 이번 두 원고를 유료
생성 API의 실계정 자동 결과라고 주장하지 않는다.

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
## 2026-10-09 전체 원고 다듬기

현재 작성 보고서·해설34편의 제목·소개·본문을 다듬었다. 새 분야 수집이나 원문14문서의
재작성은 아니다. 전체 첫 화면 전용 독립 검토와 기술8/사업12/모델14 본문 검토의 범위와
실제 수정은 [전체 기록](../RESEARCH_REFINEMENT.2026-10-09.md)에 남긴다.

수집 기준본은 source66b3c8b 공개 snapshot이며 기존 원문의 날짜·미확인 범위를 유지한다.
원고 변경으로 전체 수집·확인일을 오늘로 바꾸지 않았다. OpenAI Docs MCP의 새 확보3건은
종료 공지의 deprecated/legacy·tts-1 권장 대체, Realtime 세션, 해당 대체 모델의 지원 접점을
읽은 범위다. [종료 공지](https://developers.openai.com/api/docs/deprecations),
[Realtime](https://developers.openai.com/api/docs/guides/realtime),
[대체 모델 접점](https://developers.openai.com/api/docs/models/gpt-realtime-2.1-mini).
정확한 확보 시각·로컬 경로는 raw의 all-refinement-openai-acquisition.json에 있다.

모델 비용 단위는 보존된 원문 HTML의 과제당 비용 툴팁을 읽은 결과다. 현재 가격·계정 한도·
제품 성능 전수 확인이 아니며, 본문 검토 Pass도 실제 사람의 학습·SDK 실행을 뜻하지 않는다.
글을 재생성한 시각은 원자료의 새 측정/확인일이 아니다.

변경 후 독립 재독은 기술8·사업12·모델14 모두 필수 수정0건이다. 별도 첫 화면 전용 검토의 실제15 Revise를 수정해34 Pass가 됐으며 본문과 별도 기록한다. 이전88판·모델14원문 보존/입력34정확일치·총122판을 로컬 확인했다. 실제 재조회는 위 OpenAI3문서의 특정 절이며 다른 출처 전수 최신 검토로 확대하지 않는다.

공개 source99a5fa2/Pages37888632157 성공.05:29:34.122259 UTC의 자료 확인에서34최종입력/122판·이전88행/모델14원문행 전체 일치·39주소200/CSS 일치를 확인했고 실제390px85출력검사도 통과했다. 이것은 원문의 새 내용 수집/사실 검토나 사람의 이해 승인을 대신하지 않는다. 실패/성공/편집 지적/최종 원고 지문은 기존 보존 root에 남겼다.

## 2026-10-09 AI 활용·글쓰기·게임 제작 수동 조사

요청: 세 분야별 전문가의 사용 방법, 관련 Agent Skills, 공개 소프트웨어와 초보자의 활용 경로를 넓게 조사해 채팅으로 설명한다. 사용자는 게임 구현·스킬 설치·HTML 제작·공개 발행을 요청하지 않았다.

방법: 공식 문서와 개발 주체의 저장소로 기능·요건을 확인하고, 연구기관의 실험·작가의 직접 인터뷰·게임사의 연구 사례로 작업 방식을 비교했다. 전문 글쓰기 실험을 소설가 전체의 생산성으로, 특정 시기 코딩 실험을 현재 모든 도구의 성능으로 일반화하지 않는다. 기술 명세/README 확인은 설치·실행 평가가 아니다.

편집 질문과 답변 경로:

| 분야 | 독자 질문·선행 지식 | 확보한 답과 설명 사례 | 남은 범위 |
| --- | --- | --- | --- |
| AI 활용 | 챗봇을 써본 초보자가 무엇을 어떤 순서로 맡기는가? | 입력 자료·산출물·완료 기준을 먼저 고정; 가상 회의 메모를 담당/기한/미정 항목으로 바꾸고 반복 업무만 자동화 | 실제 개인 업무의 시간/오류 비교, 로컬 모델의 PC별 성능 미측정 |
| 글쓰기 | AI로 정보 가치와 자기 표현을 살리려면? | 독자 질문→근거→초안→구조/문장 편집; 가상 게임 입문 안내의 일반 문장을 조건·동작·관찰로 고침. 소설은 인물·갈등·선택의 장면 지시와 인간 편집을 구분 | 한국어 독자 시험·문학 품질의 독립 평가·도구별 성능 비교 미실시 |
| 게임 제작 | 비개발자와 개발자는 어떤 도구/스킬로 첫 작품을 끝내는가? | 엔진끼리 선택 기준을 비교하고 MCP 연결 도구와 스킬은 별도 설명. 30초 별 수집 게임의 이동→수집→타이머→종료→재시작 및 예상 상태 | 게임/엔진/스킬 실행, 에셋 생성·배포·플레이테스트 미실시 |

날짜: 이번 수동 확보·관련 내용 검토일은 2026-10-09 Asia/Seoul. 도구가 원문별 정확한 확보 시각을 반환하지 않아 시각을 소급 생성하지 않는다. 작업 중 확인한 실제 시계는 2026-10-09 10:17:40 UTC이며 개별 원문 발표/측정 시각이 아니다. 프로젝트의 과거 최초 수집일은 미확인으로 보존한다. 아래 원문 날짜의 `미확인`은 오늘로 채우지 않는다. 웹 도구의 읽은 절을 근거로 하며 별도 로컬 전체 원문 스냅샷은 보관하지 않았다. 기존 수집기/SQLite/report-v1/공개 판에는 반영하지 않는다.

### AI 활용: 확보한 원문과 확인 범위

| 원문 URL | 원문 날짜/측정 조건 | 실제 읽은 범위·해석 제한 |
| --- | --- | --- |
| https://www.anthropic.com/engineering/building-effective-agents | 2024-12-19; 현재 글에는 옛 도구 설명의 변경 주의가 있음 | workflow/agent 구분, 단순한 구성부터 시작, 도구 피드백. 최신 제품 우열의 근거로 쓰지 않음 |
| https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic | 발표 2025-12-02; 조사 2025-08, 직원132명/심층53명 | 디버깅·코드 이해·작은 위임, 자기보고 생산성/감독·학습 우려; 독립 인과 실험과 구분 |
| https://metr.org/blog/2026-02-24-uplift-update/ | 2026-02-24; 초기 실험2025-02~06와 후속2025-08부터 구분 | 초기19% 시간 증가와 후속 선택 편향/신뢰구간. 현재19% 느리다는 주장이나 후속 확정 가속 수치로 재사용하지 않음 |
| https://learn.chatgpt.com/docs/build-skills | 원문 발표/수정일 미확인 | OpenAI Docs MCP 본문: SKILL.md/참고자료/스크립트·선택 로딩·설치와 배포 구분 |
| https://agentskills.io/specification | 원문 발표/수정일 미확인 | 필수 name/description, SKILL.md와 선택 디렉터리, 호스트별 호환성 |
| https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro | 버전 경로2026-07-28; 별도 발표일 미확인 | 외부 도구/데이터 연결 개념. 스킬 지침만으로 도구가 연결되는 것은 아님 |
| https://developers.openai.com/api/docs/guides/evaluation-best-practices | 원문 발표/수정일 미확인 | OpenAI Docs MCP: 과업별 성공 기준/데이터/사람 피드백. Evals 플랫폼 종료 안내가 있어 신규 플랫폼 도입을 추천하지 않음 |
| https://github.com/ollama/ollama | README/라이선스의 원문 날짜 미확인 | 로컬 실행/모델 공급자, MIT 프로그램과 모델별 조건 구분. 클라우드 경로도 있어 로컬 설정 확인 필요 |
| https://github.com/Mintplex-Labs/anything-llm | README/라이선스의 원문 날짜 미확인 | 문서 대화, 데스크톱, Ollama/원격 공급자/임베더 목록, MIT. 모든 설정이 로컬이라는 보장 아님 |
| https://github.com/langchain-ai/langgraph | 원문 날짜 미확인 | 상태를 가진 장기 실행 에이전트 프레임워크, MIT. 초보자의 첫 사용에 필수 아님 |
| https://github.com/promptfoo/promptfoo | 원문 날짜 미확인 | CLI 기반 프롬프트/에이전트/RAG 평가, MIT, 공급자 API 키 요건. 유료 모델 호출 비용 별도 |
| https://github.com/langgenius/dify | 원문 날짜 미확인 | 시각적 AI 워크플로/RAG. 기능 소개와 효과 측정 분리 |
| https://raw.githubusercontent.com/langgenius/dify/main/LICENSE | 표기 ©2025; 개정일 미확인 | Apache2.0 수정 라이선스: 다중 tenant 서비스와 frontend 표시 조건. 일반 Apache2.0으로 표기하지 않음 |
| https://github.com/n8n-io/n8n | 원문 날짜 미확인 | 시각적 자동화, fair-code 표기. 일반 OSI 오픈소스와 구분 |
| https://raw.githubusercontent.com/n8n-io/n8n/master/LICENSE.md | Sustainable Use License1.0; 발표/수정일 미확인 | 내부 업무/비상업적 이용 범위와 Enterprise 예외. 자유로운 재판매 가능으로 요약하지 않음 |
| https://raw.githubusercontent.com/anthropics/skills/main/README.md | 원문 날짜 미확인 | 예제 다수 Apache2.0; docx/pdf/pptx/xlsx는 source-available 별도 조건, 저장소 전부 오픈소스라는 주장 배제 |
| https://raw.githubusercontent.com/anthropics/skills/main/skills/mcp-builder/SKILL.md | 원문 날짜 미확인 | MCP 서버 제작 절차. 기존 연결 도구를 사용하는 스킬과 직접 서버를 만드는 스킬 구분 |
| https://raw.githubusercontent.com/anthropics/skills/main/skills/webapp-testing/SKILL.md | 원문 날짜 미확인 | Playwright 기반 상호작용/스크린샷/로그 확인. 게임의 재미를 자동 입증하지 않음 |

### 글쓰기: 확보한 원문과 확인 범위

| 원문 URL | 원문 날짜/측정 조건 | 실제 읽은 범위·해석 제한 |
| --- | --- | --- |
| https://news.mit.edu/2023/study-finds-chatgpt-boosts-worker-productivity-writing-0714 | 2023-07-14; 전문직453명, ChatGPT3.5, 짧은 직업별 과제 | 시간40% 감소/평가품질18% 증가. 사실검증·기업 고유 문맥 미포함이라는 연구진 제한을 함께 보존 |
| https://discovery.ucl.ac.uk/id/eprint/10195027/ | Science Advances2024,10(28),eadn5290 | 초록의 짧은 이야기 아이디어 실험: 개별 창의성/평가 향상과 이야기 간 유사성 증가. 한국어·전문 소설가·현재 모델 효과의 직접 증거 아님 |
| https://aiinstitute.hbs.edu/back-to-the-beginnings-of-ai-at-work/ | 2026-04-09 회고; June2023 GPT4 실험, 758 BCG컨설턴트 | peer-reviewed 판 소개의 과업별 효과/오신뢰. 옛2023 소개의40%와 새 소개32%를 같은 결과로 혼합하지 않음 |
| https://coauthor.stanford.edu/ | 2022논문 링크; 영어63명/1445세션, GPT3 | 제안 수용·거절·수정의 상호작용 기록. 참가자는 crowd workers이며 전문 소설가 표본으로 부르지 않음 |
| https://github.com/stanford-oval/storm | 연구2024; README에는2025-01 통합 소식 | 관점별 질문→검색→개요→인용 원고, MIT, Python/검색·모델 설정 필요. README도 발행 전 편집 필요를 명시 |
| https://aclanthology.org/2024.naacl-long.347/ | NAACL2024-06 | 초록의 STORM 사전 집필 설계와 Wikipedia 편집자 평가; 전체 PDF/현재 한국어 성능 재현은 미실시 |
| https://aclanthology.org/2023.emnlp-main.398/ | EMNLP2023-12 | 초록의 유창성/정확성/인용품질 분리. 2023ELI5결과를 현재 모든 모델 오류율로 일반화하지 않음 |
| https://developers.google.com/tech-writing/one | Last updated2025-03-28 UTC | 독자 지식, 능동태, 문단 하나의 주제, 용어 일관성. 영어 교육 과정이며 한국어 효과 실험 아님 |
| https://diataxis.fr/ | 원문 발표/수정일 미확인 | 튜토리얼/목적별 방법/참조/설명의 독자 필요 구분. 모든 글을 같은 형식으로 강제하지 않음 |
| https://raw.githubusercontent.com/anthropics/skills/main/skills/doc-coauthoring/SKILL.md | 원문 날짜 미확인 | 문맥 수집→구조/수정→새 문맥의 Reader Claude. AI 독해 검사를 실제 사람 시험과 구분; 이번에는 연구 자료로만 읽음 |
| https://github.com/languagetool-org/languagetool | 원문 날짜 미확인 | 영어 등 교정, core LGPL2.1; 한국어 지원/교정품질 근거는 이번에 확보하지 못함 |
| https://quarto.org/docs/authoring/markdown-basics.html | 원문 날짜 미확인 | Markdown 기반 구조화 집필/출력 문서. 글쓰기용 언어모델 자체와 구분 |
| https://raw.githubusercontent.com/quarto-dev/quarto-cli/main/COPYING.md | Copyright2020~2024; 개정일 미확인 | Quarto CLI MIT. 의존 구성요소 조건과 별개 |
| https://www.thecreativepenn.com/2024/06/21/collaborative-writing-with-ai-with-rachelle-ayala/ | 2024-06-21 인터뷰 | 작가의 브레인스토밍→장면 행동/갈등/선택 지시→상호 수정. 본인 경험이며 도구별 당시 취향·기술 설명을 현재 사실로 복제하지 않음 |

### 게임 제작: 확보한 원문과 확인 범위

| 원문 URL | 원문 날짜/적용 조건 | 실제 읽은 범위·해석 제한 |
| --- | --- | --- |
| https://www.ubisoft.com/en-us/company/how-we-make-games/technology | 원문 날짜 미확인 | Ghostwriter는 barks 초안, NeoNPC/Teammates는 실험/연구. 사용 가능 범용 제품·상용 전면 도입·성과 측정으로 확대하지 않음 |
| https://www.ubisoft.com/en-us/studio/laforge/news/7CCHPeIseXSW1P49L4XZ7l/generating-video-game-scripts-with-style | 2023-11-27 | 기존 캐릭터 대사를 검색하는 스타일 모듈과 생성 모듈 결합,23게임 데이터. 연구용 사내 데이터는 공개 초보자 도구가 아님 |
| https://github.com/godotengine/godot | 원문 날짜 미확인 | 2D/3D 엔진, MIT; 별도 모델/API 불필요한 엔진과 AI보조 연결 구분 |
| https://docs.godotengine.org/en/stable/getting_started/first_2d_game/index.html | stable가변 경로, 원문 날짜 미확인 | 첫 완결2D게임 과정과 프로그래밍 선행 경험 요건. 완전 코딩 초보용 즉시 실습으로 약속하지 않음 |
| https://github.com/phaserjs/phaser | 원문 날짜 미확인 | 2D 브라우저 게임 프레임워크, MIT; 작성 언어/웹 도구 학습 별도 |
| https://phaser.io/tutorials/making-your-first-phaser-3-game/part1 | Phaser3튜토리얼; 게시/수정일 미확인 | 첫 웹게임의 출발 과정. 현행 모든 버전에 그대로 재현 검증한 것은 아님 |
| https://github.com/4ian/GDevelop | 원문 날짜 미확인 | 이벤트/행동 기반 엔진; Core/GDJS/newIDE/Extensions MIT, 상표/온라인 서비스 분리 |
| https://gdevelop.io/blog/make-games-with-ai-agent-gdevelop-automated-prompt | 원문 표기9.10.2025를 그대로 보존 | 객체/이벤트 수정, 작은 요청/반복/검토, AI credit 조건. 현행 화면의 위치·요금·크레딧 수는 미검증 |
| https://wiki.gdevelop.io/gdevelop5/tutorials/platform-game/ | 원문 날짜 미확인 | 플랫폼 게임/수집 요소 튜토리얼의 도입 범위; 전체 실습 실행 미실시 |
| https://github.com/inkle/ink | 원문 날짜 미확인 | 분기 서사 언어, Inky와 초보자 튜토리얼 링크, MIT. 범용 물리/렌더링 엔진 아님 |
| https://github.com/renpy/renpy | 원문 날짜 미확인 | 비주얼 노벨 엔진과 라이선스 원문 연결 |
| https://www.renpy.org/doc/html/license.html | 문서8.5.4표시; 게시/수정일 미확인 | 대부분 MIT, LGPL유래 부분과 동봉 구성요소 별도. 전체 배포물을 단일 MIT로 표시하지 않음 |
| https://github.com/CoplayDev/unity-mcp | 원문 README에2026-10-04 v10.3.0; 이번 릴리스 전체 감사 아님 | 에셋/씬/C#·테스트·빌드 도구, Unity2021.3LTS~6.x/Python3.10+, MIT. Unity공식 제품으로 부르지 않음 |
| https://raw.githubusercontent.com/CoplayDev/unity-mcp/main/unity-mcp-skill/SKILL.md | 원문 날짜 미확인 | 실제 name=unity-mcp-orchestrator; 상태/대상 확인→작업→컴파일·콘솔·이미지 검증. beta도 읽었으나 설명은 main에 근거 |
| https://github.com/Coding-Solo/godot-mcp | 원문 날짜 미확인 | 실행/로그/씬/노드/리소스, Godot+Node18+MCP클라이언트, MIT. 엔진 공식 연결로 오인하지 않음 |
| https://raw.githubusercontent.com/openai/plugins/main/plugins/game-studio/.codex-plugin/plugin.json | manifest0.1.2; 발표/수정일 미확인 | 공개 Game Studio plugin의 OpenAI저자/MIT/스킬 경로. 이 계정의 설치·제공 여부는 별개 |
| https://raw.githubusercontent.com/openai/plugins/main/plugins/game-studio/skills/game-studio/SKILL.md | 원문 날짜 미확인 | 게임 목적/반복 규칙/실행 경로/아트/플레이테스트의 분기; 브라우저게임 대상 |
| https://raw.githubusercontent.com/openai/plugins/main/plugins/game-studio/skills/web-game-foundations/SKILL.md | 원문 날짜 미확인 | 규칙 상태와 렌더링 분리, 입력·저장·성능 경계. 모든 엔진의 필수 구조로 일반화하지 않음 |
| https://raw.githubusercontent.com/openai/plugins/main/plugins/game-studio/skills/phaser-2d-game/SKILL.md | 원문 날짜 미확인 | Phaser+TS+Vite, 씬과 규칙 분리, HUD/에셋 구성 |
| https://raw.githubusercontent.com/openai/plugins/main/plugins/game-studio/skills/three-webgl-game/SKILL.md | 원문 날짜 미확인 | 명시적3D루프/Three.js, GLB, Rapier, DOM UI |
| https://raw.githubusercontent.com/openai/plugins/main/plugins/game-studio/skills/react-three-fiber-game/SKILL.md | 원문 날짜 미확인 | 기존React내3D, pmndrs, 고빈도 상태와 UI 경계 |
| https://raw.githubusercontent.com/openai/plugins/main/plugins/game-studio/skills/game-ui-frontend/SKILL.md | 원문 날짜 미확인 | HUD/메뉴 가독성, 플레이 영역·카메라 입력 보호 |
| https://raw.githubusercontent.com/openai/plugins/main/plugins/game-studio/skills/sprite-pipeline/SKILL.md | 원문 날짜 미확인 | 기준 프레임→전체 strip생성→크기/앵커 정규화→미리보기/엔진 확인. imagegen 의존, 실행/생성 미실시 |
| https://raw.githubusercontent.com/openai/plugins/main/plugins/game-studio/skills/game-playtest/SKILL.md | 원문 날짜 미확인 | 실제 입력/화면/로그를 통한 QA,재현 절차; 초보자 사람의 재미 평가와 별개 |
| https://raw.githubusercontent.com/openai/plugins/main/plugins/game-studio/references/playtest-checklist.md | 원문 날짜 미확인 | 시작/입력/종료/복구·화면 크기·카메라/메뉴 확인과 심각도별 재현 보고 |

### 실패·부분 검토·보류

- NBER논문 소개 URL은 웹 도구 Internal Error로 확보 실패. 검색에 나온14%/34%를 이번 채팅의 확인된 수치로 사용하지 않는다.
- MIT ORC중계 페이지는502; MIT News의 연구기관 원문으로 대체했다. 대체 성공이 원 URL의 성공은 아니다.
- GitHub game-studio목록은 Internal Error, README와 옛 develop-web-game 및 phaser-game 추측 경로는404. 확인된 plugin manifest와 실제 세부 SKILL.md로 범위를 확정했다. 옛 스킬을 현재 설치 후보로 안내하지 않는다.
- Ubisoft Ghostwriter newsroom상세는 Internal Error. 공식 Technology본문의 실제 요약과 La Forge별도 연구 원문만 확인 근거로 쓴다. 전체 상세 원문 검토 완료로 표기하지 않는다.
- GDevelop /page/ai,/features/ai-agent는 실패. wiki AI/chat은 Redirecting1줄뿐이므로 내용 검토 실패. 실제 확보된 공식 AI Agent블로그/엔진README로 기능을 설명하며 최신 UI 조작 재현은 주장하지 않는다.
- n8n옛 sustainable-use-license경로는 Page Not Found; 실제 저장소 LICENSE.md로 조건을 확인했다.
- 한국어 LanguageTool품질, 한국어 모델 간 순위, 상용AI가격, AI에셋의 개별 권리, 게임의 수익/제작시간은 미측정·보류. 기능문서를 성과보장으로 바꾸지 않는다.
- 새 수집기 연결·자동 조사·예약·보고서v1/quality sidecar·불변 판 발행은 이번 요청 범위가 아니다. research-check/research-audit의 신규 발행 승인으로 기록하지 않는다.

자체 검토: 제목·요약에서는 대상/사용 목적/시작 조건을 먼저 설명하고 SKILL.md와 MCP를 풀어 쓴다. 본문에서는 도구 추천을 조건에 따른 편집 판단으로 표시하고, 엔진·MCP서버·스킬을 같은 비교행으로 섞지 않는다. 가상 회의 입력의 미정 담당자, 게임 점수/타이머/재시작 값, 집필 전후 문장의 학습 정보가 이어지는지 확인했다. 모델 자기평가를 실제 독자 시험으로 부르지 않는다. 이번 작업은 자체 의미·이해 검토이며 독립 에이전트 검토/실제 독자 시험/설치 실행은 하지 않았다.

## 2026-10-09 후속 요청: AI 활용·글쓰기·게임 제작 3개 페이지 발행

사용자가 핵심을 먼저 보여 주고 기존 리서치에 각각 페이지를 추가하도록 요청했다. 위 채팅 조사 단계의 미발행·자체검토 상태와 구분한 후속 작업이다. 세 글의 ID는 practical-ai-workflows, ai-assisted-writing, ai-game-creation이며 개발 동향/AI 활용 아래에 배치한다. [작성·검토 기록](../AI_PRACTICAL_GUIDES.2026-10-09.md)에 독자 질문·예제·검증 범위를 연결했다.

- 실제 새 원본 수집: 57개 기존 URL 중56개 성공, CoAuthor1개 SSL 인증서 확인 실패. 우회하지 않았다. 원본 바이트·추출문·성공/실패 시각·해시는 ignored data/raw/research/2026-10-09-ai-writing-games/receipts.json에 보존했다. 최종 참고문헌은55개 고유 URL이며 HBS와 CoAuthor는 새 글에서 채택하지 않았다.
- 과거 최초 웹 확보의 정확한 시각은 여전히 미확인이다. 이번 실제 로컬 재수집 성공 시각을 최초 수집일로 소급하지 않는다. 원문 날짜·측정 기간은 위 기존 기록을 유지한다. quality source의 first_collected는null, last_successful_collection은 실제 영수증 시각이다.
- 첫 화면 독립 검토는 게임 스킬 정의를 수정한 뒤3편 통과했다. 본문 독립 검토는 회의 의존 관계 추측, 공개/로컬 스킬 혼합, Dify·n8n 조건, 소설 결과 장면과 수정 전후, 부적합한 원문 발췌를 수정한 뒤3편 재판정했다. 실제 최신 JSON 입력 지문과 리뷰를 연결했다. 관련 원문 절의 의미 검토와 짧은 발췌·형식 검사를 분리했다.
- 신규 report-v1/quality sidecar를 ai-practical-guides-2026-10-09 불변 배치로 연결했다. research-check3편 통과. audit5 gated/32 needs_substantive_review이며 기존32편을 이번에 승인하지 않았다. 유료 모델 호출0회, 새로운 예약/수집기 연결 없음.
- 로컬 검증:129시험,37편/127판, 기존34편/124판·모델14·기존 발행 순서·CSS 보존8항목 통과.200 HTML/10,827개 로컬 참조 누락0, 실제3화면폭30검사와 PNG 확인. 일반 수집의 GDELT429 경고1·CoAuthor SSL 실패·favicon404를 별도 기록한다. 공개 배포·확인은 진행 중이다.
- 가상 기대 표·장면·게임은 저자 설계다. 스킬/엔진 설치·실제 게임 실행·모델별 성능·한국어 독자 시험·효과 측정은 하지 않았다. 독립 에이전트 Pass를 실제 사람의 이해나 사용자 승인으로 쓰지 않는다.
