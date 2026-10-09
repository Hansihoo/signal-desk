# 전체 글의 정보 가치 보강과 독립 검토

사용자 요청일: 2026-10-09. 목적: AI를 배우고 활용하는 개발자·관리자가 본문에서 필요한 지식을
얻고 자기 상황에 적용하도록 기존 글을 보강하고, 별도 에이전트가 수정된 원고를 검토한다.

대상은 현재 작성 보고서 20편과 원본 모델 자료 14편이다. 기존 작성 보고서는 같은 ID의 새 불변 판으로
발행한다. 모델 원문은 유지하고 각 원문과 별개의 학습 해설 14편을 기존 검증 보고서 계약과 SQLite에
저장한다. 원문 wrapper에 해당 해설을 연결하고 원문·공유 자산 지문이 달라지면 같은 판의 설명으로
보이지 않게 한다. 실제 추가된 해설 페이지는 페이지 수에 포함한다.

공통 지침은 research-teaching 스킬과 AGENTS/작성 가이드에 연결한다. 집필자의 이해 자체검토,
공식 원문 의미 대조, 독립 에이전트의 수정 후 원고 판정, 예제 실행/출력 검사, 실제 사람 독자 시험을
구분한다. 사람 시험은 이번에 수행한 것으로 주장하지 않는다. 렌더링 통과와 문단 수는 교육 합격 근거가 아니다.

## 작업 흐름

| Feature Name | Feature Description | Progress Status | Notes |
| --- | --- | --- | --- |
| Authoring instructions | 질문별 근거와 주제 고유의 지식, 글 유형별 판정 기준을 에이전트에 연결 | Done | 프로젝트/설치본 동기화·두 스킬 검사·별도 행동 검토 통과 |
| Authored reports | 기존 20편의 제목·요약·설명·사례와 핵심 근거 보강 | Done | 최종20편 독립 재검토 Pass; 같은 ID 새 배치, 기존53문서 보존 |
| Model companions | 모델 자료14편의 숫자·조건·적용 방법을 각기 설명 | Done | 14편 독립 재검토 Pass; 원문 전체 지문에 결합하고 원문 불변 |
| Independent reviews | 수정 원고와 근거를 읽고 구체적인 막힘·과장을 재검토 | Done | 교육20·모델14·핵심 공식근거13편 및 연결 구현의 별도 최종 판정 확보 |
| Publication verification | 예제·입력·역사 보존·출력·링크·모바일·공개 내용을 확인 | In progress | 109tests·7377참조·209브라우저 검사·예제 실행 통과; 공개 배포 확인 남음 |

## 작성 보고서마다 채울 지식

