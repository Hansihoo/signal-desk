# 2026-10-10 모델 확인과 첫 증분 공개 발행

## 독자의 질문과 발행 범위

신규 모델로 같은 문의·설명서·제품 이미지 작업을 비교하려면 무엇이 달라지고,
어떤 입력·결과·가격 조건을 고정해야 하는가? API·토큰·추론 설정을 처음 접하는
개발자와 관리자를 가정한다. 공개 기능과 실제 업무 성능, 계획된 가중치와 현재
API 제공 상태, 이미지 출력 부분 가격과 요청 전체 비용을 구분하도록 설명한다.
실제 SDK/API 실습·벤치마크·사람의 독해 시험을 수행한 글은 아니다.

10월9일 준비한3가이드는 아직 공개되지 않았다. 같은 checkout에서 원격의14개
후속 커밋을 통합하고 현행 질문/근거 품질 검증을 적용해 첫 공개 발행을 완성한다.
다른 작업의 보고서37편/127판·원자료14편과 이전 모델 기록을 보존한다.
새 페이지의 출시일은6일/7일이며 오늘 출시된 것으로 표시하지 않는다.

## 오늘 수집·후보 판단

- `model-pages --collect`: 신규0/변경0/동일14, fetched14, 실패0.
- `ai-models --collect`: 신규0/변경0/동일789, retained0. 공식8관측 포함797관측.
- AI2일 후보: fetched50/신규21/변경15,12피드 실패0.
  `data/raw/ai_news/ai_news_bundle_20261009T201144Z.json`에 실제 XML을 보존했다.
- 공식14원문을 다시 확보했고 실패0. URL·최종 URL·UTC·HTML SHA-256·경로는
  `data/raw/ai_news/official/2026-10-10/receipt.json`에 보존한다. 최초 확보일·
  미확인 원문 수정일을 오늘로 소급하지 않는다.13개는3가이드 의미 대조 대상이다.
- 이번 주요 제공자 발표/변경 이력과2일 후보 범위에서3편 외 추가 신규 LLM ID를
  공식 확인하지 못했다. 이는 전 세계 신규 모델 전체의 부재를 뜻하지 않는다.
- 뉴스의 Gemini4Argon은 기존 비교표/원자료/학습 해설에 존재한다. 공식 발표는
  9월30일이며 뉴스 관찰일을 새 모델 출시일로 바꾸지 않는다.
- OpenAI10월8일 Ultrafast는 기존 gpt-6.1-sol의 service_tier 기능이고,
  Google10월8일 Deep Research Pro Preview 종료 안내는 기존 agent의 수명주기다.
  신규 모델 페이지로 만들지 않는다. 표시 요율·agent를 언어 모델의 성능과 합치지 않는다.
- Jev 후보는 non-generative decision 모델이고, GLM5.3Flash는 기존 관측에 있다.
  Meta 관련 뉴스 제목을 다른 업체 Jev의 출시 근거로 합치지 않는다.
- Falcon ASR는 TII의 음성 인식 후보로 발표 검색 결과가 확보되었으나 모델 카드
  웹 읽기는 실패했다. 발표 전문·가중치·언어별 조건을 모두 검토한 상태가 아니며
  변경 없음으로 처리하거나 코딩 성능 표에 점수를 추정하지 않는다.
- Qwen 블로그는 웹 추출 본문0줄, DeepSeek의 `/news`는 API 시작 안내로 반환됐다.
  두 경로의 완전한 최신 발표 검토는 미완료다. 실패/미검토를 변화 없음으로 세지 않는다.

## 근거와 독자 설명 검토

첫 화면만 제공한 독립 검토는 Haiku의 '입력 계산/생각의 깊이'와 Mistral의 비교
산출물 모호함을 지적했다. 토큰·검토 자원 정도를 풀어 설명하고 문의 대조표,
가상 설명서의 부품/치수/단위/쪽 대조와 API 예상 비용이라는 산출물을 명시했다.
수정 첫 화면3편은 별도 재검토를 통과했다. 본문은 그 이후에 제공했다.

본문/원문 검토에서 다음 필수 수정이 나왔고 최종 신규 배치에 반영했다.

