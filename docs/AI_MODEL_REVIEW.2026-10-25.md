# AI 모델 누락 보완 검토 — 2026-10-25

## 발행 범위와 날짜

21일 공개된 Baseten Mammoth-1/Elephant-1과20일 공개된 Voxtral3 네 모델을 소개2편과 전체 비교표70관측으로 함께 보완한다. 오늘 출시된 모델로 알리지 않는다. 같은 가중치의 재게시나 SDK를 새 기반 모델로 추가하지 않았다. 모델별 stable ID와 model_introduction 유형, 기존 Editorial을 사용한다. 가상 업무, 활용 예시, SDK 실습과 응용 문제는 없다.

Theo15문서와793원본관측은 실제 수집에 성공해 변경이 없었다. AI 기존/신규모델 후보 수집682항목의 경고는0이다. 일반 주간 GDELT의SSL 실패는 별도이며 모델 원문 실패로 부르지 않는다. 모든 공급자의 모델을 전수 심층 검토한 것은 아니며 SKY001 등 미완료 후보를 변경 없음으로 분류하지 않는다. 수집 성공을 원문 검토로 바꾸지 않는다.

## 실제 원문 확인

공개 HTTP22응답의 원본 bytes/UTC/hash와 선택 관련절을 data/raw/ai_news/official/2026-10-25의 불변 파일과 receipts-22.json에 보존했다. report-v1에는 새 provenance 필드를 추가하지 않고 품질 sidecar에 실제 범위를 기록했다. 발표21/20일, 현재 확인25일과 평가 데이터 생성22일을 구분한다.

- Baseten 공식21일 블로그, 기술 보고서, 두HF모델 카드와 메타데이터, 공식 제공 목록 및 현재 Jev0.4.1/AA데이터를 읽었다. 출시0.4 71.24/62.65와 현재Full68.44/60.26, 공개75.34/72.24를 분리했다. Full은비공개동일기술60%/신규영역40%이며 공개점수는미포함이다. Jev자료 생성22일20:10:35UTC, RTX PRO6000과 모델별serving을 구분한다. Mammoth의 평가 checkpoint9d1962f 및 serving8f9f8619와 HF현재HEAD61cec44, Elephant현재HEADb3f8a934의 차이를 확인했으며 현재HEAD와 평가판 가중치의 동일성을 자체 검증하지 않았다. 평가운영자 주석의 한 신규영역 시험 제외 및 공식보고서의 오염 없음 주장을 대조하고 미해결로 남겼다. HF현재MIT와 평가표의 오래된proprietary주석, 카드의텍스트/이미지학습과 보고서의텍스트전용 설명도 충돌을 보존했다. 공급자AA재현65.9/65.2와 현재AA운영자Elephant64.69/d1-ultra65.25/SubQ65.00을 섞지 않았다. 무료종료27일23:59PT/28일15:59KST와 이후표준단가미확인, CUDA/VRAM 및 한국어 미시험을 설명했다.
- Voxtral 공식 발표의9개 선언적 차트JSON과 주석, 네 모델카드, 변경이력/수명주기 및 현재USD Standard표를 읽었다. FLEURS45의forced/inferred/WER/CER, cpWER와30분데이터판, FLEURS35의오프라인참고와240/480/960/2400ms를 분리했다. Small의우세와AA재수록Fun/Microsoft및RealtimeGemini대비열세를 함께 썼다. Mini/Realtime의단가인상과TTS인하, 오디오분/입력문자/통합VoiceAgents대화요금을 분리했고캐시/Batch/Priority를기본요금과합치지않았다. TTS발표35언어/프리셋18언어와카드9언어의충돌,일반공개가중치/자체배포계약미확인,Active와PublicPreview의차이를남겼다. 음성재생/복제/모델실행/API과금은 수행하지 않았다.

## 내용과 출력의 검토

동일 작성자의 제목/목적/요약만 포함한 첫 화면 입력과 원문을 포함한 본문 입력을 분리했다. 판단근거, 반대 결과, 정확한단위와설정/판/미확인을 대조했고 기계 quality2편 및70관측 임시메모리검증을 통과했다. 독립에이전트검토/사람독해시험이나 벤치마크재현은 아니다. 가격/출시일을 뉴스요약만으로 채우지 않았다.

로컬 ai-models --input에70관측을 적용했고 두불변manifest와publish에 연결했다. 생성HTML/DB/raw는 제출하지 않는다. local publish/quality/audit와brief출력 성공,390×1500PNG를 실제 확인했다. 주거review의활성0 실패와나머지출력검사 통과를 모델 기능과 분리한다. 두새본문의1판을 새 지식검토 원장에 연결하고 색인을 갱신했다. 독자의 모델 비교/요금 질문2개가 현재본문을 찾았다. 현재공개판/이전판 보존, 원격배포와실제필터/모바일 검증은 완료 후 아래에 추가한다.

## 제출 경계

현재main을 사용하고 매저장소/데이터쓰기와Git쓰기 직전 git signal-gh verify로 정확한ROOT/fetch/실제push/Hansihoo CLI/GCM을 확인한다. 기본theo-s-han/전역credential과읽기전용Theo원본을 바꾸지 않는다. 기존dirty변경은로컬에보존하고HEAD기반선택index에이번배치/필수manifest/문서만더한다. 별도스킬/새branch/clone/worktree나유료API는만들지않는다. 임시시험은소유scratch실행기가정리하며필수근거는 D:/9_codex_temp/2026-10-25/signal-ai-models에보존한다.
