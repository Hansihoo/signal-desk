# FDE 공개 배포 기록 — 2026-10-12

사용자가 완성된 FDE 학습·공유 자료의 공개 배포까지 요청했다. 보고서 내용·원문 확인일은 유지하고 기존 Signal Desk Pages 경로에 추가한다.

## 배포 범위

안정 ID `fde-enterprise-adoption`, 불변 원고 r1/r2와 quality, 네 핵심 장·문서 기능 표·다섯 원본 SVG 도식을 발행한다. 생성된 DB·raw·HTML·PNG는 커밋하지 않는다. 기존 PNG 도식은 호환되고 FDE는 SVG 원본을 읽는다. 독자 본문의 편집 분류 숨김은 FDE의 정확한 내용 해시에만 연결된다.

동시 DevOps 수정 r10 이후, 새 계층 목차·튜토리얼·공통 CSS/JS 변경은 이 배포에 포함하지 않는다. 일반 index를 건드리지 않는 전용 index에 기존 HEAD와 필요한 FDE 변경만 구성해 실제 제출할 tree를 검증한다. 새 브랜치·clone·worktree는 만들지 않는다.

## 검증과 상태

배포 전 공개 기준은44보고서/150판, DevOps r9, 모델804관측/806이력이다. 기준 JSON을 D:/9_codex_temp/2026-10-12/fde-deploy/evidence/public-before.json에 보존했다. 소스·동시 작업 혼입과 기존 이력 손실이 주요 위험이다. 제출 tree의 전체 시험·발행·SVG 출력, Pages 실행 결과, 공개 본문·원본/모델 보존과 실제 브라우저를 각각 확인한다.

현재 상태: 배포 준비. 실제 실행 URL·완료·검증 결과는 배포 후 보강한다. 생성/배포를 새 원문 검토로 표시하지 않는다. 자료는 단일 작성 에이전트의 내용 자체 검토이며 인간 독자 학습 시험·고객 시스템 실행·효과 측정은 수행하지 않았다.


## 공개 배포 완료

소스 `a69379db8a00f8096f51cc3fb6833582818a6eac`의 [Pages 실행38211478978](https://github.com/Hansihoo/signal-desk/actions/runs/38211478978)이 2026-10-12 06:13:20–06:15:40 UTC(15:13:20–15:15:40 KST)에 성공했다. 전체 시험·상태 복원·수집/발행·주택 검사·백업·업로드·Pages 배포가 모두 성공이다. 소스에 포함된 변경만 검사한 로컬146시험과 발행 연결 후 영향18시험도 통과했다.

[현재 FDE 보고서](https://hansihoo.github.io/signal-desk/preview/fde-enterprise-adoption.html), [공유용 단일 HTML](https://hansihoo.github.io/signal-desk/preview/fde-study-share.html), 이전 r1·Home·연구 JSON의5주소가200이다. 보고서 r2가 입력과 정확히 일치하며 원본 SVG5개가 정상 표시된다. 공유용 파일은 일반 publish에서 자동 생성되고 현재 페이지에 저장 링크가 있다. 글꼴·CSS·JS·SVG가 내장된다.

현재 공개45보고서/152판. 이전44현재 원고·150이력과 모델804관측/806이력, 원본14문서/14이력이 그대로 보존됐다. DevOps 공개판은r9로 유지했고 미배포 수정은 포함하지 않았다. 새 collector·예약·유료 생성은 추가하지 않았다. 렌더링과 배포는 원문의 새 확인이나 인간 독자의 학습 검증이 아니다.

실제 인앱 브라우저에서 공개 제목/4장/5SVG·390px 가로 넘침 없음·키보드 목차·이미지 확대1536px·닫기/초점 복귀를 확인했다. 공유 페이지는 외부 stylesheet/script0·이미지 로드·요약 복귀 계약·콘솔 오류0을 확인했다. 다운로드 클릭 뒤 자동화 도구의 download 이벤트 대기는30초에 시간초과됐으므로 실제 파일 저장의 UI 확인을 통과로 기록하지 않는다. 파일 HTTP 응답과 전체 본문 및 내장 자산, 공유 페이지 실행은 별도로 확인했다.

초기 제출본 분리 때 참고자료 블록이 동시 DevOps의 result_tag/result_end를 잘못 참조해146시험 중18오류가 발생했다. 커밋 전 검증이 잡았고, 기존 HEAD를 기준으로 필요한 FDE 표현만 구성해 변수 의존성을 제거했다. 수정 후 전체 시험이 통과했다. 다른 작업의 source/CSS/JS와 기본 index는 보존했고 별도 index로 제출했다.

검증 증거는 `D:/9_codex_temp/2026-10-12/fde-deploy/evidence/`의 public-verification.json, local-preservation.json, selected.diff, 시험/배포 로그와 공개 화면이다. 검증용 소스 export·복원 DB·다운로드한 백업·별도 index는 마지막 소비가 끝난 뒤 소유 scratch 관리기로 정리한다. 원본 Git/공개 백업/요청한 공유 파일과 필수 검증 증거는 삭제하지 않는다.
