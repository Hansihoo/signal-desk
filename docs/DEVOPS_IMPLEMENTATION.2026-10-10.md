# DevOps 구축 실무 가이드

## 목표와 범위

개발자가 기존 Jenkins/Windows/C++ 검증을 보존하면서 중복 파이프라인, 검사 결과 누락,
재현되지 않는 빌드와 배포 추적 문제를 해결하는 도구·구성을 선택하도록 한다.
사용자 첨부 요구사항의 13개 주제를 다루며 현재 DevOps 문서의 시각적 읽기 스타일을 재사용한다.
기존 개념 시범과 과거 보고서 판은 보존한다. 새 가이드는 기존 연구 메뉴·검색·SQLite 발행에 연결한다.
새 수집기·유료 호출·DevOps 서버 설치나 운영 배포를 실행하는 작업은 아니다.

작업 유형: 공식 기술 조사와 집필, 데이터 카탈로그, 새 보고서 읽기 렌더러와 탐색 기능.
영향: 새 가이드와 앞으로 추가할 보고서의 기본 스타일; 기존 보고서는 기존 렌더링을 유지한다.
위험: CI 실행 권한/자격 증명, 도구의 라이선스와 유료 기능 혼동, 예제와 실행 검증 혼동,
기존 보고서·이력 보존. 실제 프로젝트의 비공개 CI 구성은 제공되지 않았다.
검증: 원문/라이선스 의미 대조, 질문별 답·본문 위치, 첫 화면/본문 별도 자체 검토,
보고서 품질 패키지, 단위·회귀 시험, 기존 자료 보존, 실제 PC/모바일 검색·필터·목차·복귀.

## 독자와 질문·필요 근거

독자는 Git과 자기 프로젝트의 빌드 명령은 알지만 CI 운영·테스트 리포트·배포 추적 설계 경험은
없을 수 있다. 끝에는 한 프로젝트의 현황표, PR/전체 검사 분리 계획, 도구 선택 이유,
AI 에이전트 작업 명세와 승인 조건을 작성할 수 있어야 한다.

| 질문 | 필요한 근거 | 본문 계획 |
| --- | --- | --- |
| 무엇부터 구축하고 무엇을 재사용하나? | DORA/CNCF/SSDF 적용 범위, 기존 CI 기능 | 1–5장 |
| 검사부터 릴리스·장애 분석까지 어떻게 연결하나? | CMake/CTest/GoogleTest/JUnit, 실행기·저장·권한 | 4–8장, 동일 C++ 사례 |
| 도구가 대신 구현하는 기능과 도입 조건은? | 15개 공식 문서·저장소·라이선스, 비용 구조 | 9장 카탈로그 |
| 자주 실패하는 구성은 어떻게 고치나? | CI 옵션/캐시/리포트/보안 문서 | 10장 문제별 사례 |
| 에이전트에게 무엇을 주고 누가 결정하나? | AGENTS.md와 Codex 공식 문서, 작업 명세 | 11–12장 |
| 단계적으로 확장하는 완료 조건은? | 기존 기능 보존과 공식 적용 사례 | 13장 |

공식 문서의 기능 확인과 자체 추천을 구분한다. 가상 C++ 프로젝트와 비교 조건은 편집 예시다.
실제 Jenkins·컴파일러·제품 계정 실행이 없으면 실행한 튜토리얼이나 성능 결과로 표시하지 않는다.

## 원문 확보와 내용 검토

2026-10-10 HTTP72개 시도 중70개 성공, ReportPortal403과 최초 Shared Library 라이선스404는 실패로 보존했다.
ReportPortal 원문의 선택 문단은 웹 도구로 별도 확보했고 실제 Groovy Libraries 플러그인의 MIT 원문으로
라이선스를 보완했다. 별도 보완 웹 탐색에서 OSV scan-source의 끝 슬래시 주소404도 확인했고 공식 메뉴의
끝 슬래시 없는 원문으로 확인했다. 정규화 오류는 저장된 raw에서 고쳤으며 HTTP 확보 시각을 갱신하지 않았다.
최종 보고서에 사용하는69개 자료의 정확한 URL·수집·선택 절 검토 범위는 quality sidecar와
docs/ai/AI_RESEARCH_REVIEW_LOG.md에 남겼다. 처음 확보한 정확 시각은 미확인(null)이다.

대표 사실은 DORA 다섯 지표, CNCF의 단계별 투자·최고 단계 비목표, SSDF 최종1.1/초안1.2,
CTest3.21/JUnit 출력·0건 차단, Jenkins JUnit의 UNSTABLE/빈 결과, trusted Library/JCasC 권한,
Actions 서비스와 runner MIT의 구분, GitLab CE/EE, Grafana AGPL, ReportPortal premium 조건이다.
OSV는 conan.lock·SBOM·C/C++ commit/vendored 지원과 데이터/버전 추정 한계를 확인했고 Crashpad
client/handler·업로드·심볼 분석 범위를 보완했다. 저장소 push는 정식 릴리스·지원 보증으로 쓰지 않았다.
Spotify 2020-03-16 발표는 raw HTML published_time과 대조했다. NIST PDF 전체는 미검토다.

제목/description/deck만 별도로 읽고 이후 질문/근거/본문을 같은 에이전트가 자체 검토했다.
CI 비교표의 공식 기능과 편집 권고 분리, Windows GoogleTest CRT, 절대 결과 경로,
PowerShell native 명령 실패 시 중단과 이전 XML 제거를 수정했다. 정상3개/경계값 실패/0건/XML 누락은
예상 결과이며 CMake/MSVC/Jenkins가 없어 실행하지 않았다. 독립 에이전트·사람 독자 시험은 없다.
research-check1편 통과; audit10 gated/32 legacy는 검토 영수증의 계약이며 독자 승인이 아니다.

