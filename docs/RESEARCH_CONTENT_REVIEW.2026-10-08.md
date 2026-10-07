# 리서치 내용 검토 — 독자가 이해할 수 있는가

검토일: 2026-10-08. 대상은 SQLite의 현재 보고서 **16편·상세 학습 46장**,
요약·표·데이터·결론·참고자료 및 현재 렌더링·검증 코드다.
이번 산출물은 진단, 작성 기준, 대표 보강 원고다. 기존 보고서 데이터와
공개 HTML은 이번 작업에서 재작성·재배포하지 않는다.

## 판단

자료와 설명이 아예 없는 것은 아니다. MCP Apps에는 역할·요청 흐름·공식
예제·이해 질문이 있고, Upwork에는 성장률의 분모·측정 기간·가상 계산이 있다.
가상 예시와 편집 판단을 구분한 점도 유지할 가치가 있다.

그러나 제목·표·결론을 먼저 이해하려면 이미 주제를 알고 있어야 하는 경우가
많다. 상세 해설을 모두 열어도 짧은 정의와 점검 항목 사이를 독자가 스스로
연결해야 한다. 원고의 목표가 ‘자료를 가진 보고서’에서 ‘읽고 이해할 수 있는
설명’까지 이어지지 못했다. 장 수를 늘리거나 문장을 길게 만드는 것만으로는
해결되지 않는다.

## 실제로 확인한 문제

### 선택된 MCP 표: 읽는 주체가 바뀐 문장

`mcp-apps-workflows` r2의 UI 리소스 행은
‘서버가 읽을 수 있도록 제공하는 HTML 화면’이라고 적었다. 공식 설명은
서버가 화면 리소스를 제공하고 **호스트가 읽어 표시하는 구조**다.
`서버 → 호스트`라는 같은 행의 연결 방향과도 문장 의미가 어긋난다.

