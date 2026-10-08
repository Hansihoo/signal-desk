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

12개 원문 HTML을 `data/raw/ai_news/official/2026-10-09/`에 URL·확인 UTC·
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

## 불변 입력·탐색

- 보고서3편: `config/ai_model_guides.2026-10-09.json`, stable ID는
  `claude-haiku-5-5-model-guide`, `mistral-large-4-model-guide`,
  `gemini-nano-banana-2-1-model-guide`. `개발 동향 / AI 모델·API` 아래 발행.
- 공식 사실8관측: `config/ai_model_facts.2026-10-09.json`.
  Haiku 사양/2요금구간, Mistral 사양/요금, Nano 사양/요금, Sonnet 캐시 변경.
  `ai-models --input`과 모델 publication manifest로 클라우드에도 유지한다.
- 이미 적용된 JSON은 수정하지 않는다. 이전 모델·보고서·원본은 보존한다.
- `-model-guide` stable ID와 AI 모델·API 경로를 가진 검토된 보고서는 모델별 자료
  목록의 공식 모델 가이드로 자동 포함한다. 원문 확인일 표시, 기존 검색/분야 필터와
  정식/preview 상대 링크를 사용한다. Theo 원자료 날짜와 sandbox 본문은 유지한다.

## 기술·공개 검증

검증과 배포 결과는 작업 완료 후 아래에 기록한다. 원문·의미 검토와 이해 자체검토는
기술 시험 통과와 별개의 확인이다. 주택 모집중0건인 기존 로컬 review 제한도
모델 기능 실패와 구분한다.
