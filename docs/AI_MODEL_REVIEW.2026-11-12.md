# 2026-11-12 모델 원문과 발행 검토

Theo 카탈로그 원문 18편과 비교표 원본 관측 806건에 변경이 없었다. 공식 신규 사양과 제공 조건이 있는 모델 7편을 새 안정 ID에 작성하고 공식 관측 39건을 같은 발행에 연결했다.

- BotPsy는 기반 Qwen에서 추가 학습한 가중치다. 공통 추론 모드의 BFCL v4 44.0%, Claw-Eval 46.5%의 역전, BF16 결과와 GGUF 파일 크기를 구분했다. [공식 카드](https://huggingface.co/qvac/BotPsy-0.8B)
- ERNIE 5.5 Flash Preview는 11월 5일 Base의 후속 학습 중간판이다. Qianfan 중국 시간대·정가·행사는 원문 CNY/1천 토큰, 국제 요금은 USD/100만 토큰이다. Preview 가중치의 11월 25일 전 공개는 예고다. [발표](https://ernie.baidu.com/release/ernie-5-5-flash-preview/) · [중국 요금](https://cloud.baidu.com/doc/qianfan/s/wmh4sv6ya) · [국제 요금](https://intl.cloud.baidu.com/en/doc/qianfan/s/Jm8r1826a-intl-en)
- MiniMax H3 Image는 전일의 H3 Image PE와 다른 생성·편집 체크포인트다. 33.1B 변환기, 최대 참조 16장, Standard와 Highspeed 토큰 단가, 4K 예시와 할인 한계를 나눴다. [카드](https://huggingface.co/MiniMaxAI/MiniMax-H3-Image) · [요금](https://platform.minimax.io/docs/pricing/overview)
- Alpamayo 2 Edge는 주행 VLA다. 875장면 폐루프의 15.15±0.04 km/과실 사고와 개루프 0.52m, 이전 1.5의 다른 지표·표본과 시간 범위를 구분했다. [공식 카드](https://huggingface.co/nvidia/Alpamayo2-Edge)
- PAN 2는 영상으로 행동 결과를 예측한다. Physics-IQ 순위표와 기본 실행의 다른 추론 경로·원문 단위, MiniMax H3 기본 실행이 더 높은 반대 결과를 반영했다. 대학 보도자료는 웹에서 읽었으나 로컬 수집은 403이어서 품질 패키지는 모델 카드와 공개 저장소·평가 원표를 사용했다. [공식 카드](https://huggingface.co/IFM/PAN2)
- ERNIE Light DT는 1M 문맥·128K 출력과 선택형 추론을 제공한다. Wizshot ME는 인물 영상 1080p·4~15초 및 영상 초당 CNY 0.7이다. 제품 길이와 합성 음성 검증 길이, 정량 품질 비교 미확인을 구분했다. [Baidu 출시 안내](https://cloud.baidu.com/product/qianfan_home/model_3.html?track=home_banner) · [Wizshot 요청 계약](https://cloud.baidu.com/doc/qianfan-api/s/8mwbylac7)

원문 바이트와 획득 시각은 비추적 raw에 보관했다. 작성자 첫 화면·본문 검토를 별도로 기록했다. 독립 모델 재현, 실제 청구 및 사람 독해 시험은 하지 않았다.

## 로컬 검증

품질 게이트 7편과 모델 테스트 32개가 통과했다. 로컬 발행에서 소개 7편과 비교표의 공식 관측 39건이 입력과 일치했고, 각 상세 페이지의 비교표 링크를 확인했다. 로컬 연구 워크플로 21개 중 일부는 기존 미커밋 study_report.py와 학습 템플릿 지문 불일치로 실패했다. 이 미커밋 변경은 제출하지 않는다. 공개 Actions와 공개 브라우저 결과는 배포 후 기록한다.