| 보고서 ID | 독자의 질문과 고유 보강 대상 | 초안·근거·독립 판정 |
| --- | --- | --- |
| document-rag-grounding | 원문이 어떻게 관련 후보가 되는가; 분할·키워드/의미 검색·메타데이터·선택·답의 관계 | Final draft / independent Pass |
| hackathon-tech-roadmap | 모델의 도구 호출 요청과 프로그램 실행·결과 반환·최종 답이 어떻게 이어지는가 | Final draft / independent Pass |
| mcp-apps-workflows | 화면의 로컬 변경과 서버 재조회·대화 문맥 갱신을 실제 값으로 구분 | Final draft / independent Pass |
| agent-evaluation-checklist | 답·상태·경로의 채점, 재시도·중복의 성공을 독립적으로 측정 | Final draft / independent Pass |
| voice-agent-architectures | 부분 전사·완료 발화·진행 중 작업·재생을 구분하고 끊김을 처리 | Final draft / independent Pass |
| a2a-cli-agent-connections | 기능 카드·요청·작업 상태·결과물과 echo/실제 작업 성공을 연결 | Final draft / independent Pass |
| openai-api-migration | 모델과 endpoint 변경, 요청·응답·파서의 전후 비교와 전환 판단 | Final draft / independent Pass |
| llm-model-comparison | 평가 단위와 성공당 비용을 계산하고 실제 작업 후보를 선정 | Final draft / independent Pass |
| github-pages-storage | 파일당 크기·중복·Git 이력·대역폭을 구분해 보관량 계산 | Final draft / independent Pass |
| github-marketplace-paid-apps | 설치 계정·선택 저장소·구매·권한 상태를 같은 제품 사례로 연결 | Final draft / independent Pass |
| aws-activate-credits | 청구 대상·잔액·유효기간으로 현금 비용과 이후 비용을 계산 | Final draft / independent Pass |
| aws-partner-hackathon | 참가 역할·기술 선택·메시지 전송과 영수증/전달 결과의 차이 | Final draft / independent Pass |
| nlnet-restack-call | 공개 공공 기술의 문제·마일스톤·예산과 참여 조건을 연결 | Final draft / independent Pass |
| google-oss-reward-status | 기여·취약점 범주·현재 프로그램 상태·보상의 차이를 실제 경로로 선별 | Final draft / independent Pass |
| openai-safety-bounty | 프롬프트 주입이 신뢰 경계를 넘는 과정과 범위에 맞는 증거 | Final draft / independent Pass |
| upwork-ai-integration-demand | 관측 수입의 지표를 읽고 납품 업무·현장 연동 역할과 필요한 역량을 정의 | Final draft / independent Pass |
| tally-small-saas-case | 유료 전환·이탈·매출과 기능 분기·고객 실험을 연결 | Final draft / independent Pass |
| polaris-government-opportunities | R&D·공급·조달 역할과 원기관 첨부의 선행 자격·부담금을 선별 | Final draft / independent Pass |
| polaris-sales-opportunities | 문서 추출의 정확도·수정 비용·고객 업무 KPI와 도입 가설을 계산 | Final draft / independent Pass |
| office-business-directions | 제품 발표의 단계와 실제 업무 변화·의존 조건을 경쟁 축으로 비교 | Final draft / independent Pass |

## 독립 검토와 원문 기록

사용자가 이번 작업에서 별도 에이전트 검토를 명시적으로 승인했다. 교육 원고 검토자와 모델 원고
검토자는 기존 글의 공백과 필요한 판정 기준을 제시한 뒤 실제 수정 원고를 읽었다. 공식 근거 검토자는
공고·지원·시장·보안의 핵심 원문을 대조했다. 사전 자문을 수정 후 통과 판정으로 계산하지 않았다.

배치 파일/내용 hash와 리뷰 범위를 아래에 남기고 제목·요약 읽기와 본문·사례 읽기를 따로 판정했다.
발견 사항, 실제 수정, 다시 읽은 결과를 이어 기록했다. 집필자는 20편과14편을 작성했고 독립 원고
판정은 다른 에이전트가 맡았다. 공식 근거 검토자는 모델 초안의 공백 편집을 도왔지만 그14편의
독립 통과 판정을 맡지 않았다.

## 수정 원고와 독립 검토 결과

작성 보고서 배치: `config/research_authoring.2026-10-09.json` — 현재20편 전체를 같은 ID의 새 판으로 작성.
최종 SHA256: `17c0d1b6e2285849232d99f680fdca2cb128568c97f2e49ddb1b517c9bcd4144`.
교육 검토자는 제목·description·deck·summary를 먼저 읽고,20편의 본문·학습 펼치기·결과·표·참고내용을
읽었다. 초안 `5d5c947c…`에서 실패를 보고한 뒤 `fcc1b9c…`, `e1f997a…`, 최종 판의 수정 문맥을
다시 읽었다. 최종20편 모두 명시한 설명 목적에서 Pass. 이는 SDK 완성 튜토리얼이나 실제 사람의 학습 승인과 다르다.

