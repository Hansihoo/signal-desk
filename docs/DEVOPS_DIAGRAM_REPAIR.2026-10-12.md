# DevOps의 정의와 요약 그림 보강

후속 피드백: 사용자는 공개 r6 첫 장의 두 가상 예시가 왜 나오는지 이해하기 어렵다고 지적했다. 정의와 필요성에 먼저 답하도록 고친 로컬 r8과 실제 검증 범위는 [설명 순서 수정](DEVOPS_EXPLANATION_REPAIR.2026-10-12.md)에 있다. 아래 r6 자체검토와 공개 출력 확인을 독자 승인으로 해석하지 않는다.

DevOps를 공부하는 독자가 협업과 자동화, 운영에서 얻은 피드백의 관계를 설명할 수 있도록, 사용자에게 거부된 r5 요약과 첫 개념 장을 보강했다. 사용자의 후속 배포 요청에 따라 r6을 공개 사이트에 게시했고 Chrome에서 확인했다.

## 요약

DevOps는 소프트웨어를 개발하는 사람과 서비스를 운영하는 사람이 목표와 책임을 공유하고, 반복 작업을 자동화하며 실제 서비스에서 얻은 피드백으로 계속 개선하는 방식이다. 코드, 검사와 배포를 순서대로 실행하는 그림만으로 이 뜻을 충분히 설명할 수 없다.

기존 요약은 자동화를 첫 정의처럼 배치했고, 운영 확인에서 코드 수정으로 돌아가는 연결은 꼬리가 상자에서 떨어져 있었다. 이번에는 공동 계획, 개발과 검사, 배포와 운영, 결과의 다음 개선을 연결하고 각 단계에 여러 역할이 참여하도록 표시했다. 화살표에는 전달하는 내용을 적었다.

| 출발 | 도착 | 전달하는 것 | 새 그림에서 확인한 연결 |
| --- | --- | --- | --- |
| ① 함께 계획 | ② 개발하고 검사 | 합의한 변경 | ① 오른쪽 경계에서 ② 왼쪽 경계로 |
| ② 개발하고 검사 | ③ 배포하고 운영 | 검사한 버전 | ② 아래 경계에서 ③ 위 경계로 |
| ③ 배포하고 운영 | ④ 결과로 개선 | 사용자 의견과 운영 기록 | ③ 왼쪽 경계에서 ④ 오른쪽 경계로 |
| ④ 결과로 개선 | ① 함께 계획 | 다음 계획에 반영할 개선 | ④ 위 경계에서 ① 아래 경계로 |

네 상자는 설명을 단순화한 예다. 보편적인 표준 네 단계나 단계별 전담 부서가 아니다. 검사한 버전의 운영 반영에는 제품과 팀에 맞는 시험 환경 확인과 승인 조건이 필요하며, 그림은 상세 작업을 한 상자에 묶었다. 검사 실패와 복구의 상세 절차는 기존 CI/CD, 구축 및 운영 장에서 읽는다.

## 독자의 질문과 바뀐 설명

독자는 DevOps를 처음 배운다. 가격 정렬 오류 사례에서 공동으로 정할 기준, 자동 검사로 확인할 결과, 운영 문제를 다음 개선에 반영하는 일을 구분하는 것이 과제다. 비교 축은 팀이 함께 일하는 방식과 그 안의 검사 및 배포 절차의 범위다.

| 질문 | 근거와 답 | 원고 위치 |
| --- | --- | --- |
| 개발과 운영은 각각 무엇을 하는가? | 기능 구현과 오류 수정, 실제 실행 환경과 서비스 상태 관리 | 요약 `DevOps의 뜻`, 1장 첫 해설 |
| 협업은 무엇을 바꾸는가? | 공동 목표와 정보, 책임 공유 및 다른 단계에 대한 참여 | 요약 `협업이 바꾸는 것`, 1장 정의와 사례 |
| 자동화한 도구만 설명해서는 왜 부족한가? | 검사 기준과 대응 담당자를 정하고 실제 결과를 함께 사용한다 | 1장 도구의 역할, 2장 첫 문장 |
| 화살표는 무엇을 전달하는가? | 변경, 검사한 버전, 운영 결과, 다음 계획 | 요약 `그림의 화살표`, 새 그림과 대체 텍스트 |

가격 1, 2, 10의 기존 정렬 사례를 유지했다. 초안에서 빈 값 처리 규칙까지 먼저 정했다고 쓴 부분은 후속 운영 사례가 가격 누락을 처음 발견하는 내용과 충돌했다. 처음에는 정렬 기대값과 검사할 입력 및 배포 후 확인 사항을 합의하고, 운영에서 새로 발견한 입력을 다음 테스트로 반영하도록 고쳤다. 기존 5장의 코드와 실행 결과는 그대로다.

