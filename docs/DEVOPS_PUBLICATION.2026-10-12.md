# DevOps r14 공개 배포

사용자는 보강한 DevOps 문서의 공개 배포까지 요청했다. 기존 Signal Desk Pages
배포 절차로4장12세부 목차, CI/CD 비교표1개, 전달/복구 도식2개와 실습 다운로드를 발행한다.

현재 공개 기준은 FDE 배포 a69379d/Pages38211478978의45보고서/152판이다. DevOps는r9이며,
모델804관측/806이력과 원본14/14가 있다. 새r10-r14의5개 불변 배치를 함께 발행해 과거
설명과 수정 이력을 보존한다. r14를 이전 판에 덮어쓰지 않는다.

다른 문서 변경과 기존 FDE 원고/표시/SVG를 보존한다. 일반 index를 건드리지 않는 전용
index에서 HEAD와 DevOps 관련 소스/문서만 구성한다. 생성 DB/raw/HTML/PNG는 커밋하지
않는다. examples/devops-sort의 소스는 포함하되 웹 ZIP은 원고에 보존한 정확한 코드를
렌더할 때 생성한다. 새브랜치/worktree/clone과 workflow/권한/예약을 추가하지 않는다.

작업 디렉터리의 전체152시험166.218s가 통과했다. 실제 제출 tree의 원고 품질 게이트와
발행 결과, Pages의 검사/배포 결론, 공개 본문/다운로드/출처와 기존 이력 보존을 확인한다.
내용 검토 날짜와 원문 획득 날짜는 배포로 갱신하지 않는다. 예제 원격CI/실제 운영 서버와
사람의 학습 시험을 이 사이트 배포 성공과 혼동하지 않는다.

공개 배포와 검증은 완료됐다. 소스 커밋과 실행 URL, 실제 결과는 아래에 기록했다.
증거는 `D:/9_codex_temp/2026-10-12/signal-desk-devops-deploy-r14/evidence/`에 보관한다.

## 2026-10-12 DevOps r14 공개 배포 완료

사용자 요청에 따라 소스 `1d17b18bc0b693d5f447bb34fc214f9680f2e939`를 main에 발행했다.
[Pages 38214660351](https://github.com/Hansihoo/signal-desk/actions/runs/38214660351)은
15:54:40 KST에 success로 완료됐다. 배포 단계는15:54:35, publish job은2분31초였다.
[공개 문서](https://hansihoo.github.io/signal-desk/preview/devops-implementation-guide.html?v=1d17b18)는
r14 원고와 정확히 일치한다.4장12세부 목차, CI/CD 비교표1개와 전달/복구 도식2개가 반영됐다.

- 로컬 전체152시험166.218초, 제출 tree의 품질 게이트/발행/brief/review가 통과했다.
  공개 CI도152시험39.788초와 housing briefing review를 통과했다.
- 공개45문서/157판. 다른44현재 문서와 배포 전152판, 모델804관측/806이력,
  원본14문서/14이력은 정확히 보존됐다. 기존 FDE r2와 SVG/공유 기능을 유지했다.
- Home/현재 문서/ZIP/r1-r13의16개 HTTP 경로와 원고 JSON, 본문 내부 anchor가 정상이다.
  별도로 preview Home의 최근 업데이트와 최신 DevOps 제목도 확인했다.
- 공개 실습 ZIP의9개 파일은 제출 tree에서 생성한 고정 원고 파일과 바이트가 같다.
  ZIP 컨테이너의 생성 OS 정보는 Windows0/Linux3으로 달라 전체 ZIP 해시는 같지 않다.
  파일 내용 보존과 컨테이너 메타데이터를 구분했다.
- 실제 Chrome1864px에서 CI/CD 표와 전달 도식 PNG를 저장해 확인했다. 두 세부 목차 링크와
  복구 도식의3단계/보관 경로를 확인했으며 가로 넘침이 없다. 공개 화면을 크롬에 열었다.
  모바일 레이아웃은 앞선 로컬 DOM 검증 범위이며 공개 모바일 캡처를 추가 수행하지 않았다.
- 사이트 발행 성공이 예제 원격 CI나 실제 운영 서비스 배포, 사람의 학습 시험을 뜻하지 않는다.
  원문 획득/내용 검토 날짜는 이번 발행으로 갱신하지 않았다.

생성 DB/raw/HTML/PNG/ZIP은 커밋하지 않았다. DevOps 관련42개 소스/설정/문서만 제출하고
남아 있던 FDE 작업 파일과 기본 GitHub 계정을 보존했다. workflow/인증 권한/예약을 바꾸지 않았다.
증거는 `D:/9_codex_temp/2026-10-12/signal-desk-devops-deploy-r14/evidence/`에 보관한다.
임시 소스 내보내기와 공개 snapshot 복원은 owned scratch에서 검증 후 제거됐다.