| 보고서 | 주요 실질 보강 | 독립 내용 판정 |
| --- | --- | --- |
| A2A | 통신 규칙·터미널 도구 정의, 작업 상태·산출물과 연결 시험의 차이 | Pass |
| 에이전트 평가 | 답/상태/허용 경로 교집합, 재시도 분모와 호출 수 가정 | Pass |
| AWS 크레딧 | 대상 청구·만료·비대상 비용과 지원 종료 후 현금 계산 | Pass |
| AWS 파트너 대회 | 등록 조직 자격, 전송 수락과 전달 상태, 같은 주문의 지연 알림 | Pass |
| 문서 검색 | 분할·임베딩·후보 선택, 버전 필터·지식베이스·온톨로지, 반환 후보 확인 | Pass (원리·설계) |
| Marketplace | 설치 계정과 선택 저장소, 구매 상태·기능 권한·재전송/취소 | Pass (제품 구조) |
| Pages 보관 | 본문·첨부·Git 이력·배포 크기·접속 대역폭 계산 | Pass |
| Google OSS 보상 | 기여/취약점/패치, 프로젝트 등급·비공개 목록·퍼징·재현 입력 | Pass |
| 해커톤 학습 | 동일 조회 함수·인자·반환·근거·최종 답·화면의 왕복 | Pass (로컬 조회·AI 설계) |
| 모델 비교 | v1.5 평가 단위, 시도당/성공당 비용과 업무 후보 선정 | Pass |
| MCP Apps | 동일 공고의 로컬 정렬·서버 재조회·대화 선택 전달 | Pass (동작 원리) |
| NLnet | 공개 기반 기술 정의, 개발 마일스톤·검증 성과·75일/€30,000 예산 | Pass |
| 문서 AI 기업 방향 | 계약 PDF→내부 규정→초안/승인, 연결 기능과 제공 상태 | Pass (도입 판단) |
| API 이전 | 모델 교체와 endpoint/파서 변경, Chat/Responses 응답의 차이 | Pass (이전 계획) |
| Safety Bounty | 자료→행동 신뢰 경계, OpenAI 측 수정 가능성·특정 경로50% | Pass |
| 공공 사업 | 제조 AX 선행 완료 과제·60점·기관 역할·성과·부담금 | Pass |
| 문서 AI 영업 | 필드 오류·검토시간·도구비·통합비와 구매 가설 | Pass |
| Tally | 온라인 폼 정의, 월환산/현금·전환/이탈과 시간 순서의 인과 한계 | Pass |
| Upwork/FDE | 2025 미국 계약 수입의 분모, 고객 업무 연동·현장 납품 역할 | Pass (과거 지표·역할) |
| 음성 AI | 부분/확정 전사, 재생 중단/실행 취소/오래된 결과 폐기 | Pass (동작 원리) |

독립 원문 검토자는13편의 핵심 공식 근거·단위·날짜·미확인 범위를 대조했다. 본문을 직접 편집하지
않고, 최종 판을2026-10-09 03:31:59 UTC까지 재검토하여 Pass 판정했다. 모든 참고자료의 전수 최신성 검증이 아니다.
확인한 문제와 실제 수정은 다음과 같다.

- 첫 초안에서 해커톤 함수가3인자에서2인자로 바뀌고 공고 ID/마감·출처가 끊겼다. 원래3인자·A/서울/10월18일과 source 필드를 일치시키고 마감 검색으로 질문을 제한했다.
- MCP의 새 정렬/재조회 예제도 A/B/C의 날짜·지역과 충돌했다. 기존 A서울18일/B경기30일/C서울11월3일을 유지했다.
-20건 재시도 중15건 성공에서120회를 계산할 때20건 모두1회라는 가정을 추가했다. 업무 시도와 실제 모델 호출 수를 분리했다.
- 제목·요약의 A2A/CLI, 크레딧 경로, APN, Tally, 음성 구조, 인터넷 기반 기술의 뜻을 앞에서 설명했다. APN은 네트워크이며 등록 조직과 같지 않도록 재수정했다.
- 제조 본 PDF8쪽을 읽은 뒤 선행 자격·성과·부담금/마감과 기존 미열람 문장을 모두 맞췄다. ZIP 양식1~3·실제 회사 자격은 미확인으로 남겼다.
- Safety50%를 특정 제삼자 주입/유출 경로로 제한하고 현재 OpenAI 측 수정 범위를 연결했다. AWS 영상의 “3분 초과는 볼 의무 없음” 번역을 복원했다.
- Google의 동적 원문 확보 상태를 갱신하고 OT2 목록의 비공개 한계를 절차에 반영했다.

