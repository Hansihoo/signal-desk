# 2026-11-11 모델 공개 검토

Theo catalog 18편을 수집했다. 새 원문은 Claude Fable 5.2이며, Gemini 4 Carbon·GPT-6.1 Terra·통합 비교의 3편은 이전판을 보존한 채 갱신했다. 비교표 원본 806건 중 Claude Fable 5.2 제공 정보와 Cursor 평가 6건이 추가됐다. 기존 Fable 소개와 Theo 본문은 별도 주소에서 읽을 수 있다.

- Muse Ember는 11월 9일 공개됐다. Meta 직접 API의 200K 입력 경계, 캐시 적중, Google Cloud Preview와 Max 평가별 강약을 구분했다. [출시](https://research.meta.ai/blog/muse-ember) · [표준 요금](https://dev.meta.ai/docs/pricing-rate-limits)
- Gemini 4 Carbon은 기존 모델의 제공 확대다. 안정 API의 11월 도입 요금과 12월 적용 단가, 동기와 long decode 출력 한도를 별도 기록했다. [제공 확대](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/) · [API 요금](https://ai.google.dev/gemini-api/docs/pricing)
- Gemini Robotics 2.5는 파트너 배포다. 자동차 부품 정리 실증 96%는 Apollo 2, Robotics ER과 행동 모델을 결합한 결과다. Argon의 안전 시험은 별도다. [DeepMind 발표](https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/)
- MiniMax H3 Image PE는 텍스트에서 이미지 설명과 화면비를 만드는 가중치다. 편집 경로는 프롬프트를 공개했다. 동일 조건의 성능 비교와 PE 전용 표준 단가는 미확인이다. [모델 카드](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image-PE)
- Fable 5.2의 CursorBench 4.0 다섯 설정과 Cursor 적용 요금을 평가 비용 및 Anthropic 직접 API와 구분했다. [CursorBench](https://cursor.com/es/cursorbench) · [제공 및 요금](https://prod.cursor.com/docs/models/claude-fable-5-2)

11월 11일 KST에 공식 문서의 관련 부분을 읽고 공개 원문 및 획득 지문을 비추적 자료에 보관했다. Holo4는 9월 기존 출시이며 MNN-Pocket 기술 보고서보다 가중치 공개가 앞선다. 단백질 서열 전용 HyPLM은 일반 언어·문서·개발 모델 비교의 범위 밖으로 분류했다. 실제 추론, 청구, 독립 재현은 미확인이다.

## 로컬 검증

신규 소개 3편과 Carbon 개정판, 공식 관측 29건을 함께 등록했다. 로컬 발행, 품질 게이트, 모델·발행 테스트 37개가 통과했다. Muse Ember 공식 요금 상세에서 200K 초과 조건, 출력 USD 1.50 및 캐시 USD 0.012와 확인일을 확인했다. Pages 공개와 브라우저 검증 결과는 배포가 끝난 뒤 기록한다.

## 공개 완료 — 2026-11-11 05:19 KST

커밋 `955cf58`의 [GitHub Pages 실행](https://github.com/Hansihoo/signal-desk/actions/runs/42893121819)이 성공했다. 제출본 테스트 214개와 클라우드 주거 점검이 통과했다. 로컬 주거 점검은 활성 공고 0건 항목만 실패했다. 로컬 지식 색인에는 소개 4편의 현재판 지문과 근거를 연결했고 Muse Ember 요금 질의를 확인했다.

공개 데이터에서 소개 4편과 공식 관측 29건이 검토 입력과 일치했다. 배포 전 보고서 258판, 모델 관측 2,776판, Theo 원문 23판의 지문을 모두 보존했다. 새 배포에는 보고서 262판, 모델 관측 2,805판, Theo 원문 23판이 있다. Theo 기존 3편의 수집 변화는 연결 자산의 개정이며 본문은 같다.

공개 390px 브라우저에서 새 소개 4편의 비교표 8개, 비교표 링크, Carbon의 제한 제공 1판을 확인했다. [전체 모델 비교표](https://hansihoo.github.io/signal-desk/preview/ai-models.html)에서는 5개 모델을 검색해 Muse Ember의 FrontierCode 27.2%와 장문 요금, Robotics의 96% 실증, MiniMax의 FP4 제공, Carbon의 12월 단가, Fable의 CursorBench 60.0% 및 평가 비용 USD 32.79를 원문 단위·조건·확인일과 함께 확인했다. LFM3-Omni-2B의 1~3차 관측과 [Theo Fable 5.2 원문](https://hansihoo.github.io/signal-desk/preview/model-guides/claude-fable-5-2-model-guide.html)의 검색·정렬을 실제로 확인했다.
