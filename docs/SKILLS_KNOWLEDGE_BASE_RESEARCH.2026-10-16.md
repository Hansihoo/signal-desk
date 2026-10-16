# 여러 AI 스킬을 검토 지식베이스로 활용하는 조사

사용자 요청 제목은 **여러 AI 스킬을 지식베이스로 묶어 활용할 수 있을까?**이다.
개발자가 공개 스킬의 방법을 모아 현재 작업의 빠진 고려사항을 검토하는 구상의
타당성을 판단하도록 작성했다. 별도 지식베이스 프로젝트의 구현 요청은 아니다.

## 결과와 읽기 경로

- 보고서 ID: `skills-as-knowledge-base`, 현재 2판.
- 로컬 페이지: `site/preview/skills-as-knowledge-base.html`.
- 메인: `site/preview/index.html`의 최근 업데이트·자료 목록·분야에 연결.
- 분류: AI 개발 / 지식과 데이터 / 스킬 지식베이스.
- 6장·9개 세부 주제·30개 블록, 과정 도식2·차트2·표2·출처12.
- 독립 리서치이며 기존 `agent-skills-guide` 계획 및 지식베이스 입문 글은 유지.
- 현재 로컬61보고서/179판. 이전60보고서/177판과 그 행·시각·지문을 보존했다.
- commit/push/공개 배포, 유료 모델 호출, 스킬 설치와 새 KB 시스템 구축은 미수행.

## 주장과 근거의 범위

| 독자 질문 | 답 위치 | 근거와 제한 |
| --- | --- | --- |
| 무엇을 묶어 어떻게 검토하는가? | idea | 명세의 원문·참고자료 구조와 점진적 로딩을 확인. 보관/노출/적용 구분 및 검토 흐름은 설계 해석. |
| 스킬의 효과와 개수는? | evidence | SkillsBench v4와 SWE v1의 자체 보고값. 과제·모델·단위·천장 효과를 보존. 개수별 집단의 차이를 인과나 최적값으로 바꾸지 않음. |
| 같은 발상이 연구됐는가? | prior | DC·ACE·SkillSeek의 경험 재사용/증분 갱신/검색을 연결. 전체 검토 방식의 직접 검증으로 취급하지 않음. |
| 개발에서는 어떻게 쓰는가? | example | Python API 기본 필터 오류의 가상 입력→후보→선별→검토 결과. tdd·grilling 조언의 채택/조정과 React 조언 제외. 실행 결과 아님. |
| 무엇을 관리하고 평가하는가? | operate, decision | 원문·검토 항목·프로젝트 조정·결과의 분리 제안. 현재 방식/직접 스킬/검색 검토를 같은 과제로 비교하는 평가안. 실험 미수행. |

