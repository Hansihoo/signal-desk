# 에이전트 활용 기술의 7개 조사 계획 페이지

사용자가 지정한 표의 7개 행을 각각 한 페이지로 등록한다. 2026-10-13 후속 답변에서 목차와 조사 계획부터 등록하기로 명시했다. 상세 기술 리서치나 실행 검증을 완료한 페이지로 표시하지 않는다.

## 페이지와 후속 조사 범위

| 표의 기술 | 안정 ID와 공개 페이지 | 큰 목차 | 세부 목차 |
| --- | --- | --- | --- |
| 스킬 | [agent-skills-guide](https://hansihoo.github.io/signal-desk/preview/agent-skills-guide.html) | 4 | 12 |
| 문맥 관리·지식 검색 | [agent-context-knowledge-guide](https://hansihoo.github.io/signal-desk/preview/agent-context-knowledge-guide.html) | 4 | 12 |
| 도구 호출·MCP | [agent-tools-mcp-guide](https://hansihoo.github.io/signal-desk/preview/agent-tools-mcp-guide.html) | 4 | 12 |
| 작업 흐름·멀티 에이전트 | [agent-workflow-multi-agent-guide](https://hansihoo.github.io/signal-desk/preview/agent-workflow-multi-agent-guide.html) | 4 | 12 |
| 하네스·체크포인트 | [agent-harness-checkpoints-guide](https://hansihoo.github.io/signal-desk/preview/agent-harness-checkpoints-guide.html) | 4 | 12 |
| A2A | [agent-a2a-guide](https://hansihoo.github.io/signal-desk/preview/agent-a2a-guide.html) | 4 | 12 |
| 평가·실행 기록 | [agent-evaluation-traces-guide](https://hansihoo.github.io/signal-desk/preview/agent-evaluation-traces-guide.html) | 4 | 12 |

각 페이지는 작성 목적→요약→큰 목차와 세부 목차→조사 질문→예정 결과→공식 참고자료의 순서다. 도구 설치·실습·사례의 실제 결과는 후속 조사에서 작성한다. 기술별 역할·활용 조건·적용 과정·실패·결과 확인을 조사할 범위로 정했으며, 새 독립 기술 주제를 추가하지 않았다.

## 등록과 보존 계약

- 새 안정 ID 7개를 사용한다. 기존 A2A CLI·평가·RAG·MCP Apps 개별 글을 덮어쓰지 않는다. 향후 본문 보강은 같은 7개 ID의 새 불변 배치와 판으로 등록한다.
- `config/agent_tech_plans.2026-10-13.json`과 같은 이름의 quality 파일을 새 배치 `agent-tech-plans-2026-10-13`으로 연결한다. report-v1에 계획 상태 필드를 추가하지 않고 title/deck/scope/caveats에 단계를 명시한다.
- quality의 custom 프로필은 사용자가 요청한 목차·조사계획 범위다. ready와 audit의 gated 표시는 이 계획판에 대한 형식·범위 검토이며 해당 기술의 상세 리서치나 실습 완료를 뜻하지 않는다.
- 개념·범위 검토와 첫 화면/본문 자체 편집을 별도 기록했다. 작성자가 이미 내용을 알고 있으므로 독립 에이전트나 실제 초보 독자의 시험으로 간주하지 않는다.
- `study_pages.json`의 기존 연결·설정은 보존하고 7개 새 ID의 정확한 내용 해시에 묶인 목차 설정만 추가했다. 각 페이지에는 4장·12개 세부 질문이 있으며 본문/상단 목차 두 위치에서 같은 세부 질문으로 이동한다.

## 검증

- research-check: 계획 7편 통과. research-audit: 24 gated / 30 needs substantive review. 신규 7편은 목차 계획의 제한된 프로필이며 다른 문서의 상태를 바꾸지 않는다.
- 전체 154 테스트, 129.356초 통과. 임시 시험 자료는 codex-temp-lifecycle의 owned scratch 실행기로 정리했다. 기존 ResourceWarning은 제품 등록 실패와 구분한다.
- 로컬 54문서/170판. 기존 47문서·163판·41배치·26품질배치와 모델 816관측/818판·원문14/14의 이전 행은 값·내용·저장 시각까지 그대로다.
- 새 7편의 84세부 질문·168두 위치 링크는 모두 본문의 해당 anchor로 연결된다. 모든 페이지에 조사 계획 단계가 표시된다.
- 실제 in-app browser에서 390/1280px ×7편을 확인했다. 390px에서 document width375, 1280px에서1265로 문서 가로 넘침이 없고 각12세부 목차가 있다. 현재 장/세부 위치, 목차 클릭과 펼침 메뉴16링크를 확인했다.
- Edge CLI의 390px 요청 PNG는 실제 레이아웃 폭과 캡처 폭의 차이로 오른쪽이 잘렸다. 이 이미지를 모바일 통과 근거로 쓰지 않았으며 실제 브라우저 viewport390에서 줄바꿈·첫 화면을 확인했다. 데스크톱 PNG는 시각 확인했다.
- 기존 brief·summary desk·PNG 생성. 주거 review는11Pass/1Fail이며 실패 사유는 기존 자료의 활성 공고0이다. 신규 계획 페이지의 출판·목차 검사와 구분한다.

원문·계획·수집/내용 확인 시각·해시·기존 로컬/공개 baseline·시험과 감사 근거는 ignored `data/raw/agent-usage-2026-10-13/plan-pages/`에 보존한다. 필요한 화면 및 렌더링 근거는 `D:/9_codex_temp/2026-10-13/signal-agent-plans/evidence/`에 보존하며 삭제 가능한 임시 폴더로 표시하지 않는다.

## 공개 반영

기존 GitHub Pages 배포 경로로 공개 반영을 진행한다. 실제 결과와 링크는 완료 후 추가한다. 기존 사용자 작업 파일·기본 GitHub 계정·워크플로·수집기·예약 설정은 보존한다.