모델 해설은 `config/model_reading_guides.2026-10-09.json`에14편을 별도로 작성했다. 독립 모델 검토자의
첫 판정은5편 Pass/9편 Revise였다. 원문 표와 기초 기록의 Pro/Max20X 차이, 가상 사용 비율,
구독 한도 소비와 API 달러 비용, Index 점수/백분율, 비용·시간 단위, Sol High/xHigh와 동점 사례,
Grok의 같은 추론 강도/다른 평가환경, Atlas QnA 이진 채점, MoE/KV의 누락 정의를 수정했다.
catalog 기준일 공란과 원문 본문에 있는 확인 날짜도 구분했다. 최종 재검토·발행 결과는 아래에 기록한다.

프로젝트 스킬과 설치본의 SKILL.md/참고문서를 동기화하고 UTF-8로 quick_validate를 실행해 둘 다 통과했다.
집필 지침의 별도 행동 검토도 질문→근거→본문 위치·글 유형별 판정·수정 후 재읽기를 실제 판단에 쓰는 규칙으로 인정했다.
처음 Windows 기본 인코딩으로 스킬 검사를 실행한 것은 cp949 읽기 실패였고 `python -X utf8`로 해결했다.

## 출력 계약과 검증 범위

해설 원고는 기존 report schema v1→SQLite 판 이력에 저장한다. `model_learning_links.json`은 본문을
저장하는 별도 지식 DB가 아니라 원자료와 해설 ID의 연결 설정이다. 지문은 HTML뿐 아니라 공유 JS/CSS와
메타데이터 전체를 포함하며 기존 `model_pages` content_hash와 같다. 바뀐 원문에는 예전 해설을 최신 판의
설명으로 끼워 넣지 않고 이전 해설·해당 과거 원문 링크를 보여준다. 역사 wrapper에는 현재 해설 본문을 붙이지 않는다.
수입 원문 자체·수집 날짜·catalog 공란을 바꾸지 않는다. 학습 해설이 실제로 만든14페이지는 페이지 수에 포함한다.

코드 검증은 지문 결합·원문 보존·공유 자산 변경 뒤 오래된 해설 차단·역사 연결·누락 해설의 깨진 링크 방지와
경로/중복 설정 거부를 검사한다. 같은 문장을 생성하는 테스트나 글 길이는 학습 품질 합격 근거로 쓰지 않는다.
실제 SDK·유료 모델 호출·원문 모든 모델 사양 재측정·개인/기업 신청·공격·결제·사람 독자 시험은 수행하지 않았다.

## 모델14편의 최종 독립 판정

최종 배치 SHA256: `9a0ae0b06d61aaf3f31436cab64968be5585eec3270caee8f3de66f63edd5140`.
별도 모델 검토자가 첫 판정의 필수 수정9편과 나머지5편을 최종 원고에서 다시 읽고14편 모두 Pass로
판정했다. 대상은 해당 수입 원자료의 읽기·비교·적용 설명이다. 공급자의 현재 가격·모델 사양을
모두 다시 검증했다는 뜻이 아니다. 각 원고에는 조건을 바꾼 연습과 풀이가 있다.

