# 2026-10-09 신규 모델 확인·발행 검토

## 독자의 질문

현재 모델에서 무엇이 바뀌었고 어떤 작업으로 비교해야 하는가? 모델명·Context·
입출력 단가를 처음 읽는 독자를 가정한다. 읽은 뒤 신규 모델의 정확한 ID와 제공
상태를 구분하고, 가격의 단위·요청 조건을 설명하며 동일 입력의 검사를 설계할 수
있어야 한다. API 실행·실제 독자 시험·벤치마크 재현을 수행한 글로 제시하지 않는다.

## 비교 기준과 판정

- 작업 시작: clean main, origin/main과 동일. 기존 789관측/789판·428모델명·
  Theo 14문서/14판과 발행 보고서를 비교 기준으로 확인했다.
- `model-pages --collect`: 신규0/변경0/동일14, 실패0.
- `ai-models --collect`: 신규0/변경0/동일789. 최초 연결 항목을 신규 출시로 세지 않았다.
- AI 2일 후보 수집: fetched50/inserted23/updated13, 피드 실패0. 검색·뉴스 제목은
  후보이며 공식 모델 사양이나 성능 증거로 사용하지 않았다.
- 10월6일 Mistral Large4·Nano Banana2.1, 10월7일 Haiku5.5는 공식 출시
  ID가 있고 위 기준에 없었다. 오늘 출시로 표기하지 않고 10월9일 새로 검토·추가한다.
- Sonnet5.5의 캐시 읽기 $0.20→$0.10은 기존 모델 가격 변경으로만 기록한다.
- OpenAI 10월7일 ChatGPT 발표의 GPT6Sol/Luna는 기존 ID이며 Chat 경험 확대다.
  chat-latest 갱신·Decisions API·도구 라이브러리 릴리스도 신규 모델 페이지로 세지 않는다.
- LiquidAI open d1 후보는 토큰을 생성하지 않는 decision 모델이다. Falcon ASR는
  음성 인식 후보다. 범용 생성·코딩 모델 표에 같은 지표로 합치지 않고 뉴스 후보를
  보존한다. Falcon 발표 본문은 웹 읽기에서 확보하지 못했으며 사양·가격을 추정하지 않았다.
- 주요 제공자 공개 발표·모델 목록·변경 이력을 확인했지만 전 세계 모델의 완전한
  발견이나 모든 기존 수치의 재검증을 보장하지 않는다.

## 원문·의미 검토