| 지적한 위치·문제 | 원문·수정 | 확인 범위 |
| --- | --- | --- |
| Haiku Context lead가 입력 한도로만 설명 | 입력·대화·출력의 수용 범위로 정의 통일 | 용량과 정확도/무료 사용량 구분 |
| Haiku100K 경계와 캐시 입력 연결 누락 | 캐시 읽기·쓰기 포함 전체 입력. 새입력20K+캐시90K=110K이면 높은 구간 | 본문·가격 표 note·공식 가격2관측의 새 판 |
| Mistral 토큰·Context·M/B/T 선행 개념 누락 | 토큰 정의와100만/10억/1조 단위, 총/활성 파라미터 구분 설명 | 사용량·MoE·미공개 자체 서버 비용 구분 |
| Nano 반복 편집 입력 상태 연결 누락 | 이전 interaction ID 또는 생성 이미지 재전송; 둘째는 첫 이미지, 셋째는 둘째 이미지 | 가상 편집의 입력/중간 상태/출력과 승인 조건 |

이전 두 배치를 고치지 않고 `ai_model_guides_release.2026-10-10.json`으로 같은
stable ID의 revision3을 추가한다. 질문별 답·본문 위치·원문 선택 발췌·의미/한계·
주장 연결·첫 화면/본문 검토 입력 지문은 같은 이름의 quality JSON으로 발행에 연결한다.
짧은 발췌 문자열 검사는 의미 전체나 사람의 학습을 증명하지 않는다. 전체 원문
파일은 raw에 두고 public config에는 선택 발췌·hash·검토 메타데이터만 보관한다.
유료 생성/검색 API를 호출하지 않았다.

Haiku 가격 경계 보완은 `ai_model_facts.2026-10-10.json`의 같은2관측 ID로 추가했다.
`ai-models --input`: 신규0/변경2;797관측/799판. 이전 판과10월9일 입력은 보존한다.
금액·단위는 바꾸지 않고 캐시 입력을 경계 계산에서 빼는 오해를 정정했다.

## 기술·발행 검증

최종 검증·Pages Actions·공개 URL 결과는 아래에 이어 기록한다. 통합 전109시험과
기존 모델 필터/모바일 확인을 통과했다. 두번째 원격 통합 직후 전체131시험 중1개가
최신 배치의 quality 연결 전 상태에서 실패했다. 최종 품질 배치를 등록한 후 전체
회귀를 다시 실행한다. 주거 모집중0건인 기존 로컬 review 제한과 모델 검증은 구분한다.

### 최종 로컬 검증 결과

- 독립 검토자의 최종3편 판정은 모두 Pass다. 첫 화면/본문6가지 점검과
  실제 JSON 위치를 근거로 재독했다. 검토한 최종 원고 SHA-256은
  fdee8b9c6b5cf3d5d81468419d16c64a0c2176c9c44eed5849d06e2646ef346e다.
  관련13원문의 조건·가격·예시 연결과14개 raw 해시를 대조했다.
  사람 독자/실제 모델 응답/벤치마크 검증을 뜻하지 않는다.
- 최종 품질 배치 적용 후 전체131시험이102.796초에 통과했다. 앞선 최신 배치
  연결 전 실패는 해결됐으며 upstream 시험을 약화하거나 제거하지 않았다.
- research-audit:40현재 보고서 중8편은 quality 연결,32편은 새 실질 검토 필요.
  이3편의 통과로 다른32편을 승인하지 않는다.
- 현재 공개 JSON의37보고서와127이전 판은 로컬과 정확히 같다.
  최종 로컬40보고서/136판, Theo14원문, 모델797관측/799판.
- 201HTML의8042내부 href/src 참조에서 누락0. 브라우저19검사/페이지 오류0:
  3가이드320/390/768/1440px 본문·5필수장·이전 판·공식 출처,
  모델 목록17/공식3 검색·분야/초기화, 비교표8공식 관측/effort·상세·날짜/
  이력·CSV, 메인 메뉴/계수와 정식/preview 경로를 확인했다.
- reports/ai-models-oct10-local의 가이드3개/목록/비교표 PNG와
  reports/brief.png(390px),reports/desk-summary.png(645px)를 눈으로 확인했다.
  표는 자체 가로 스크롤을 유지하며 페이지 전체 넘침은 없다.