| 원자료 slug | 최종 해설의 이해 대상 | 독립 판정 |
| --- | --- | --- |
| claude-opus-5-5-model-guide | 추론 단계별 동점·비용과 다른 시험 점수 | Pass |
| codex-6-model-guide | 실제 측정한 Max와 xHigh 추천의 차이 | Pass |
| codex-claude-200usd-capacity-report | Pro/Max20X 근거 차이·미확정 요금제·가상 소비량 | Pass |
| codex-model-comparison | 기준 모델과 구독 한도 소비 배수 | Pass |
| codex-model-guide-20260909 | 시험·표본이 다른 코딩 점수의 한계 | Pass |
| coding-agent-index | v1.3 과거 판·시도 단위와 현재 판의 차이 | Pass |
| coding-agent-index-v1-4 | 점수·자동 추천·차트 필터·시도당 달러/분 | Pass |
| gemini-4-argon-model-guide | 할인 API 가격과 구독 한도 추정의 비교 조건 | Pass |
| gpt-6-1-sol-model-guide | 종합 점수와 작업별 성능·reasoning effort | Pass |
| grok-4-7-report | 같은 추론 강도·다른 평가환경과 도구/API 경로 | Pass |
| llm-coding-benchmark-reference-company-v6 | 패치·테스트·저장소 질문의 정답 기준 | Pass |
| llm-models | 파라미터·양자화·MoE·KV 캐시와 메모리 | Pass |
| model-cost-performance | API 비용·구독 소비 배수·성공당 비용 | Pass |
| windows-codex-max-guide | 화면 설정과 실제 지원·실행의 확인 | Pass |

모델 검토의 비필수 제안 하나는 v1.4 변형 연습에서 이미 정의된 단위를 한 번 더 표기하는 것이었다.
필수 내용 수정은 남지 않았다. 실제 사람에게 어려운 단어·연습이 남는지는 사람 독자 시험으로 확인해야 한다.

## 실제 실행·출력 검증

- 전체109개 unittest와 compileall 통과. Windows 기본 Python에서는 기존 모델 페이지 테스트3곳의
  `read_text()`가 cp949로 UTF-8 HTML을 읽어 실패했다. 명시적 UTF-8로 수정 후 기본 명령의8개 영향
  테스트와 독립 구현 재검토가 통과했다.
- `publish`로34현재 작성 보고서/87판·14원자료/789관측을 생성했다. 최종20+14 입력과 local SQLite
  export가 같다. 이전53문서의 `(id, revision, document)`가 모두 같으며 원자료14개 HTML/자산/메타데이터도
  baseline과 완전히 같다. 로컬/공개 DB의 저장 시각 차이는 문서 변경으로 간주하지 않았다.
-160개 HTML·7377개 내부 파일/앵커 참조 오류0. 모델14 wrapper의 중복 ID·깨진 참고 앵커0.
- 실제 headless Edge/Playwright에서1280/390/320px의 모든34보고서·14원자료 wrapper와 메인,
  검색→문서 검색 원리 글, Enter 펼치기, 해설→원자료 이동을209항목 검사했다. 가로 넘침·pageerror0.
  첫 검색 시험은 포괄적인 단어에서 단일 결과를 가정해 실패했으며 고유 제목으로 검색 조건을
  좁혀 실제 클릭 경로를 검증했다. 검색 구현을 이 가정에 맞추어 바꾸지 않았다.
- 공개 Python 예제의 원고 코드를 직접 실행했다. 서울A, 경기B, 기간 확대A/C, 빈 목록, 끝점 포함,
  뒤집힌/잘못된 날짜와 출처값을 확인했다. 별도로 가상 비용·전환·매출·검토시간 등9개 계산을 검산했다.
  API 의사 기록을 실제 공급자 응답으로 주장하지 않았다.
- `brief`, `desk --tab summary`, `review`12항목 통과. 390px 메인·검색 원리·모델 메모리 해설,
  brief/desk PNG를 실제 열어 글·단락·레이아웃을 확인했다. 원자료 iframe의 고유 폭은 기존 격리 계약을 유지한다.

검사/캡처는 기존 등록 임시 출력 루트 `reports/research-teaching-2026-10-09/`에 보존한다.
`authoring-output-checks.json`, `authoring-example-checks.json`과3개 `authoring-*.png`가 근거다.
출처 확보·실제 검토 범위는 [조사 검토 기록](ai/AI_RESEARCH_REVIEW_LOG.md)에 연결한다.
공개 사이트 최종 수치·이전 판 보존·배포 결과는 배포 후 기록한다.