## 원문 확인과 날짜

2026-10-12에 [AWS DevOps](https://aws.amazon.com/devops/what-is-devops/), [AWS CI](https://aws.amazon.com/devops/continuous-integration/), [AWS CD](https://aws.amazon.com/devops/continuous-delivery/), [DORA Continuous Delivery](https://dora.dev/capabilities/continuous-delivery/)와 [Microsoft DevOps](https://learn.microsoft.com/en-us/devops/what-is-devops)를 실제 HTTP로 확보했다. 정의와 협업, 역할 참여, CI 및 배포 준비의 관련 절을 읽었다. 이 공식 설명을 성능의 독립 실험으로 사용하지 않는다.

수집 시각, 원본과 텍스트 지문, 확인 범위는 `data/raw/devops-2026-10-12/definition-repair-sources.json`과 품질 패키지에 있다. 기존 최초 수집 미확인 값과 원문 게시일은 오늘로 소급하지 않았다. 처음 웹 도구로 읽은 Microsoft 원문의 정확한 최초 시각도 추정하지 않고 실제 HTTP 성공 시각을 보존했다. 다른 기업 사례, 조사 지표와 실습 자료의 이전 확인일과 미실시 범위는 유지했다.

## 새 판과 검증

- 원고: [devops_implementation.2026-10-12.r6.json](../config/devops_implementation.2026-10-12.r6.json)
- 품질 기록: [devops_implementation.2026-10-12.r6.quality.json](../config/devops_implementation.2026-10-12.r6.quality.json)
- 새 그림: [devops-summary.2026-10-12.r6.png](../housing_watch/assets/editorial/devops-summary.2026-10-12.r6.png)
- 판 연결: [devops_visuals.2026-10-12.r6.json](../config/devops_visuals.2026-10-12.r6.json)

불변 배치 `devops-definition-2026-10-12`는 같은 보고서 ID를 유지한다. r5 이미지 연결을 이전 판 목록에 추가하고 r4 연결도 보존했다. CI/CD와 구축 이미지의 바이트, 3장 이후의 본문, 표와 그래프, 예제 코드는 그대로다. 2장은 첫 연결 문장만 보강했다.

첫 화면 세 필드와 별도 요약의 자체검토, 변경 본문과 원문 대조, 실제 이미지 연결 검사와 출력 확인을 각각 기록했다. 작성자는 이전 판을 이미 읽었으므로 무정보 독해 시험이나 독립 에이전트 검토로 부르지 않는다. 사용자가 거부한 r5의 이전 Pass도 독자 승인으로 사용하지 않았다. 수정된 r6에 대한 사람 독해 확인은 아직 수행하지 않았다.

전체142시험, `research-check` 1편, `research-audit` 12gated/32legacy와 `publish`가 통과했다. 브라우저320/390/768/1024/1440px 및 JavaScript 미사용 읽기6기록에서 새/이전 그림 지문, 이미지 확대와 가로 이동, Escape와 초점 복원, 목차와 Home 검색, 페이지 넘침을 확인했다. 실제 PC와 모바일 PNG를 읽었다. 첫 실행의 숨겨진 모바일 빠른 목차 클릭 시간 초과는 검사 대상을 보이는 본문 목차로 고친 뒤 재검증했고 실패 로그도 보존했다.

다른43편과 이전144판은 저장된 행과 시각까지 동일하다. 새 DevOps 판1개로 현재44편/145판이며 모델804관측/806판, 원본14문서와 이력도 정확히 보존했다. 검증 근거는 기존 작업 폴더 `D:/9_codex_temp/2026-10-12/signal-desk-home/evidence/devops-repair/`에 남겼고 임시 실행 폴더는 정리했다. 위의 초기 로컬 검증에서는 공개 배포를 하지 않았으며, 이후 사용자의 요청으로 아래 배포를 수행했다. 예제의 실제 CI/CD와 사람 독자 시험은 여전히 수행하지 않았다.

## 공개 배포와 Chrome 확인

source `b031c7d4b643b891349c50feb2011d681faa2ea9`를 정상 commit/push했고 [Pages38187510657](https://github.com/Hansihoo/signal-desk/actions/runs/38187510657)이2026-10-12 09:20:56 KST에 성공으로 완료됐다(2분18초). 사이트 CI142시험과 실제 클라우드 주거 review가 통과했다. 주간 뉴스 수집의 경고1건은 배포 성공과 구분하며 전체 출처의 최신 검증 완료로 부르지 않는다.

공개 JSON에서 수정 DevOps 원고가 로컬 입력과 정확히 일치하고 다른43편과 이전144판, 모델804관측/806판, 원본14문서와 이력이 같음을 확인했다. 새/이전 요약 이미지와 공유 CSS도 로컬 출력과 일치한다. Home의 실제 변경6건을 확인했고 [공개 문서](https://hansihoo.github.io/signal-desk/preview/devops-implementation-guide.html?v=b031c7d#summary)를 Chrome에서 열어 새 정의, 그림과 Home 메뉴를 확인했다. 요청한 탭은 유지했다.

배포 결과와 로그, 공개 전후 JSON, 보존 확인 및 실제 Chrome PNG는 위 근거 폴더의 `deployment.json`, `deployment-log.txt`, `public-before.json`, `public-after.json`, `public-preservation.json`, `public-summary-chrome.png`에 보존했다.

## 이미지 제작 프롬프트

내장 `image_gen`으로 r5 요약 그림을 편집했다. 첫 생성물의 계획 항목 사이에 추가된 작은 화살표 두 개는 불필요한 순서를 만들므로 두 번째 편집에서 제거했다. 생성 원본 두 장은 기본 생성 폴더에 보존하고 선택한 결과를 위의 버전이 있는 소스 PNG로 복사했다. 자동 게시에서는 이미지를 생성하지 않는다.

첫 호출의 최종 프롬프트:

```text
Edit target: the provided DevOps summary infographic. Create a thoroughly corrected replacement teaching image, preserving its clean white background, navy text, purple accents and friendly business cartoon illustration style. This is for a beginner Korean DevOps research article. The current image incorrectly makes DevOps look like just a code/test/deploy checklist and has a detached return-arrow tail. Correct both problems. Landscape 1536x1024 with large crisp Korean text; minimal clutter and generous space. Exact title: 'DevOps: 개발과 운영의 협업'. Exact subtitle: '함께 계획하고, 자동화하고, 운영 결과로 개선합니다.' Four rounded panels arranged as a simple clockwise loop, with 1 upper-left, 2 upper-right, 3 lower-right, 4 lower-left. Each panel shows developers and operations staff collaborating, never exclusive job ownership by phase. Panel 1 exact heading '01 함께 계획', short caption '변경 목표와 확인 기준을 함께 정합니다.' and two people discussing a service. Panel 2 heading '02 개발하고 검사', caption '코드와 테스트를 만들고 반복 검사를 자동화합니다.' and a person with a code screen and automated test screen. Panel 3 heading '03 배포하고 운영', caption '검사한 버전을 반영하고 실제 상태를 확인합니다.' with a service screen, server and staff. Panel 4 heading '04 결과로 개선', caption '사용자 의견과 오류를 다음 계획에 반영합니다.' with staff discussing user feedback and error records. Precisely FOUR directional connectors. Edge 1: attached to RIGHT edge of panel 1, pointing RIGHT into LEFT edge of panel 2; label '변경'. Edge 2: attached to BOTTOM edge of panel 2, pointing DOWN into TOP edge of panel 3; label '검사한 버전'. Edge 3: attached to LEFT edge of panel 3, pointing LEFT into RIGHT edge of panel 4; label '운영 결과'. Edge 4: attached to TOP edge of panel 4, pointing UP into BOTTOM edge of panel 1; label '다음 계획'. All arrow shafts start at the actual source-panel border and end at the destination border, with ONE arrowhead only at the destination. No detached tail, crossed connector, arrow inside a speech bubble, decorative arrows or backwards arrow. Reserve empty gutters between panels for arrows and their labels, and do not overlap any text or pictures. Bottom banner exact text '개발과 운영이 목표, 정보, 책임을 공유합니다.' Small footer '과정을 단순화한 설명용 예시입니다.' Make the collaboration, repeatable automation and feedback meaning much clearer than the old image. Do not claim performance metrics or that team merger is required.
```

두 번째 호출의 최종 프롬프트:

```text
Precise single-panel correction to the provided new DevOps infographic. Preserve exactly the four outer panel boxes, all four correctly attached clockwise arrows 01->02->03->04->01 and their labels, all headings, footer/banner, style, characters and text outside panel 01. Inside panel 01's white planning board ONLY, remove the two small blue right-facing arrows between the three colored notes. These three planning concerns are discussed together, not a sequence of steps. Replace that board heading with exact Korean '함께 정할 기준'. Replace the three colored notes' labels respectively with '사용자 문제', '검사 기준', '배포와 복구'. Arrange them as three equally weighted notes with NO connectors, arrows or sequence numbers inside this board. There must now be only the FOUR outer purple arrows in the whole illustration, all still joined to the correct source and destination panel edges. Do not otherwise change the image.
```
