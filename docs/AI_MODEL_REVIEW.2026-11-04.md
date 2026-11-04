# 2026-11-04 VR-1.1 모델 검토

현재 상태: 상세 소개와 전체 비교표의 공개 반영 및 검증을 완료했다. 사용자가 브라우저를 활성화한 뒤2026-11-05 실제 공개 필터/상세/원문/단위/이력/링크와1280/390px 화면을 확인했다. 아래 비활성화 실패는 당시의 역사적 기록이다. 후속 결과는 [11월5일 검토](AI_MODEL_REVIEW.2026-11-05.md#전일-vr-11-공개-화면-검증-완료)에 남겼다.

## 범위와 선정

기존 main/08ac86d에서 시작했고 매 저장소/데이터 쓰기 직전에 git signal-gh verify로 정확한 루트, Hansihoo 프로젝트 CLI/GCM 및 양쪽 원격을 확인했다. 다른 dirty 변경은 보존하며 HEAD와 이번 콘텐츠만 선별 제출한다. 새 branch/clone/worktree, 전역 인증 변경이나 유료 API는 없다.

질문은 보안 수정 모델과 일반 코딩 도구의 성과/제공/가격을 어떻게 비교하는가다. Cogent의11월3일 VR-1.1은 새 공식 발표이며 이전 VR-1의 공격경로 탐색과 구분했다. IBM Palette는11월3일 연구 방법/시제품 설명이나 공개 모델 제공/가중치/가격이 확인되지 않았고, Concise-9B는11월1일 논문으로 모델 배포가 확인되지 않아 후속 연구 후보로 남긴다. 기존 LongCat/ML4/Genie4 및 baseline Grok4.7/Fable5.1을 새 출시로 반복하지 않았다. Gemini2.5 수명주기는 전일 일일 브리핑과 중복이다.

Theo model-pages17편, ai-models800개 관측의 수집은 모두 동일/실패 없음이다. 이는 전체 공식 사실 재검증이 아니다. 별도 collect --days3의 신규 모델 검색/공식/커뮤니티 후보를 살폈으며 hn-newest WinError10054는 남는다. 전일 확인된 공개 JSON32MB 제한의 sync-public을 반복하지 않았다. 실패 범위를 변경 없음으로 표시하지 않는다.

## 내용과 검토

VR-1.1의57.9%, Claude Code/Opus5.5와 Codex/GPT5.6-Cyber 각45.3%는 Cogent가 공개한190과제 결과다. 과제당3시도와 네트워크/채점 테스트 차단, 시스템별 추론 예산 차이 및 학습 오염 가능성을 함께 적었다. 동일 시도 수를 동일 연산량/비용으로 바꾸지 않았다. 동적 공식 순위표의 실제 행은 미확인이라 공급자 측정으로 한정한다. 182과제의 Fiber 사례, 이전 VR-1 IntrusionBench와 현재 수치를 섞지 않는다.

공개 API/가중치, 규모/문맥/최대 출력과 표준 요금은 미확인이다. 이전판 심사 조건을 새 판의 확정 자격으로 승계하지 않는다. Opus5.5 기본API 입력4/출력20 USD/100만토큰 및 별도 캐시읽기0.20은 실제 Claude Code 총비용이나 구독료가 아니다. 모델+harness 구성과 가중치 자체 성능도 구분한다. 코드/가상업무/실습 없이6장과 결론,4개 비교표 및6개 새 facts를 등록했다.

고정 request/recipe를 사용해 작성자 첫 화면(title/description/deck만)과 본문/원문 검토를 별도로 수행했다. 품질 gate와 authoring1판, 현재 knowledge 본문 지문 및 출처 검색을 연결했다. 이것은 독립 에이전트 검토나 사람 독해 시험이 아니다. 실제 모델 실행/회사 코드/실청구도 없다.

기존 로컬95보고서/234판,2432모델/2546관측판 및Theo17/19내용을 보존했다. 보고서96/235,모델2438/2552로 증가했다. 반복 manifest 적용은 last_seen_at을 갱신하므로 그 시각을 내용/확인일 변경으로 부르지 않는다. 나머지 본문/판/출처/확인일은 동일하다. 지식 검토 원장은 실제 knowledge의 document_digest로 연결했고 이전 원장은 보존했다.

## 원문 취득

- `launch` https://www.cogent.com/blog/vr-1.1-on-livecvebench-remediating-real-vulnerabilities / UTC `2026-11-03T20:04:55Z` / SHA256 `af6399f7ec18011440e8f8cc4284e734546fc3b0f1dc3c621244f5884b5799c5` / `data/raw/signal_review/5a24380be2202ceac5f2f673ebc7f222e285f78f603c7aedecb8dcb15c65336e.json`.
- `previous` https://www.cogent.com/blog/how-we-built-and-benchmarked-vr-1-our-frontier-cyber-reasoning-model / UTC `2026-11-03T20:04:57Z` / SHA256 `7f511fa58ad9a4f51d17cb836f2ca511fa3c43fb12f309710a0adf7a5f201453` / `data/raw/signal_review/f08855231e8baa809bb9581cbd2889b9e0ee1d05c74a8e1ca40ed64fa7e27a70.json`.
- `previous-access` https://www.cogent.com/blog/cogent-at-the-frontier-announcing-vr-1-the-first-mythos-class-ai-model-built-for-cyber-defense / UTC `2026-11-03T20:05:00Z` / SHA256 `a6fcc3c6e860f168fd4b34314e14ee951682fb2c18a0ce82dfcf1babd47f52d1` / `data/raw/signal_review/43fd289095064f6b8fa7412a51b04f804aa1ee3f937e29289d301f62b5020885.json`.
- `bench` https://livecvebench.github.io/ / UTC `2026-11-03T20:05:03Z` / SHA256 `422ae479d4adce8a6702899787a07ec16bae95115334a369cf3f3c96ca961e74` / `data/raw/signal_review/de3b11acca77dca823e8890fda7f1fa6cd114bbc27d7586639628fbad4762e6a.json`.
- `pricing` https://platform.claude.com/docs/en/about-claude/pricing / UTC `2026-11-03T20:05:08Z` / SHA256 `88e8b79e7c7cf87a4f42bdc47a08051be5df0dcc6df985098de7ee72863d2094` / `data/raw/signal_review/ea958afdf7bd25908249054910b4bdceaa465d17358bd79f7bf841f82ccf3812.json`.
- `opus` https://platform.claude.com/docs/en/models/opus-5-5/overview / UTC `2026-11-03T20:05:11Z` / SHA256 `dd4e0226a037c18059affd33a28aa5e8fab408d6834a891e5abb74087be49042` / `data/raw/signal_review/0041ba0e57e7012ed1a7ccefd79a0edf1ec3ea9788943f17a6f6af81db48dfac.json`.
- `release` https://www.prnewswire.com/news-releases/cogent-unveils-vr-1-1--its-latest-frontier-cyber-model-which-tops-livecvebench-for-vulnerability-repair-302927966.html / UTC `2026-11-03T20:05:14Z` / SHA256 `4cefd48ed7c20ab760d28582c946f59b12f3291058489b5e233b465eef4c30d4` / `data/raw/signal_review/c379be97a53923718adb413b7d1eaa171d6ef0b0d689592f96ddcfeec6d9953d.json`.

## 검증의 제한

CUA createBrowserTab이 `Local browser use is disabled in Work settings`를 반환했다. 다른 UI 자동화로 우회하지 않았다. 콘텐츠/사실/생성 HTML/HTTP 검사와 실제 화면 상호작용 검증을 구분하며, 상세 또는 비교표의 실제 공개 검증이 남아 있으면 전체 발행 완료로 기록하지 않는다. 사용자에게 Work 설정의 로컬 브라우저 활성화를 요청했다.


## 정확한 제출 소스의 검증 — 2026-11-04 05:26 KST

선정 Git index만 외부 공통 scratch로 내보내214시험(119.775초)과 품질/publish/audit를 통과했다. 공개 snapshot state-20261103T035228Z-41574657285-1.tar.gz의 SHA256 5ae28dabf263a66419ddc4ebe3a9d44419cf1f193eb87574d5b760cbd4267b40을 확인해 DB와 archive만 안전 복원했다. 보고서93/230→94/231,모델2432/2539→2438/2545,Theo17/19내용과 기존 판을 보존했고 새 소개/6facts가 입력과 일치한다.4개 표와161상대 링크/앵커를 확인했다.

첫 검증의 불변 알림배치 해시 충돌은 git archive가 core.autocrlf=true를 따라 LF blob을 CRLF로 내보낸 검증 복사본의 문제였다. snapshot 등록값/HEAD blob/변환 바이트 해시를 대조하고 내보내기에만 -c core.autocrlf=false를 적용해 해결했다. DB/불변 원고/전역 Git 설정은 바꾸지 않았다. 일부 model observation ID가 검토 입력 ID가 아닌 정규화 해시라는 점도 실제 original 필드로 대조했다. 검증 도우미의 가정 교정이며 제품 변경이 아니다.

brief390px HTML의 데이터/폭/줄바꿈 검사는 통과했다. 브라우저를 사용하지 않아 PNG가 없으므로 review의 이미지2검사만 실패했다. 현재 복원본의 활성 주거 공고는1건이며 이전 모집중0건 실패와 다르다. 이 이미지 한계와 아직 못한 실제 공개 소개/전체표 필터·상세/모바일 검증을 모델 데이터 실패와 합치지 않는다. source push/Pages/HTTP 검증은 후속으로 남는다. 필요한 품질/선정 HTML·검증 로그는 D:/9_codex_temp/2026-11-04/signal-models에 보존하고 일회성 seed/도우미와 공통 scratch는 마지막 소비자 종료 후 정리한다.


## 공개 반영과 남은 화면 검증 — 2026-11-04

Source `0830e6445373635fddfce63ad6f4c7f79322ceeb`를 현재 main에 일반 push했고 [Pages41712734403](https://github.com/Hansihoo/signal-desk/actions/runs/41712734403)가 success로20:34:43UTC에 완료됐다. 클라우드 시험/수집/생성/주거 이미지검사/누적상태 저장과 배포가 통과했다.

공개 [VR-1.1 소개](https://hansihoo.github.io/signal-desk/preview/cogent-vr-1-1-model-guide.html), [전체 비교표](https://hansihoo.github.io/signal-desk/preview/ai-models.html), 자료실과 분야4경로 HTTP200을 확인했다. 소개의27원고 본문,4표,7출처와 전체표 링크가 입력과 일치한다. HTML의 inline table-token span을 제거한 셀 텍스트로 대조했다. 잘못 가정한 preview/<id>-r1.html 경로는404였고 실제 생성기의 현재판/이전판 계약을 확인했다. 새 소개는1판이므로 별도 과거 소개 링크가 없으며 기존 과거판은 보존된다.

전체표의 내장 JSON에서6개 새 관측의 원본 입력/정확값/조건/URL/2026-11-04확인일,1판 및 첫 이력과2438현재/2545이력 일치를 확인했다. 이것은 브라우저 검색/상세 패널의 동작 검증이 아니다. 공개 화면에서 VR-1.1 검색→공식 평가와 요금→57.9% 및190과제/서로 다른 추론 예산, 미공개 표준 요금/출처/확인일/첫 판을 읽고, 소개의 전체표 링크와1280/390px 화면·넘침·키보드를 확인하는 작업이 남는다. 사용자에게 로컬 브라우저 활성화를 요청했으며 답 없이 켜졌다고 가정하거나 다른 UI 자동화로 우회하지 않았다. 전체 완료/모바일 검증 성공으로 기록하지 않는다.

원문 영수증은 data/raw에, 필요 검증 로그/품질 audit/선정 HTML 및 public-verification.json과 public-body-verification.json은 D:/9_codex_temp/2026-11-04/signal-models에 보존한다. 공개 Release의 다운로드 복제본과 공통 scratch는 소비 종료 후 정리했다. 일회성 도우미도 마지막 소비자 종료 후 정리한다. 다른 dirty 파일이나 로컬 knowledge 자료는 제출하지 않았다. 실제 모델 실행/실청구/사람 시험은 없다.
