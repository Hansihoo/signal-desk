# AI 활용·글쓰기·게임 제작의 독립 리서치 페이지

사용자는 세 분야를 폭넓게 조사하고, 전문가의 실제 사용·관련 스킬·오픈소스·초보자 활용 방법을 포함해 핵심 내용을 먼저 알려 달라고 요청했다. 후속 요청은 기존 리서치 사이트에 각각 페이지를 추가하는 것이다.

목표는 도구 목록을 읽는 데서 끝나지 않고 자기 업무 요청문, 집필 초안, 작은 게임 규칙표를 만들 수 있게 하는 것이다. 작업 유형은 수동 조사·콘텐츠 집필·기존 발행 경로 적용이다. 영향 범위는 새 report-v1 문서 3개와 quality sidecar, 발행 manifest와 운영 문서다. 기존 렌더러·CSS·수집기·예약·유료 생성 설정은 변경하지 않는다. 주요 위험은 연구 조건의 일반화, 공개 코드의 라이선스 혼동, 가상 예제를 실행 결과로 오해하는 것, 원문에 없는 관계를 만들어 내는 것이다.

## 독자 질문과 본문의 답

| 문서 ID | 독자의 질문·산출물 | 본문 위치와 주요 근거 |
| --- | --- | --- |
| practical-ai-workflows | AI에 첫 업무를 어떻게 맡기며 반복 작업에 무엇을 추가할까? 회의 메모의 실행 목록과 확인 질문을 만든다. | first-task/meeting-example: 가상 메모와 미정 값; expert-use: Anthropic 직원 조사·METR; skills-and-tools/open-tools: 공식 스킬·MCP 규격과 저장소·라이선스. |
| ai-assisted-writing | 설명문과 소설에서 사람과 AI가 어떻게 협업할까? 설명 초안 또는 장면 지시서·초안을 수정한다. | reader-question/writing-example: Google·Diátaxis와 가상 별 수집 설명; evidence-writing/expert-writing: STORM·ALCE·MIT·UCL·Ayala; fiction-example: 저자 구성 기대 장면·수정 전후·변형 풀이. |
| ai-game-creation | 내 코딩 경험에 맞는 도구와 스킬로 어디서 시작할까? 30초 별 모으기의 규칙표와 기능별 요청문을 만든다. | production-ai: Ubisoft; choose-engine: 엔진 공식 자료; star-game: 초기 상태→행동→기대 상태; actual-skills/engine-connections: 실제 Game Studio SKILL.md·Unity/Godot 커뮤니티 연결. |

세 글은 각각 핵심 답을 주는 deck·summary를 본문보다 먼저 보여 준다. 주제 경로는 `개발 동향 / AI 활용 / 업무 활용·글쓰기·게임 제작`이다. 기존 34개 문서와 124개 판, 모델 원본 14개, 발행 순서의 기존 부분과 CSS는 보존 대상이다.

## 근거 확보와 품질 검토

앞선 채팅 조사에는 원문 57개가 포함됐다. 이번에는 같은 57개 URL 중 56개 HTTP 원본과 추출문·영수증을 `data/raw/research/2026-10-09-ai-writing-games/`에 보존했다. CoAuthor 사이트 1개는 인증서 확인 실패이며 우회하지 않았다. 최종 세 글의 참고문헌은 서로 다른 55개 원문이다. 미채택 CoAuthor와 HBS 자료의 실패·범위는 원래 검토 기록과 분리해 남긴다.

이전에 수행한 웹 원문 확보의 정확한 최초 시각은 미확인이다. 새 로컬 영수증은 실제 재수집 시각이며 과거 최초 수집을 소급 생성하지 않는다. quality의 `first_collected`는 null로 보존하고 `last_successful_collection`은 이번 영수증의 성공 시각을 사용한다. 원문 게시일·측정 기간은 검토 로그의 기존 조건을 유지한다. 본문·출력 생성은 원문 확인 날짜를 갱신하는 행위가 아니다.

제목·소개·요약만 읽는 별도 검토에서 게임의 스킬 정의 부족을 수정했다. 이후 독립 본문 검토에서는 회의의 근거 없는 의존 관계, Dify·n8n 조건 설명 부족, 소설의 결과 장면·수정 전후 부족, 원문 제목/탐색 문구가 섞인 발췌를 지적했다. 실제 내용과 발췌를 수정한 뒤 같은 최신 입력을 재검토했다. MIT 앵커가 Submit/LangSmith 일부를 잡는 오류는 단어 경계로 수정했다. 검토 입력의 canonical SHA256을 quality package에 연결한다.

짧은 발췌·문자열/지문 검사는 관련 원문 절을 읽은 의미 검토와 구분한다. 독립 에이전트 검토는 실제 한국어 독자 시험이 아니다. 모델·게임·스킬 설치 실행, 한국어 교정 품질과 생산성·제작 시간·수익 측정은 수행하지 않았다. 가상 기대 출력은 저자 설계이며 실제 모델 응답으로 표시하지 않는다.

## 발행과 확인

입력은 `config/ai_practical_guides.2026-10-09.json`, 품질 파일은 같은 이름의 `.quality.json`, 불변 배치는 `ai-practical-guides-2026-10-09`이다. 과거 배치를 편집하지 않는다. 검증 범위는 `research-check`, `research-audit`, 테스트, 로컬 발행·링크·보존 검사, 1280/390/320px 검색·분류·문서 화면, 주거 brief/desk/review와 PNG, 공개 배포 후 데이터·390px 화면 확인이다.

로컬 검증: 세 첫 화면·본문이 수정 후 독립 검토를 통과했고 `research-check` 3편, `research-audit` 5 gated/32 legacy를 확인했다. 테스트 129개 통과, 발행·링크 200 HTML/10,827개 참조/누락0, 기존 자료 보존 8항목, 실제 1280/390/320px 검색·분류·요약/본문/출처·폭 검사 30항목 통과다. 세 첫 화면 PNG와 brief·desk PNG를 직접 확인했다. 앱 브라우저 bridge 연결 실패 후 로컬 headless Edge를 사용했다. 최초 검색 시험은 토큰 검색에서 결과가 반드시 1개라고 잘못 가정해 실패했고, 실제 대상 글이 검색 결과에 포함되는 조건으로 수정했다. 사이트 검색 동작은 바꾸지 않았다.

일반 수집은 AI127개·뉴스64개, SH8개를 가져왔다. GDELT HTTP429 경고1건은 성공한 다른 수집과 구분한다. CoAuthor SSL 실패와 선택 favicon404도 별도다. 주거 search/context/report/render/brief/desk/review는 실행됐고 review는 PASS지만 이 검사는 공고 내용의 현재 유효성·검색 관련성 심사를 대신하지 않는다.

공개 배포: 소스651e300의 [Pages37920945741](https://github.com/Hansihoo/signal-desk/actions/runs/37920945741)가2분18초에 성공했다. 실제 공개 데이터는37편/127판이며 새3편·기존34편/124판·모델14·기존 순서·CSS의8보존 검사와 실제390px 검색·탐색·요약/본문/출처·분류10검사가 통과했다. 공개 PNG도 직접 확인했다. 페이지는 preview/practical-ai-workflows.html, preview/ai-assisted-writing.html, preview/ai-game-creation.html이다. 원본·검증 산출물은 소유 스레드 원장에 기록하며 사용자 정리 요청 전에는 삭제하지 않는다.
