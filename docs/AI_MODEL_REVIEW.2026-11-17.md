# 2026-11-17 모델 소개와 누적 비교표 검토

기존 main과 Editorial을 사용한다. 새 Hy4 Flash·LongCat-Video-Avatar 1.6 소개와 기존 Qwen4 프리뷰 소개의 후속 정식판, 해당 공식 비교 관측 및 운영 근거만 제출한다. 다른 작업의 미제출 렌더러·작성 카탈로그·문서 변경은 제출하지 않는다.

## 원문과 변경 판정

- Qwen4-Max: [Alibaba 공식 발표](https://www.alibabacloud.com/blog/alibaba-unveils-qwen4-max-new-ai-teammate-for-work-creativity-and-discovery_603783)의 11월16일 정식 ID `qwen4-max`, 2400B/71B, API·앱 제공과 [현행 사양](https://docs.qwencloud.com/developer-guides/getting-started/latest-model), [지역별 요금](https://docs.qwencloud.com/developer-guides/getting-started/model-prices)을 대조했다. 기존 `qwen4-max-preview-model-guide`의 2판으로 보존하며 단순 이름 변경의 중복 페이지를 만들지 않는다. API ID·종량제 제공·표준 단가의 변화는 별도 관측으로 추가한다. Work360 52.69/47.74와 공식 발표가 인용한 Code Arena WebDev의 설정별 결과를 읽고 Fable·Opus·Carbon·Astra보다 낮은 결과도 설명했다. 자체 산업 시험과 외부 평가의 공급자 인용, 현재 Arena 원장의 독립 조회를 구분한다.
- Hy4 Flash: [Tencent 11월16일 발표](https://www.tencent.com/tencent-launches-hy4-flash-to-power-high-speed-cost-efficient-ai-deployment-for-everyday-workflows/), [모델 목록](https://cloud.tencent.com/document/product/1823/130051), [요금](https://cloud.tencent.com/document/product/1823/130055)과 세 평가 그림을 읽었다. 총224B에 Engram64B가 포함되며 활성12B다. 원문의 1M/960k/64k를 임의 이진·십진 정수로 바꾸지 않았다. WorkIndex 42.1은 Preview39.7보다 높지만 Hy4 51.4보다 낮다. 내부85명·259과제의 만족도2.79는 Haiku2.81에 가깝고 DeepSeek3.09보다 낮다. CNY 표준0.5/2/0.02, 발표의 근사 USD0.070/0.281/0.003, 한시 반값과 앱 무료를 분리했다. 반값 종료는11월30일12:00 Beijing/13:00KST다. [Vercel](https://vercel.com/changelog/hy4-flash-now-available-on-ai-gateway-for-50-off)의 별도 11월29일 종료와 같은 시각으로 추정하지 않았다. 가중치는 공개 예정이다.
- LongCat-Video-Avatar 1.6: [공식 README](https://github.com/meituan-longcat/LongCat-Video)의11월15일 출시, [1.6 카드](https://huggingface.co/meituan-longcat/LongCat-Video-Avatar-1.6)와 이전1.5, 공개 파일 목록과 MIT 조건을 읽었다. HF 생성일11월13일을 출시일로 바꾸지 않았다. 텍스트 LLM LongCat2.5와 다른 영상 계열이다. [기술 보고서](https://github.com/meituan-longcat/LongCat-Video/blob/main/assets/LongCat-Video-Avatar-1.6-Tech-Report.pdf)의 관련 절 및 9·12쪽 그림을 시각 대조했다. 508입력쌍·33,051개 유효 표·15비교쌍의 분모와 무승부 보정, API 실패 제외를 보존한다. 1.6은1068.1 Elo로2위이며 OmniHuman2.0의1236.7보다 낮다. 애니메이션 평균2.246→2.114의 퇴보와0.5배속 엄격 검토에서82.5%인 립싱크 문제율도 본문과 표에 남겼다. 공개 가중치에 관리형 API 무료나 최소 VRAM 보장을 붙이지 않았다.

Theo 본문18편과 비교 원본806관측은 이번 수집에서 변경이 없었다. 기존 AI 검색 후보와 공식 경로를 함께 살폈으며 이미 소개한 MiniMax 이미지 모델과 기존 모델의 기능 재소개는 새 모델로 만들지 않았다. 모든 제공자의 모든 출시를 전수 검토했다고 주장하지 않는다.

## 획득과 검토의 범위

비추적 `data/raw/model_maintenance/2026-11-17/`에 성공·실패 획득, SHA-256, 공식 이미지, PDF와 관련 절 추출을 보존했다. Qwen의 직접 HTTP는 시간 초과했고 웹 도구가 반환한 공식 본문 관련 절을 별도로 보존했다. 완전한 원본 HTML 수집 성공으로 기록하지 않는다. Hy 연구 랜딩의 JS 껍데기는 본문 검토로 세지 않고 공식 발표·문서·그림을 대조했다. 일반 뉴스 수집기의3MB 한도를 넘는 PDF는 별도의32MB 상한 PDF 열람으로 확보했다.

원문 의미와 숫자·조건을 대조하고, 제목·목적·요약만 분리한 첫 화면 및 실제 본문을 같은 작성자가 자체 검토했다. 기존 발행 recipe의 모델 소개·Editorial 조합을 사용했다. 독립 추론, 전체 가중치 로딩, 실청구, 한국어 문서 실험과 사람 독해 시험은 수행하지 않았다.

소개3판과 공식 관측55건을 새 불변 입력과 두 publication manifest에 함께 연결했다. 사양은 수치 필드의 단위를 지키고 평가값은 `평가 점수`와 원문 단위, 요금은 USD/CNY별 원문 단가로 저장한다. 지식 원장의 기존 항목을 보존한 새 판과 색인을 만들고 세 독자 질문에서 새 본문 검색을 확인했다.

## 검증과 공개 상태

제출 소스의 시험·화면 검사 및 GitHub Pages·실제 공개 URL 검증은 아래에 실제 결과로 기록한다. 수집·로컬 입력 적용만으로 배포 완료를 선언하지 않는다.


## 제출 소스와 로컬 검증

- 제출 index의 기능 입력과 기존 발행 코드를 Git 메타데이터 없는 소유 임시 복사본에서 검증했다. 전체214시험, 소개3편 품질 검사, publish와 품질 audit가 통과했다. 기존 보고서139편, 보고서289판, 모델2828관측·2969판 및 Theo18편·23판의 로컬 내용 보존도 확인했다. Qwen 소개는1판을 남긴2판이다.
- 390/1280px 소개3편의12표·페이지 폭·전체 비교표 실제 이동과 Qwen 프리뷰1판 링크가 통과했다. 공식 보기에서55관측의 원본 입력 일치, 평가 셀 숫자, 원문 단위·출처·날짜·평가판·조건·최초 저장을 확인했다. USD/CNY 단가와 과제 비용의 실제 셀28개를 대조했다. 사양의224B와2400B·1,000,000, 제공자 필터도 확인했다. 첫 화면·표 상세 PNG를 열어 읽었다.
- 첫 브라우저 검사의 경쟁 모델 검색은 기존 관측이 많아 첫 페이지에서 대상 행을 찾지 못했다. 현재 원본 데이터에는 해당 관측이 있었고, 모델 이름만으로 모든 판이 한 페이지에 나올 것이라는 검사 가정이 원인이었다. 공식 자료·모델·평가판으로 범위를 좁히는 실제 검색으로 검사를 고친 뒤55건이 통과했다. 제품 코드나 기록을 우회·삭제하지 않았다.
- 주거 review는11항목 통과/활성 공고0의1항목 실패다. 생성 brief PNG를 확인했으며 이 기존 주거 자료 제한을 모델 기능 실패와 분리한다. 독립 모델 실행·실청구·사람 독해 시험은 하지 않았다.

## 공개 배포와 최종 검증 완료

- 기능 소스 `718fa92ba8e3a59b7d42c756952e7b9b346fdf3a`를 기존 main에 정상 push했고 [Pages 43950829935](https://github.com/Hansihoo/signal-desk/actions/runs/43950829935)가 성공했다. 2026-11-17 05:40 KST 실제 공개 `research-data.json`에서 소개3판·공식55관측의 입력 일치, 다른 현재 보고서137편과 이전 보고서285판·모델2962판·Theo원문23판의 내용 보존을 확인했다.
- 공개 소개3편의 PC1280/모바일390 화면과12표, 전체 비교표 실제 이동, Qwen 프리뷰1판, 내부 링크/anchor504개를 확인했다. 공개 공식 보기55관측의 평가 수치·원문 단위·평가판·조건·출처·확인일·최초 이력과 실제 단가/과제비용28셀, 제공자·모델·사양 필터가 통과했고 브라우저 오류는 없었다.
- 공개390px 첫 화면3편 및 요금·평가 상세 PNG를 열어 읽었다. Hy4 Flash CNY 반값의 입력0.25/출력1/캐시읽기0.01(100만 토큰당), 종료11월30일13:00KST와 LongCat 애니메이션2.114의 반대 결과가 실제 상세에 표시됐다. Qwen의 지역별 표준가·이전 판과 LongCat의 가중치/운영비 구분도 보존됐다.
- 공개 확인은 배포물과 입력·출력의 대조다. 독립 모델 실행, 실청구, 한국어 업무 및 사람 독해 시험은 수행하지 않았다. 원문·공개 응답·화면 근거는 비추적 raw에 보존하며 일회성 소유 소스 복사본은 정리했다. 이 기록만 담은 후속 문서 커밋은 배포된 기능 소스를 바꾸지 않는다.

공개 소개: [Qwen4-Max 정식판](https://hansihoo.github.io/signal-desk/preview/qwen4-max-preview-model-guide.html), [Hy4 Flash](https://hansihoo.github.io/signal-desk/preview/tencent-hy4-flash-model-guide.html), [LongCat-Video-Avatar 1.6](https://hansihoo.github.io/signal-desk/preview/longcat-video-avatar-1-6-model-guide.html). [전체 모델 비교표](https://hansihoo.github.io/signal-desk/preview/ai-models.html)도 같은 작업에서 공개 반영됐다.