| 모델 | 공식 근거 | 기록 조건·미확인 사항 |
| --- | --- | --- |
| [Haiku5.5](https://www.anthropic.com/claude-haiku-5-5) | [사양](https://platform.claude.com/docs/en/models/haiku-5-5/overview) / [가격](https://platform.claude.com/docs/en/about-claude/pricing) / [이전](https://platform.claude.com/docs/en/models/haiku-5-5/migration-guide) | claude-haiku-5-5·1M Context·128K 일반 출력·medium. 요청 프롬프트≤100K/>100K 두 요율, 캐시5m/1h·Batch·지역. 동일 텍스트의 토큰 재계산. 시스템 카드 본문 확보 실패로 평가별 effort/Harness/시도수 검토 미완료; 점수 미입력. |
| [MistralLarge4](https://mistral.ai/news/mistral-large-4/) | [카드](https://docs.mistral.ai/models/mistral-large-4) / [변경 이력](https://docs.mistral.ai/resources/changelogs) | Public Preview·mistral-large-4·총1.05T/활성52B·1M. 카드의 USD 할인/일반 요율, 2주50% 할인. 정확한 할인 종료 시각·라이선스·출력한도·지식기준·메모리 미확인. 가중치 공개는 월말 계획, 다운로드 완료 아님. |
| [NanoBanana2.1](https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1) | [출시](https://ai.google.dev/gemini-api/docs/changelog) / [가격](https://ai.google.dev/gemini-api/docs/pricing) / [사용](https://ai.google.dev/gemini-api/docs/image-generation) | stable GA·gemini-nano-banana-2.1·131072입력/32768출력. 이미지·텍스트/추론·검색 요금 분리. 1K/2K/4K 정사각형 장당 출력 상당 가격; 전체 요청 가격 아님. 이전 ID deprecation·종료일 미정. 문자/반복 편집 개선은 제공자 설명. |

14개 원문 HTML을 `data/raw/ai_news/official/2026-10-09/`에 URL·확인 UTC·
최종 URL·SHA-256과 함께 저장했다(모두 성공). 모델 실행을 하지 않아 실사용·
AA·Agent·Cursor 점수를 추가하지 않았다. 제공자 평가판·도구 유무의 구분과
미확인 설정을 본문에 설명했다. 비공개 엔진/UI·고객·계약 정보를 사용하지 않았다.

## 독자 이해 자체검토

Haiku는 문의 분류→요청 길이별 비용→4.5 이전→동일 문의 검사, Mistral은 설명서
표/도면 추출→미리보기/가중치→비용→근거·단위 검사, Nano는 제품 이미지
생성/반복 편집→해상도·출력→부분 비용→문자·제품 형태 검사의 같은 예시를 이어간다.
수용량·가격·기대 결과·실패 기준은 본문 5장씩에 둔다. 가상 계산과 편집 판단,
공식 사실을 구분하며 실제 독자 이해 시험을 했다고 주장하지 않는다.

- Haiku 가상 1M입력/0.2M출력: 짧은 요청 구간 $0.20, 긴 요청 구간 $1.00.
  합계 토큰 수로 구간을 정하지 않는다. 캐시/할인/도구 없이 단순 계산.
- Mistral 가상 1M입력/0.2M출력: 할인 $1.098, 일반 표시 $2.196. 캐시/도구 제외.
- Nano 가상 1K 정사각형 3장: 이미지 출력만 $0.1008. 입력/텍스트/추론/검색 제외.
- Haiku JSON 요청은 공식 migration의 adaptive/effort 형식을 확인했으나 실행하지
  않았다. 의미상 기대 분류와 JSON 보장 여부를 구분했다. Nano는 사용 버전에 따라
  확인해야 하는 인자를 가짜 SDK 튜토리얼로 만들지 않았다.

### 현행 집필 기준 적용과 두 가지 읽기

원격의 research-teaching 기준을 통합한 뒤 첫 원고를 다시 읽었다. 제목·요약만
읽으면 작업과 산출물은 보이지만 API·토큰·캐시·effort·가중치·GA를 처음 접하는
독자가 본문을 따라가기 어렵고, 본문에는 일부 예시의 실제 입력·기대 출력과
조건을 바꾼 연습이 부족했다. 이 판정은 집필자의 자체검토이며 독립 독자의 평가가 아니다.

적용한 첫 배치를 고치지 않고 `ai_model_guides_learning.2026-10-09.json`으로
같은 ID의 revision2를 추가했다. 제목·요약만 읽어 모델별 할 일과 한계를 설명하는지,
본문을 읽어 같은 예시의 산출물을 만들고 조건 변화에 대응하는지 나누어 검토했다.
Haiku는 가상 문의3개의 분류와 제품명 null 조건, Mistral은 가상 설명서의25mm·
쪽2·도면A 근거와25/30mm 충돌, Nano는 제품 이미지 생성/편집과 재시도 비용을
입력·기대 산출물·오답 조건·변형 문제 및 풀이로 연결했다. 캐시/effort 선행 개념은
05:36 KST에 추가 확보한 공식 두 문서와 대조했다. 가상 출력은 실제 모델 응답이 아니다.

2026-10-09 05:43 KST 기준, 최초12원문의 실제 확보는05:13:16–05:13:28 KST,
추가2원문은05:36:47 KST다. 전체 최초 수집일이나 원문 수정일을 이 시각으로
소급하지 않는다. 정확한 URL·UTC·해시는 receipt.json과 AI_RESEARCH_REVIEW_LOG에
연결한다. 현재 공개20보고서/53판은 내려받은 public-before.json과 내용 단위로
대조했고 모두 보존했다. 최종 통합 상태는23보고서/59판이다.

## 불변 입력·탐색

- 보고서3편: `config/ai_model_guides.2026-10-09.json`, stable ID는
  `claude-haiku-5-5-model-guide`, `mistral-large-4-model-guide`,
  `gemini-nano-banana-2-1-model-guide`. `개발 동향 / AI 모델·API` 아래 발행.
- 공식 사실8관측: `config/ai_model_facts.2026-10-09.json`.
  Haiku 사양/2요금구간, Mistral 사양/요금, Nano 사양/요금, Sonnet 캐시 변경.
  `ai-models --input`과 모델 publication manifest로 클라우드에도 유지한다.
- 이미 적용된 JSON은 수정하지 않는다. 이전 모델·보고서·원본은 보존한다.
- 학습 보강은 별도 불변 배치로 등록해 각 가이드 revision1과 revision2를 모두
  보존한다. 기존20개 보고서의 발행본·이전 판은 수정하지 않는다.
- `-model-guide` stable ID와 AI 모델·API 경로를 가진 검토된 보고서는 모델별 자료
  목록의 공식 모델 가이드로 자동 포함한다. 원문 확인일 표시, 기존 검색/분야 필터와
  정식/preview 상대 링크를 사용한다. Theo 원자료 날짜와 sandbox 본문은 유지한다.

## 기술·공개 검증

원문·의미 검토와 이해 자체검토는 기술 시험 통과와 별개의 확인이다. 원격 통합 후
전체108시험, 목차 집계 추가 후 영향20시험 통과. 최종 로컬123HTML의3908내부
참조에 누락0. 실제 브라우저19검사에서3가이드×320/390/768/1440px의 본문·
날짜·출처·이전 판과 자료17페이지의 검색/분야/초기화·날짜 폭, 비교표8추가관측의
검색·effort·상세 출처/날짜/이력·CSV를 확인했다. 원본 Theo sandbox의5필터·
비어 있는 결과·초기화·Escape도 별도 통과했다. 콘솔 오류·화면 가로 넘침0,
브리핑/데스크/모델 페이지 PNG를 육안 확인했다.

증거는 무시된 reports/ai-models-oct9-local/에 보존한다. 일회용 Edge 프로필과
검사 스크립트는 소유 scratch runner로 정리했다. 주택 review는11PASS/1FAIL로,
기존 로컬 모집중0건만 실패했다. 모델 기능 실패와 구분한다. API·SDK·모델 실행,
사람/독립 에이전트의 독해 시험과 독립 벤치마크 재현은 미실시다. Pages Actions와
실제 공개 페이지 검증 결과는 배포 후 추가한다.
