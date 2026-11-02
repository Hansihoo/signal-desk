# 2026-11-03 모델 원문 검토와 LongCat-2.5 추가

현재 상태: 상세 소개와 전체표 37사실의 공개 반영 및 실제 화면 검증 완료. [Pages 41521632311](https://github.com/Hansihoo/signal-desk/actions/runs/41521632311). 아래 공개 전 기록은 당시 상태이며 최종 결과는 끝의 공개 완료 절을 따른다.

## 범위와 판단

기존 main/HEAD 49e4ef0에서 시작했다. 매 쓰기 직전 정확한 루트, Hansihoo 프로젝트 CLI/GCM, fetch와 실제 push 목적지를 git signal-gh verify로 확인했다. 다른 작업의 dirty 파일과 미발행 로컬 자료는 보존하며 신규 모델 콘텐츠만 선택 제출한다. 인증 전환이나 새 clone/worktree/branch, 유료 추론은 수행하지 않았다.

질문은 이전 LongCat 사용자와 개발자/관리자가 2.5의 시각 입력과 장기 코딩 개선, 경쟁 평가의 약점, API/가중치/비용 조건을 어떻게 비교할지다. 새 ID longcat-2-5-model-guide의 첫 판으로 작성했다. 기술 글의 11월 1일, 기업 발표/API 이력의 11월 2일과 확인일 11월 3일을 구분한다. 9월 Preview를 오늘의 신규 모델로 세지 않는다. 공식 LFM3 발표에 포함된 d1-2B는 기존 소개에 있으므로 중복 발행하지 않았다. Gemini 3.7 Flash 재보도 후보는 원 발표가 8월 13일이며 오늘의 출시가 아니다. Gemini API 이력의 11월 2일 2.5 모델 종료 예정은 수명주기 후보로 확인했으나 이번 LongCat 소개의 성능/요금에 혼합하지 않았다. 전 제공자 완전 조사나 모든 수명주기 보고서 개정을 완료했다고 주장하지 않는다.

model-pages 수집은 17개 모두 동일/실패 없음, ai-models Theo 비교표 수집은 800개 모두 동일/실패 없음이다. 이는 원문 전체 내용 재검토 수가 아니다. signal_review sync-public은 공개 JSON 32MB 제한으로 실패했다. 기존 로컬 큐는 보존하고 별도 collect로 보완했으며 hn-newest SSL EOF는 남는다. 다른 공식/커뮤니티 경로의 목록 수집 성공을 이 실패의 복구나 원문 독해로 표시하지 않는다. 이 운영 공백은 모델 원문/발행 실패와 구분한다.

## 원문과 해석

공식 기술 글은 HTTP 200이지만 SPA 제목만 받은 상태였다. CUA 브라우저에서 실제 표시된 본문/평가표와 부록을 읽고 8개 선정 평가 행, 별표와 방법을 전사했다. launch.browser-extract.r2.json은 선택 DOM 사실/방법의 수동 추출이지 전체 원문 HTTP 저장물이 아니다. 당시 실제 본문은 20,988자, UTC 2026-11-02T20:12:47.999Z에 읽었다. HTTP shell과 추출 파일 모두 raw에 보존한다.

Terminal v2.1 88.4/70.8, v4.0 38.5/3.0의 개선과 Opus5 v4.0 53.9, Program Bench 37.0 및 Vision2Web 80.2에 대한 상대 열세를 함께 적었다. 별표의 외부 인용과 Meituan 재측정, Claude Code 판/길이/추론 설정, v2.1만 3회 평균, BrowseComp 자체 방법, AutomationBench 공개 v1.0.6 600과제, SpreadsheetBench/시각 심사 차이를 보존했다. 원문 공통 %단위가 없어 임의 %로 바꾸지 않았다. 평가표 Opus5를 가격표 최신5.5와 합치지 않는다.

문맥은 정확히 1,048,576 입력+출력 토큰이다. 매개변수의 max_tokens 262,144와 퀵스타트 128K 출력 충돌을 병기하고 더 큰 값을 확정하지 않았다. 2.0 MIT를 공개 예정인 2.5에 승계하지 않았다. LongCat USD0.30/0.006/1.20과 별도 CNY2/0.04/8은 100만 토큰당 한시 할인이다. 표준가/종료일 미공개이므로 표준 요금 핵심 필드에는 넣지 않고 공식 보기의 명시적인 한시 할인 열에 보존했다. Anthropic Opus5 표준5/25와5.5 표준4/20은 별도 판/조건이다.

## 작성과 현재 상태

수집 전 request/recipe/plan을 동결했고 실제 원문 독해 후 7개 장/4개 비교표로 작성했다. 첫 화면과 본문/원문을 별도로 작성자가 검토했으며 독립 에이전트/사람 독자 검토로 부르지 않는다. 모델 실행, 한국어 회사 문서, 최소 장비, 계정/한국 접근, 실제 청구는 미수행이다. 불변 소개/quality/37개 facts 배치와 세 manifest에 연결했다. 로컬 소개 첫 판/authoring record/본문 지문 검토 원장과 지식 검색을 함께 갱신했다. 정확한 제출 소스 검증과 공개 배포는 진행 중이다.

## 획득 영수증

- `launch` https://longcat.ai/blog/longcat-2.5 / UTC `2026-11-02T20:06:01.675596+00:00` / SHA256 `32cd6e61d2c207de847143dbafa889ddfdb6d56ab418434b5df374ae9fc8d7e3` / `data/raw/model_maintenance/2026-11-03/launch-32cd6e61d2c2.raw`.
- `company` https://www.meituan.com/news/NN261102280001343 / UTC `2026-11-02T20:06:02.078172+00:00` / SHA256 `c126915b21cd5d1c88c9f1cdfd36915675b2c8fecd7345598bf0a8e6809de6be` / `data/raw/model_maintenance/2026-11-03/company-c126915b21cd.raw`.
- `change` https://longcat.chat/platform/docs/change-log / UTC `2026-11-02T20:06:01.971239+00:00` / SHA256 `eb7b34c83f733626c8441c06f5f49cf98bec3a30beb075e64652fd066ee34572` / `data/raw/model_maintenance/2026-11-03/change-eb7b34c83f73.raw`.
- `pricing` https://longcat.chat/platform/docs/pricing/longcat-2.5 / UTC `2026-11-02T20:06:01.916465+00:00` / SHA256 `f8fc1d8021634b47d23f47240ee249233f5cf323f893b3989bdd803c3d4982de` / `data/raw/model_maintenance/2026-11-03/pricing-f8fc1d802163.raw`.
- `params` https://longcat.chat/platform/docs/api/model-params / UTC `2026-11-02T20:06:01.977836+00:00` / SHA256 `40310f386afe5a3f7836727beccb438d411e502815f534ed80b6e5c13262a061` / `data/raw/model_maintenance/2026-11-03/params-40310f386afe.raw`.
- `quick` https://longcat.chat/platform/docs/ / UTC `2026-11-02T20:06:02.254899+00:00` / SHA256 `54422109943d2386a11f0b9819435ac10a48726638cfbee692ba26def336b6cb` / `data/raw/model_maintenance/2026-11-03/quick-54422109943d.raw`.
- `previous` https://huggingface.co/meituan-longcat/LongCat-2.0/raw/main/README.md / UTC `2026-11-02T20:06:02.317906+00:00` / SHA256 `465f906597726afdce4d58afb00e8bde1766e4886c26860becc2d3fd2edbedc9` / `data/raw/model_maintenance/2026-11-03/previous-465f90659772.raw`.
- `claude-price` https://platform.claude.com/docs/en/about-claude/pricing / UTC `2026-11-02T20:06:02.981042+00:00` / SHA256 `0e1f4c98b788ec483f011d5bf4b56ed4435771d5ad7f3993079cfae0260caf1e` / `data/raw/model_maintenance/2026-11-03/claude-price-0e1f4c98b788.raw`.

## 정확한 제출 소스와 화면 검증

Git index의 선정 콘텐츠와 HEAD만 공통 소유 scratch로 내보냈다. 공개 snapshot state-20261102T021128Z-41376262930-1.tar.gz의 SHA256 387f9acb28f4ce93b62e671b2605cc1070ae0799cdcacb287861275f90b1facc를 확인하고 DB/archive만 안전 복원했다. 정식 소스에서 214시험 106.706초, 소개 품질 검사, publish/research-audit/brief390/review가 통과했다. audit의 기존 29편 내용 검토 필요는 새 소개 승인으로 바꾸지 않았다. 공개 예정 JSON 93보고서/2432관측에서 새 소개와 37개 facts가 입력과 같다. 로컬 기존 94보고서의 판/본문/갱신일과 2395관측의 판/본문, 기존 이력 수는 보존했다.

CUA에서 소개 PC1280/모바일390의 실제 스크린샷과 본문을 읽었다. 4개 표/내부 앵커/전체표 연결과 가로 넘침 없음을 확인했다. 전체표 공식 보기와 LongCat 검색에서 88.4/평가판/추론/실행 조건/공통 % 미표기, USD0.30/0.006/1.20 한시 할인과 표준 미공개, 별도 CNY2/0.04/8, 자료 원문/11월3일 확인일/첫 판을 실제 상세에서 대조했다. 닫기 버튼의 접근 이름을 실제 aria-label로 고친 것은 검증 locator의 수정이며 제품 코드 변경이 아니다.

주거 brief PNG는 기존 출력 계약을 확인한 것으로 현재 주거 자격/마감 재검토가 아니다. 모델 콘텐츠 완료와 별개다. 공통 scratch는 마지막 소비자 종료 후 정상 정리됐으며 필수 원문/품질/검증 로그와 선정 공개 HTML만 외부 작업 폴더에 보존한다. 모델 실행/청구/독립 사람 시험은 미수행이다. 공개 배포/화면 검증은 진행 중이다.

## 공개 완료 — 2026-11-03 05:50 KST

Source `0bf2c3741b5961bbc963fc0245c26fb6556b20b6`를 기존 main에 일반 push했고 [Pages 41521632311](https://github.com/Hansihoo/signal-desk/actions/runs/41521632311)가 성공했다. 신규 [LongCat-2.5 소개](https://hansihoo.github.io/signal-desk/preview/longcat-2-5-model-guide.html)와 [전체 비교표](https://hansihoo.github.io/signal-desk/preview/ai-models.html)가 같은 작업에서 반영됐다. 원본 수집만의 완료로 세지 않는다.

첫 실행 41520070635는 Deploy website에서 GitHub OIDC ID 토큰 요청 시간 초과로 실패했다. id-token: write는 이미 선언돼 있었다. 같은 실행의 실패 작업 재시도는 github-pages 산출물 2개로 중단됐다. 동일 소스의 새 workflow_dispatch 실행으로 중복 산출물 원인을 피하고 성공했다. 권한이나 소스 변경으로 고쳤다고 주장하지 않으며 두 실패 로그도 보존한다.

공개 JSON의 새 소개와 37개 관측 원본/fields/출처/11월3일 확인일/첫 판이 검토 입력과 정확히 같다. 기존 92현재 보고서와 229이전판 및 report_versions, 2395모델 관측/2502이력과 Theo17현재/19이력이 그대로다. 현재 93보고서/230이전판, 2432모델/2539이력이다. 소개/전체표/기존 Mistral3판 HTTP200을 확인했다.

CUA에서 실제 공개 소개와 전체표를 연결해 검색/공식 보기/평가와 요금 상세를 열었다. 평가값 88.4, 원문 수치/공통 %미표기, 평가판/추론/실행 조건과 원문/날짜/첫 판, USD0.30/0.006/1.20의 한시 할인 및 표준 미공개, 정확한 문맥과 출력 충돌을 대조했다. 공개 PC/390px의 본문과 모바일 표·상세에서 가로 넘침이 없고 링크가 동작한다. 기존 판과 비교표 이력은 삭제하지 않았다. 실제 추론/실청구/계정/한국어 회사 문서/독립 사람 시험은 미수행이다.

요구된 원문/품질/선정 화면·로그/공개 보존 근거는 D:/9_codex_temp/2026-11-03/signal-models에 유지한다. 원본 GitHub 자산을 보존한 채 검증에 사용한 다운로드 복제본과 일회성 도우미만 마지막 소비자 종료 후 정리한다. 다른 dirty 변경/로컬 지식 구현과 원장은 제출하지 않았다.