보강 문장: ‘MCP 서버가 호스트에게 제공하는 HTML 화면. 호스트가 이 자료를
읽어 대화 안의 격리된 화면으로 표시한다.’
이 문제는 글의 길이가 아니라 요약하면서 역할을 바꾼 오류다.
[공식 UI Resources·Tool-UI Linkage](https://apps.extensions.modelcontextprotocol.io/api/documents/overview.html#ui-resources)를 기준으로 정정해야 한다.

### 해커톤 조회 예시: 입력 조건과 함수가 맞지 않음

`hackathon-tech-roadmap` r1의 두 번째 장은
`find_notices(region, keyword)`로 ID·제목·URL을 반환한다고 설명하면서
‘서울에서 이번 달 마감되는 공고’를 찾는다. 날짜 조건을 전달하거나
조회 후 필터링하는 단계가 없다. 반환 필드에도 마감일이 명시되지 않는다.

날짜 인자를 받는 도구와 마감일 반환값으로 고치거나, 반환 목록을 앱이 날짜로
필터링하는 단계를 설명해야 한다. 앱이 함수를 실행하고 결과를 모델에
돌려주는 역할 분담은 [공식 함수 호출 흐름](https://ai.google.dev/gemini-api/docs/function-calling)과 맞지만,
독자가 추적할 하나의 예시가 덜 완성됐다. [개선 원고](RESEARCH_WRITING_EXAMPLES.md)에
인자·샘플 데이터·반환·최종 답을 함께 제시했다.

### Tally 제목: 관찰을 성장 원인으로 읽게 함

`tally-small-saas-case` r2는 ‘Tally의 성장, 무료 제품과 지속 개선에 기반’이라는
제목이다. 저장된 근거는 창업자의 매출 공개, 제품 방향 설명, 변경 기록이다.
본문은 자체 공개 수치와 사례의 한계를 잘 구분하지만 이 자료만으로 무료
제품과 지속 개선이 성장을 일으켰다고 검증한 것은 아니다.

제목을 ‘Tally가 공개한 매출 기록과 제품 운영 방향’처럼 관찰 범위에 맞추고,
창업자의 설명과 독립적으로 확인된 인과관계를 구분해야 한다. 이번에는
해당 재무 수치·현재 실적을 새로 검증하지 않았으므로 기존 확인일을 유지한다.

### 입문 글이 다른 입문 자료로 독자를 떠넘김

해커톤 첫 장은 HTTP·JSON·비동기 응답·환경 변수를 선행 지식으로 나열한다.
읽는 사람이 이것부터 배우려는 경우에는 다음 행동이 모호하다. MCP 글도
기초 개념을 설명한 뒤 공식 Quickstart로 연결하지만 그 Quickstart는 기존
MCP 서버 제작 경험, Tools·Resources 이해, Node.js 20+를 전제한다.
[공식 준비 조건](https://apps.extensions.modelcontextprotocol.io/api/documents/quickstart.html#prerequisites)
확인 없이 ‘그대로 실행하면 된다’로 연결하면 입문 경로가 끊긴다.

개념을 이해하는 원고와 구현 준비 경로를 나누어 설명하고, 링크를 눌렀을 때
무엇을 읽고 어디까지 할 것인지 알려줘야 한다. 이 보고서 안에서 약속한
이해 목표는 외부 문서를 열지 않아도 달성할 수 있어야 한다.

### 판정 기준 대신 ‘확인하라’가 반복됨

‘정확도 확인’, ‘상태 처리’, ‘기록 보관’은 필요한 작업이지만 학습 결과가
보이지 않는다. 같은 질문의 기대 답, 실제 반환값, 실패 시 나타날 현상을
나란히 제시해야 독자가 무엇을 검사하는지 알 수 있다. 평가 글에는 사례의
종류가 이미 있어 출발점이 좋지만 실제 평가 기록 한 건이 빠져 있다.

A2A 글의 CLI 예시는 서버 준비를 외부 안내에 맡기고 공고 비교·요약 요청을
보낸다. 공식 echo 서버를 첫 연습 대상으로 쓰면 반환은 입력의 반복이다.
그 결과는 연결을 확인할 뿐 문서 분석 성공이 아니다. 학습 목적을 연결 확인으로
정했다면 `hello` 요청과 예상 `hello` 응답부터 보여주는 편이 명확하다.
[공식 echo 실습](https://a2a-protocol.org/latest/blog/2026/10/01/introducing-a2a-cli/) 참조.

## 문제를 반복하게 만든 작성·출력 방식

1. **독자의 도달점이 작업 계약에 없다.** 데이터에는 `scope`, `summary`,
   `learning` 등이 있지만 읽은 뒤 가능한 일과 선행 지식은 명시적으로 관리하지 않는다.
2. **목차와 요약이 원고를 앞선다.** `요약 → 데이터 → 결과 → 해설`로 출력한다.
   이해의 전제가 되는 설명이 모두 접혀 있고 결론 뒤에 있다. 데이터 자체가
   없는 내용을 숨긴 것은 아니지만 처음 읽는 경로가 설명을 건너뛴다.
3. **표는 의미를 연결해 주지 않는다.** ‘호스트 ↔ 서버’, ‘MCP / A2A’, ‘RAG’라는
   단어와 화살표만으로는 누가 어떤 값을 주고받는지 이해하기 어렵다.
4. **예시가 단계마다 새로 시작한다.** 개념별 짧은 예시·명령·권고가 있어도
   같은 입력과 자료가 어떻게 최종 결과가 되는지 추적하기 어렵다.
5. **제약 설명이 이해 설명보다 앞서는 경우가 있다.** 중요한 조건은 필요하지만
   무엇을 하려는지 알기 전에 제한과 ‘별도 확인’부터 읽으면 판단할 대상이 불분명하다.
6. **자동 검증의 성공을 내용 품질로 확대했다.** `validate_report`는 타입·필수
   필드·출처 ID 등을 확인한다. `review`는 주택 브리핑의 DB·HTML·PNG 상태를
   검사한다. 72개 테스트와 모바일 확인은 문장의 의미·논리·독자 이해 검증이 아니다.

이 판단은 저장된 원고와 코드에 대한 편집 검토다. 실제 독자 집단의 이해도나
소요 시간을 측정한 사용자 연구로 표현하지 않는다.

## 보고서별 목적과 보강

‘우선’은 다른 기술 글의 선행 이해에 해당하거나 구체적인 오류가 있어 먼저
고칠 대상이다. ‘다음’은 설명을 보강할 대상이며 사실 정확성을 승인했다는 뜻은
아니다. 링크는 현재 공개 보고서다. 목적은 이번 검토에서 제안한 도달점이다.

| 보고서 ID·현재 판 | 독자에게 남길 목적 | 필요한 보강 | 순서 |
| --- | --- | --- | --- |
| [mcp-apps-workflows](https://hansihoo.github.io/signal-desk/preview/mcp-apps-workflows.html) · r2 | 조회 결과를 대화 안에서 비교·선택할 때 서버·호스트·화면의 역할을 설명한다. | UI 리소스의 읽는 주체 정정. 일반 대화와 화면 비교를 하나의 공고 사례로 연결. 클릭 결과와 모델에게 전달되는 문맥을 구분. 필수 설명은 기본 읽기 경로로 이동. | 우선 |
| [hackathon-tech-roadmap](https://hansihoo.github.io/signal-desk/preview/hackathon-tech-roadmap.html) · r1 | 자신의 준비 상태에서 무엇을 어떤 순서로 만들지 정한다. | HTTP·JSON의 입문 경로. 날짜 인자·반환 필드 정정. 하나의 샘플 프로젝트와 단계별 산출물·실패 관찰. 대회 사례에서 학습 순서를 선택한 이유. | 우선 |
| [document-rag-grounding](https://hansihoo.github.io/signal-desk/preview/document-rag-grounding.html) · r1 | 답이 문서에서 나오는 과정을 설명하고 근거가 맞는지 판단한다. | 한 질문, 서로 다른 문서 문단, 선택된 근거, 최종 답을 끝까지 제시. 분할·색인·검색을 이 과정과 연결. 잘못 찾은 경우와 잘못 해석한 경우의 결과 비교. | 우선 |
| [agent-evaluation-checklist](https://hansihoo.github.io/signal-desk/preview/agent-evaluation-checklist.html) · r1 | 그럴듯한 답과 성공한 작업을 구분하며 평가 기록을 만든다. | 입력·기대 값·도구 기록·실제 답·판정 이유가 있는 한 건의 예시. 신규 학습과 기존 Evals 사용자의 전환 대응을 분리. | 우선 |
| [tally-small-saas-case](https://hansihoo.github.io/signal-desk/preview/tally-small-saas-case.html) · r2 | 자체 공개 매출과 운영 선택을 해석하고 자기 제품에 적용할 질문을 고른다. | 제목의 인과 표현 수정. 제품 방향·변경 기록·성장 관찰을 분리. 무료·유료 가치 및 고객 확보 경로는 추가 근거가 있을 때 설명. MRR 해설 유지. | 우선 |
| [voice-agent-architectures](https://hansihoo.github.io/signal-desk/preview/voice-agent-architectures.html) · r1 | 기존 앱에 음성을 연결할 구조를 고르고 책임 경계를 설명한다. | 같은 한 발화를 세 구조로 추적. 음성 인식 오류·조회 오류·응답 재생 오류를 각각 관찰. 어떤 조건에서 구조 선택이 바뀌는지 설명. | 다음 |
| [a2a-cli-agent-connections](https://hansihoo.github.io/signal-desk/preview/a2a-cli-agent-connections.html) · r1 | 원격 작업을 맡길 필요를 판단하고 첫 통신 왕복의 의미를 이해한다. | Agent Card의 필요한 항목을 사례와 연결. echo 연결 확인과 실제 문서 작업을 구분. 환경 준비·예상 출력·오류 위치가 있는 작은 실습. | 다음 |
| [openai-api-migration](https://hansihoo.github.io/signal-desk/preview/openai-api-migration.html) · r2 | 자기 코드에서 종료 대상 사용을 찾고 교체 비교 계획을 세운다. | 해당 모델을 쓰는 경우의 설정·요청·실패 예시. 기존 API 방식과 모델명 교체의 차이. 미사용 독자의 해당 여부를 초반에 구분. 게시 전 종료 일정 재확인. | 다음 |
| [github-marketplace-paid-apps](https://hansihoo.github.io/signal-desk/preview/github-marketplace-paid-apps.html) · r2 | 만들 제품 유형과 유료 등록·운영 준비를 구분한다. | App·OAuth·Action의 실제 작업 차이를 한 제품으로 비교. 설치·게시·유료 권한 상태를 순서대로 설명. webhook 예시는 전후 계정 상태까지 연결. | 다음 |
| [upwork-ai-integration-demand](https://hansihoo.github.io/signal-desk/preview/upwork-ai-integration-demand.html) · r2 | 과거 수입 성장률을 정확히 읽고 다음 수요 조사의 질문을 정한다. | 제목과 첫 설명에 미국 플랫폼·수입·2025년 범위 연결. 성장률 해설 유지. 실제 공고 사례를 보강할 때 예산·납기·요구 기술을 확인하고 가상 예시와 구분. | 다음 |
| [github-pages-storage](https://hansihoo.github.io/signal-desk/preview/github-pages-storage.html) · r1 | 발행량·크기·복사 방식으로 보관량을 계산하고 자기 운영 조건을 구분한다. | 1년 발행 수→10년 수→용량의 계산을 풀어 설명. 단일 보고서 저장과 현재 누적 스냅샷 복제의 차이를 작은 자료로 예시. | 다음 |
| [aws-activate-credits](https://hansihoo.github.io/signal-desk/preview/aws-activate-credits.html) · r2 | 비용 지원의 성격과 자기 신청 경로를 구분한다. | Provider·Org ID·투자 단계 등 용어를 조건과 연결. 승인→적용 대상 비용→유효기간·지원 종료 후 비용의 흐름. 최신 자격을 재확인하며 판정 불명확한 항목은 남김. | 다음 |
| [aws-partner-hackathon](https://hansihoo.github.io/signal-desk/preview/aws-partner-hackathon.html) · r2 | 소속 자격을 먼저 판단하고 해당할 때 제출 요구를 이해한다. | APN과 소속 조건을 풀어 설명. 해당·비해당 예시. 메시징 서비스가 수행하는 실제 작업과 AI가 수행하는 작업을 나누어 시연 구체화. | 다음 |
| [nlnet-restack-call](https://hansihoo.github.io/signal-desk/preview/nlnet-restack-call.html) · r2 | 자신의 공개 기술 프로젝트와 공모 범위의 관계를 판단한다. | 인터넷 기반 스택·오픈소스 성과물·정책 예외를 자연어로 설명. 적합·부적합·미확인 예시와 필요한 증거. 제출 전 동적 정책 재확인. | 다음 |
| [google-oss-reward-status](https://hansihoo.github.io/signal-desk/preview/google-oss-reward-status.html) · r2 | 기여 종류와 현재 신청 상태를 분리하여 지급 기대를 판단한다. | 실제 프로젝트/프로그램 이름이 무엇을 가리키는지 설명. 저장소 활동과 보상 접수를 별개로 확인하는 사례. 공식 상태 재확인. | 다음 |
| [openai-safety-bounty](https://hansihoo.github.io/signal-desk/preview/openai-safety-bounty.html) · r2 | 정상 요청·권한 경계·재현 결과·영향으로 제출 범위를 이해한다. | 정상 동작과 경계 위반을 같은 가상 사례에서 비교. 조건별 재현 기록의 형태를 보여주고 공식 제출 범위와 연결. 실제 공격 수행이나 지급 판단으로 확대하지 않음. | 다음 |

## 어떻게 고쳐 나갈 것인가

먼저 [작성 기준](RESEARCH_WRITING_GUIDE.md)의 독자·목적 메모를 만든다.
MCP Apps와 도구 호출을 대표로 한 [개선 원고](RESEARCH_WRITING_EXAMPLES.md)는
문제 상황→개념→한 사례의 과정→판단 근거를 이어 썼다. 원고만 읽고 다른
사례에 적용하는 이해 질문과 해설도 포함했다.

그다음 대표 보고서의 본문을 재작성해 필수 설명과 선택적 심화를 나눈다.
제목·요약은 완성된 본문에서 추출한다. 동일한 방식으로 나머지를 고치되
신청 안내·변경 통지·통계 해석에 같은 학습 목차를 강제하지 않는다.
각 보강은 기존 ID의 새 판으로 저장하고 원문 확인일과 변경 이유를 남긴다.

우선 MCP 표의 역할 오류, 해커톤 예시의 입출력 불일치, Tally 제목의 인과
표현은 내용 정정 대상이다. 이후 기초 설명·실제 예시·다른 상황에 적용하는
질문을 보강한다. 본 진단 문서 작성만으로 이 보고서들이 정정·재배포된 것은 아니다.

## 검토 근거와 확인 범위

- 전체 원고 읽기: `research_reports` 16편, 현재 26개 저장 판, 상세 학습 46장.
  이전 판 26개를 모두 재심사한 것은 아니다.
- 코드 확인: `housing_watch/research_data.py`, `briefing_preview.py`,
  `editorial.py`, `editorial_report.html`, `review.py`.
- 이번에 다시 확인한 기술 원문: MCP 기본 구조, Apps 개요·확장 사양·Quickstart,
  Gemini 함수 호출·구조화 출력·File Search, A2A CLI 공식 발표.
- 작성 원칙 확인: Google Technical Writing의 Audience·Documents,
  Diátaxis의 Explanation·Tutorials. 적용 방식은 프로젝트 편집 판단이다.
- 지원 공고·보상·요금·매출의 모든 사실을 10월 8일 기준으로 다시 검증한 것은
  아니다. 해당 보고서를 실제 보강·게시할 때 공식 원문을 재확인해야 한다.
- 개념 개선 원고의 예시는 설명용이며 API·MCP 서버를 구현해 실행한 결과가 아니다.
  실제 독자 이해도 시험도 아직 수행하지 않았다.

검토 기준 DB의 ID·판·내용 해시 목록을 정렬해 계산한 SHA-256:
`e845174aa74161f2f8709bd6c01d445c8e2489f4980e6577fd91895755a3a771`.
`data/research.json`의 이전 출력이 아니라 현재 SQLite 원고를 검토했다.