원문12건의 URL·발표/판 날짜·첫/최신 획득 시각·실제 검토 범위는
[조사 원장](ai/AI_RESEARCH_REVIEW_LOG.md#2026-10-16-여러-ai-스킬을-검토-지식베이스로-활용하는-타당성-조사)에 있다.
원문 바이트·전체 정규화 텍스트는 ignored `data/raw/research/2026-10-16-skills-knowledge/`에 보관한다.
실험 기간과 미확인 게시일을 획득일로 채우지 않았다. 최초 Python 인증서/디코딩 실패는
별도 영수증에 보존하고 Windows curl의 정상 인증서 검증으로12건을 획득했다.

## 작성·검토 기록

`config/authoring/skills-knowledge-base.request.json`에서 독자 목적·범위·표현을 고정했다.
선택 recipe는 `dab000491725d2315e6f9e340bede3341814b36c7bb3e2d7e215055294d819c6`이며
두 판에 authoring record를 연결했다. report-v1은 변경하지 않았다.

`config/skills_knowledge_research.2026-10-16*.json`의 원고와 품질 패키지,
`config/skills_knowledge_visuals.2026-10-16*.json`의 정확한 본문 지문별 화면 조합을 추가했다.
기존 공통 렌더러·CSS·JS는 작업 시작 때와 바이트가 같다.

같은 작성자가 원문 관련 절과 표·수치·조건을 대조하고 첫 화면과 본문을 별도로 검토했다.
첫 화면은 제목·소개·deck만 별도 입력으로 출력했다. 독립 에이전트 검토나 사람 독해
승인을 주장하지 않는다. 브라우저에서 표가 문단 위에 놓이는 것을 확인한 뒤 2판에서
“아래의 세 집단”을 “표의 세 집단”으로 고쳤다. 1판과 그 품질·화면 조합은 보존했다.

## 검증

- 두 판 `research-check` 통과. 최종 configured audit31 gated/30 substantive-review 필요.
  gated는 기계 계약과 에이전트 검토 연결 상태이며 사람 승인 수가 아니다.
- 관련 회귀94개 통과. 첫 묶음은82개 통과와 작성 관리 모듈의 import 경로 오류1건이었다.
  `unittest discover -s tests -p test_authoring.py`로 해당12개를 다시 실행해 모두 통과했다.
  제품 코드를 수정해 시험을 우회하지 않았다.
- 로컬 publish·brief 출력 성공. housing review는12중11개 통과, 기존 활성 공고0건으로
  1개 실패. 생성한 `reports/brief.png`를 실제 확인했다. 이 결과는 연구 내용 검토와 별개다.
- 생성 HTML718개/내부 참조58,033건에서 깨진 참조0. 새 본문12출처 URL 연결 확인.
- 실제 in-app browser의1280/390/320px 화면을 읽었다. 페이지 가로 넘침0,
  세로 과정 도식·600px 표의 좁은 영역 내 가로 스크롤·제목 줄바꿈을 확인했다.
  모바일 목차 열기→장 이동→자동 닫기, 현재 위치, 산정 근거 펼치기와 Home 등록 확인.
  새 페이지 콘솔 오류0·깨진 내부 anchor0. 이는 실제 독자 시험이 아니다.
- 원 DB27테이블 중 기존23개는 전체 행·지문이 같고, 보고서/이력/발행/품질4테이블은
  이번 ID와 배치만 제외하면 기준본과 정확히 같다. 모델 원자료·과거 판도 보존됐다.

## 지식베이스 반영과 검색 한계

현재2판의 본문 지문은 `503c78969d3341aeadc9f6d6058fc764eda5a080f3e6503d50738f56bc61aa92`,
document digest는 `3d23d0abf7dcca0f25eb4c554b4959b84334e7a6504a78099b3042d08b2be5e0`이다.
`config/content_review.2026-10-16.skills-knowledge.json`에 실제 자체 검토를 연결하고
기존69개 항목을 보존했다. knowledge_sources 포인터와 색인을 갱신했다.
현재1,092문서/2,122문단, 경고0이며 새 글은 `usable_with_limits`다.

실제 질의6개 중5개에서 이 글을 찾았다. 보관/노출/적용, Python API의 채택·제외,
충돌/유지비, SkillsBench 개수 관계는 본문과 해당 출처를 반환했다. 제목에 가까운 질문은
주요 요점과 한계를 반환해 본문 확장이 필요하다. “스킬을 세 개까지만 써야 한다는 연구
근거가 있나?”는 no_evidence였다. “SkillsBench 연구에서 스킬 개수와 성능은 어떤
관계인가?”로 묻자 해당 설명과 차트 근거를 찾았다. 실패를 지우거나 의미 검색이 보장된다고
표시하지 않는다. 검색 알고리즘은 이 글 작성에서 바꾸지 않았다.

```powershell
python -m housing_watch knowledge "스킬 보관량 노출량 적용량은 어떻게 다른가?" --limit 5 --json
python -m housing_watch knowledge "SkillsBench 연구에서 스킬 개수와 성능은 어떤 관계인가?" --limit 5 --json
python -m housing_watch knowledge --document report:skills-as-knowledge-base --section example --json
```

원문에 연결된 모든 파일/스크립트, 실제 재배포의 이용 조건, 전체 검토 방식의 개발 성과와
유지비, 사람 독해는 추가 확인 대상이다. 잠재 효과를 실측 이득으로 표시하지 않았다.

획득 영수증·분리된 검토 입력·DB 기준선·보존 결과·검색6건·출력/브라우저 검증은
`D:/9_codex_temp/2026-10-16/signal-skills-knowledge/evidence/`에 필요한 근거로 보존한다.
원문과 검증 근거가 있는 혼합 폴더이므로 폐기 완료 표시를 하지 않는다.