- brief/desk 생성 성공. 로컬 housing review는11PASS/1FAIL이며 실패는 기존
  모집중 공고0건이다. AI 모델 수집·발행·필터 실패로 보고하지 않는다.
- 브라우저 검증은 성공했고 이후 Edge BITS 임시 파일 잠금으로 scratch 정리만
  한번 실패했다. 소비자 종료/소유권을 재확인한 공식 실행기의 Complete로
  D:/9_codex_temp/2026-10-10/codex-scratch-signal-model-oct10-browser-8ef0db7133ed를
  정리했다. 필요한 PNG/검증 JSON/raw 영수증은 ignored 경로에 보존한다.

Pages Actions와 실제 공개 데이터·브라우저 결과는 배포 후 아래에 기록한다.

### 공개 발행 영수증

- 정확한 checkout/원격 fetch·push/프로젝트 Hansihoo 신원을 매번 guard로 확인하고
  origin main에 일반 push했다. 원본 Theo 저장소·기본 인증·전역 자격 설정은 바꾸지 않았다.
- 사이트 소스: ccd70bbc4b7e59b0f83d60d7960e8aa9bc624ecc.
  [Pages Actions37987444452](https://github.com/Hansihoo/signal-desk/actions/runs/37987444452)
  성공,2026-10-09T20:30:28Z–20:33:47Z(10일05:30:28–05:33:47 KST,3분19초).
  클라우드131시험은9.709초에 통과했고 수집/누적 상태 저장/주거review/배포가 성공했다.
  AI126건 warnings0, 일반뉴스67건 GDELT HTTP429 경고1은 대체 수집과 함께 별도 보존했다.
  Python Element truth-value/Node punycode deprecation 경고는 테스트·배포 실패가 아니다.
- 공개 JSON HTTP200 확인:2026-10-09T20:34:14.128434+00:00(10일05:34:14 KST).
  공개40보고서/136판, 모델797관측/799판, Theo 원문14편.
  reports/ai-models-oct10-live/public-after.json과 public-preservation.json에 실제
  응답·UTC·SHA-256과12개 보존검사를 보관했다. 응답 지문:
  2e732d4cfd2ac8b728a57b4dcaf61fbb006237cfb541718cd9fd60532ee4dc8f.
- 기존37현재 보고서와127이전 판 문서, Theo14원문과789원관측의 사실은 정확히 보존했다.
  현재40보고서는 로컬 입력과 같고 새3편 revision3/이전1·2판, 캐시 경계2관측
  revision2/10일 확인일이 공개 JSON에 있다. 세계 모든 모델 수를797개라고 세지 않는다.
- 실제 공개 브라우저19검사/페이지 오류0:3본문320/390/768/1440px,
  목록17페이지/공식3 검색·분야/초기화, 전체 비교표8공식 관측/effort·출처·날짜·
  이력/CSV, 정식·preview 내부 연결, 메인 메뉴 계수를 확인했다.
  가이드3편·비교표의 공개 PNG도 눈으로 확인했으며 검증 JSON은 같은 ignored 폴더에 있다.
  local/live scratch 소비자는 종료했고 실행기가 일회성 파일을 정리했다.
- 공개 링크:
  [Claude Haiku5.5](https://hansihoo.github.io/signal-desk/preview/claude-haiku-5-5-model-guide.html),
  [Mistral Large4](https://hansihoo.github.io/signal-desk/preview/mistral-large-4-model-guide.html),
  [Nano Banana2.1](https://hansihoo.github.io/signal-desk/preview/gemini-nano-banana-2-1-model-guide.html),
  [모델별 자료](https://hansihoo.github.io/signal-desk/preview/ai-model-guides.html),
  [전체 비교표](https://hansihoo.github.io/signal-desk/preview/ai-models.html).

소스 확보·공식 조건 의미 검토, 독립 첫 화면/본문 Pass, 기술 출력/공개 검증은
각각의 범위로 기록했다. 실제 모델·SDK 실행, 평가 Harness 재현, 사람의 학습 검증은
수행하지 않았다. 미검토 후보·수명주기/설정 변경을 신규 모델로 바꾸지 않는다.
생성 SQLite/HTML/PNG/원문 raw/개인정보는 commit에 포함하지 않았다.
이후 발행 영수증만 기록하는 문서 커밋은 [skip ci]로 중복 배포를 피한다.
