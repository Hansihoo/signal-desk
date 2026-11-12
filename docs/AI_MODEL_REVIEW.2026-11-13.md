# 2026-11-13 모델 원문·소개·누적표 검토

목표는 신규 모델·의미 있는 제공 변경을 기존 Editorial 소개와 전체 비교표에 함께 보존하는 것이다. 코드·일정·기존 배치는 바꾸지 않는 콘텐츠 작업이다. 위험은 모델·별칭 중복, 원문 지표/요금 단위 혼합과 공개 배포 누락이며, 불변 입력·원문 해시·영향 테스트·실제 공개 브라우저로 대조한다.

Theo 모델 본문 18편과 비교표 원본 806관측은 이번 수집에서 변경이 없었다. 수집 결과를 공식 사실 검증으로 간주하지 않았다. 기존 소개 ID·판과 대조해 아래 5편을 작성했다.

- [Gemini 4 Hydrogen](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/) — 11월 12일 발표. stable ID, 입출력 통합1,048,576토큰·기본65,536출력, 암시적 캐시만 지원하는 계약을 확인했다. Google 표의 터미널·OSWorld·과학 역전과 이전 Flash 할인 기간을 포함했다. 모델 카드·API·요금 관련 절을 읽었으며 방법론 링크 획득에서는 해당 내용이 확인되지 않아 세부 harness 동등성은 미확인이다.
- [Gemini Decision 1](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/) — 11월 11일 발표. 공유 입력과 질문 합계262,144토큰·출력0·질문1,000개 및 Standard USD0.10/100만 입력을 대조했다. 평가 이미지를 직접 열어 Jev에 뒤지는 정확도·평가 총비용과 낮을수록 좋은 ECE를 기록했다. 전일 일일 소식의 별도 재알림이 아닌 소개·비교표 추가다.
- [Qwen4-Max-Preview](https://docs.qwencloud.com/developer-guides/getting-started/latest-model) — 11월 11일 제공 시작. qwen4.0-max-preview는 같은 모델 별칭이다. 종료 KST11월26일01:00, 추론·답변 공유 출력393,216토큰, Singapore Token Plan·Individual의 대화형 전용 조건, 정가와 한정 Credits 할인을 분리했다. 비교 가능한 정량 성능은 미확인으로 남겼다.
- [AlphaGenome 2](https://deepmind.google/blog/alphagenome-2-deciphering-how-cells-read-dna-to-better-understand-disease/) — 11월 11일 발표. 공식 논문1~5쪽에서 90% precision/accuracy의 recall과 AUPRC/AUC, AG1·Borzoi·Scooby 비교를 읽었다. DNA길이는 토큰이 아니며 PRO-cap·quantile_score 제거와 이전 모델 유지 용도를 반영했다. 비상업 무료·상업private preview이며 임상 검증이나 상업 정가 확인은 아니다.
- [Praxis-1](https://runway.com/news/company-news/praxis-1-is-now-available) — 9월 소개한 모델의 11월11일 가중치·코드 공개다. 보고서의 DROID/RT-1 적응판·RoboLab120×10회, RT-1 서랍 과제 역전과 기본 README의80GB GPU 요구를 대조했다. Apache2.0과 운영비·실험 비용 가정·호스팅 정가는 구분했다.

원문 바이트·획득 시각·SHA256과 실제 읽은 범위를 비추적 raw 및 품질 부록에 보존했다. 작성자 첫 화면·본문 자체검토를 분리했으며 독립 모델 실행·실제 청구·생물학 재현·사람 독해 시험은 하지 않았다.

## 로컬 검증

소개5편의 quality gate와 모델·자료·연구 발행·공개 사이트 영향45시험이 통과했다. 소개5편의 본문표11개·비교표 링크·지식 색인의 현재1판과 usable_with_limits를 대조했다. Qwen 종료·백엔드 제한 질의가 해당 본문을 반환한다. 전체 audit의 과거 미검토 글은 이번 승인으로 승격하지 않는다.

누적표에는 공식32관측을 추가했다. 이어 적용한 관측4개는 통합표의 context·접근 경로·캐시 가격을 연결하는 별도 불변 보완이며 최초 배치를 고치지 않았다. 전체판을 보존하고 같은 관측의2판으로 남긴다.

## 공개 검증

발행 소스를 main에 제출한 뒤 Actions와 실제 공개 상세·누적표·필터·단위·출처·확인일·이전 판·390px 화면을 검증해 후속 기록한다. 공개 반영을 확인하기 전 완료로 취급하지 않는다.