## 구현과 앞으로의 기본 형식

report-v1 원고는 config/devops_implementation.2026-10-10.json, 별도 도구 데이터는
config/devops_tools.2026-10-10.json이다. 카탈로그는 보고서 내용 해시에 묶이고 모든 설명이
정본 원고에도 있어야 한다. 이전 판은 현재 카탈로그 해시가 다르면 그 판의 정본 설명으로 읽는다.
새 불변 발행 배치 devops-implementation-2026-10-10과 기존 보고서/SQLite/메뉴 경로를 사용한다.

housing_watch/study_report.py/.css/.js와 config/study_pages.json이 새 읽기 형식을 담당한다.
기존41개 ID는 Editorial로 동결하고 새 ID는 요약→목차→장별 설명→적용 결과→출처 순서로 렌더링한다.
공통 research sidebar/CSS는 보존하고 본문 목차는 상단에 둔다. 장 이동 전 읽기 위치를 저장해 뒤로 돌아오며
실제 이전 페이지도 복원한다. 직접 열 때는 리서치 목록을 제공한다. 도구 검색/분야/등급의 결합 필터,
빈 결과/초기화/선택 비교/필터 간 선택 유지/세부 펼치기를 구현했다. JavaScript 없이 전체 설명을 읽는다.
의존성 추가, 수집기·자동화·유료 호출·DevOps 인프라 변경은 없다.

## 검증과 산출물

최종 로컬42보고서/138판: 이전41보고서·137판, 모델 원본/ledger, 공통 CSS와 수용된 로컬v2 해시 정확 보존.
136개 시험, JS syntax/compileall, 품질 검사, publish/brief/desk/review 통과. 기존 publication 회귀 시험이
요구하는 data 앵커가 새 레이아웃에서 빠져 첫 비교표에 연결해 수정했다. 빈 자료 영역을 추가한 것은 아니다.
모든212 HTML의13086 로컬 참조에 누락이 없었다. 기존 링크 검사 helper의 출력 경로를 그대로 사용해
이전 hackathon 영수증이 갱신된 것을 발견했다. 새 결과는 DevOps 경로로 옮기고 이전211/12409 결과는
그때의 completion.json 기록과 검사 출력 형식에서 복원했다. 이 복원은 원본 바이트 해시 검증으로 주장하지 않는다.

Edge1440/1024/850/768/390/320px의 구조/목차/현재장/정확한 복귀 위치/검색/결합필터/비교/키보드/
메뉴 닫기/코드/넘침9기록, standalone 오프라인3폭 및 별도 정적 review 총4기록을 확인했다.
초기 시험 코드의 잘못된 DOM 셀렉터·검색 query를 빠뜨린 URL 기대값·본문에 없는 단어 조건을 고쳤다.
실제 목차 Escape가 global sidebar handler와 충돌한 제품 동작은 전파를 제한해 수정했다.
PC/모바일 첫 화면·흐름·비교표와 housing brief/desk PNG를 직접 확인했다.

공유용 reports/devops-2026-10-10/devops-implementation-guide.html은 글꼴/CSS/JS 내장,
사이트 이동 링크는 공개 절대주소다. 기존 v2와 이전 시범 파일은 수정하지 않았다.
별도 devops-implementation-guide-review.html은 선택 검토용이며 스크립트 비활성·시스템 글꼴 차이를 표시한다.
도구2MiB 입력 제한으로 내장 웹글꼴만 뺀 파생 입력을 사용했고 실제 결과/파생 해시는 manifest에 남겼다.
검토본의 기능을 실제 검색/필터/목차 검증으로 취급하지 않는다. 스레드 등록 경로는 그대로 보존한다.
공개 배포와 공개 보존 검증은 다음 절에 완료 상태를 기록한다.


## 공개 반영 완료

source b808091 / [Pages38044404452](https://github.com/Hansihoo/signal-desk/actions/runs/38044404452),
2026-10-10T10:17:48Z 시작·10:19:41Z 완료 상태 success. CI136tests, 공개 원문 수집/발행,
housing review와 durable snapshot/Pages 배포가 성공했다. 일반 뉴스 warnings1은 기존 수집 영역의
부분 경고이며 이 가이드69원문 확인이나 배포 실패로 합치지 않는다. 브라우저의 Linux DBus 로그는
review PASS와 함께 남았으며 제품 사용자의 경고로 표시하지 않는다.

공개 보존10항목:42보고서/138판, 새 원고 exact, 이전41보고서/137판, 모델14원문,
기존 발행 상대순서·공통CSS·새 HTML이 로컬 검토본과 일치했다. CSS는 Windows/Linux 줄바꿈을
정규화한 비교이며 로컬 이전 원본 바이트 해시도 별도 보존했다. 실제 공개 Edge6폭9기록의
목차/복귀/검색/결합필터/비교/키보드/no-JS 읽기를 확인했다. 공개 PC/모바일 PNG도 직접 확인했다.

주소: https://hansihoo.github.io/signal-desk/preview/devops-implementation-guide.html
기존 로컬v2와 이전 시범, 공유용 단일 HTML, 정적 검토본, raw/품질/실패/성공 영수증은 등록 경로에
계속 보존한다. 실제 C++·Jenkins 실행과 사람 독자 시험은 이 완료 범위에 포함하지 않는다.
