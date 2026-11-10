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
