# 2026-10-31 Mistral Large 4 공개판 검토

목표는 29일 개선 가중치와 이전 API 미리보기·Large 3 및 경쟁 모델의 강약점, 현재 표준 비용과 배포/라이선스를 비교하는 것이다. 작업은 기존 소개의 내용 보완이며 새 모델 ID나 UI 재설계가 아니다. 영향은 기존 report ID의 새 4판과 60개 검토 사실의 같은 작업 반영이다. 위험은 서로 다른 지수/Harness·양자화·미리보기 상태·상업 사용 예외를 섞는 것이며 원문 조건을 본문과 표에 보존했다. 검증은 품질·선택 제출 소스 테스트·publish/brief/review·실제 PC/390px 및 공개 수치/단위/출처/날짜/이전 판·보존 검사다.

## 실제 취득과 내용 검토

Theo model-pages는 17개 수집 성공/신규0·변경0, ai-models는800원본 관측 동일이다. 이 범위의 수집 결과이며 모든 모델의 공식 사실 재검증이 아니다. signal_review는685후보 취득/20경로 성공,hn-newest TLS EOF 실패1을 보존했다. 신규 제목/검색/목록 취득은 본문 검토 성공으로 세지 않는다. Mistral 공식뉴스의29일 최신모델글과 현재API변경이력,선택후보를 대조했다. 그 밖의 모든 공급자·미독후보·SKY의 전수 심층검토는 미수행이다.

29일 발표의9개 chart-spec JSON 원값을 읽고 카드의 Coding/Intelligence와 NVFP4 평가3PNG를 시각 대조했다. 코딩48/GLM49, Cyber50.9/DS57, Finch73.3/Kimi77.33, Browse84.5/Kimi91.2, Opus쌍대선호22를 함께 남겼다. Terminal 본문41/차트41.4를 구분한다. 원문개별Harness·표본/오차 미공개와 AA판차이를 설명하며 과거49.8→48을 모델퇴보로 계산하지 않는다. 비공개FrontierCode2.0은현재AA v1.1과별개다.

현재카드 약1T/활성49B와임베딩출력포함52B,API문서1.05T/52B/vision1.6B를 병기했다. 설정위치1048576과1M사양, vLLM특정구성의1M미검증/262144상한을 분리했다. NVFP4가 겨냥하는Blackwell과 FP8대비일부평가하락,DSpark의특정조건가속을유지한다. 법률검토가아니며MaaS·계열사·상업목적과내부/공식제품·내장/중계예외를원문전문으로확인했다. 공개가중치와 API PublicPreview유지를구분하고GA/최소자원/최대출력/종료일을추정하지않았다.

현재동일Mistral Standard 요금표의ML4 .70/.07/2.10,GLM1.40/.14/4.40,DS .30/.007/1.20USD/100만토큰을읽었다. API출시할인/원개발사직접가격/Batch/Priority/지역·계약·실청구와합치지않는다. 이전할인관측은삭제하지않고당시조건으로유지했다. 기존공식사양1관측은같은ID의새판으로갱신하고59관측은비교/조건별로추가했다.

같은작성자가본문없는first-screen.json을별도읽고본문·원문을대조했다. 초기작성의잘못된references/caveats필드와짧은선택발췌는발행전품질검사에서검출해고쳤고잘못된모델파일명전제도실제consolidated목록으로수정했다. 원문취득실패와구분하며제품코드변경은없다. 연구스킬/authoring조합과현재4판의실제본문지문을연결했고지식색인·독자질의반환을확인했다. 독립에이전트/사람독해,모델실행·한국어회사문서·청구·계정시험은없다.

## 원문 취득과 실제 독해 범위

- `announcement` https://mistral.ai/news/mistral-large-4-oss/ / UTC `2026-10-30T20:00:45.450652+00:00` / SHA256 `ea75b881b18df328eef8dfc9432c8ea0cce9d99b17983244ca91acb8d3af5f54` / `data/raw/model_maintenance/2026-10-31/announcement-ea75b881b18d.raw`. 29일 metadata 발표일/개선 가중치·추론3모드와9개 차트 JSON을 실제 읽음. 코딩·Cyber·금융·검색·선호의 상대 열세와 제한 보안 변형, 현재 단가·MaaS 설명. 데모 실행·영상 전체 검증 없음.

- `card` https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/raw/main/README.md / UTC `2026-10-30T20:00:51.011476+00:00` / SHA256 `bd99fb7896a8e8e59f811be20716df569ceff7de4115d9757ede28bf6d17d314` / `data/raw/model_maintenance/2026-10-31/card-bd99fb7896a8.raw`. 전체/활성 집계, 언어/입출력/문맥/추론·기능·라이선스·런타임·DSpark 관련절. 설치 코드 읽기만 했으며 실행 없음.

- `license` https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/raw/main/LICENSE / UTC `2026-10-30T20:00:56.381744+00:00` / SHA256 `d242ebedb53ffd7e26c220e3305665ca47e4e5267fa62ff4cdeb3953b8353c78` / `data/raw/model_maintenance/2026-10-31/license-d242ebedb53f.raw`. 전문: 고지·본인 및 계열사 MaaS·상업목적·의미 있는 제어의 정의·내장 및 중계 제외·내부/공식제품 예외·무보증. 법률 자격 확정 아님.

- `config` https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/raw/main/config.json / UTC `2026-10-30T20:01:01.688394+00:00` / SHA256 `3081fb94f5001f34a21e08437df710bb0b6423beada9184b566a8f5b1ee46277` / `data/raw/model_maintenance/2026-10-31/config-3081fb94f500.raw`. FP8양자화및예외층,max_position_embeddings1048576,전문가128/4,DSpark관련설정.설정값을실제서비스보장으로전환안함.

- `metadata` https://huggingface.co/api/models/mistralai/Mistral-Large-4-1T-A52B / UTC `2026-10-30T20:01:07.100001+00:00` / SHA256 `ac6c62725511d77868f3e7362433eddf60f37cb501bddd6453e0162ad695d5c9` / `data/raw/model_maintenance/2026-10-31/metadata-ac6c62725511.raw`. gated상태·실제safetensors파일목록·revision확인.다운로드·실행아님.

- `docs` https://docs.mistral.ai/models/mistral-large-4 / UTC `2026-10-30T20:01:16.351130+00:00` / SHA256 `90f783f968eddb7a057bf2307e6b27cf579686da9d79db9aa4bc05f0d05ac7f8` / `data/raw/model_maintenance/2026-10-31/docs-90f783f968ed.raw`. 현재 Public Preview/1.05T·52B/시각1.6B/1M/현재 API 단가와 기능 관련절. GA로 승격하지 않음.

- `pricing` https://docs.mistral.ai/deployment/laplateforme/pricing / UTC `2026-10-30T20:01:23.138541+00:00` / SHA256 `599f30a7eb78121b5ae836efb473cc52aa5c9857a33404457c4c4dc9d7a32e5c` / `data/raw/model_maintenance/2026-10-31/pricing-599f30a7eb78.raw`. 발견/범위확인;전문심층검토아님.

- `lifecycle` https://docs.mistral.ai/deployment/laplateforme/models — 취득실패 `HTTP Error 404: Not Found`. 현재URL은다른성공원문으로보완했으며실패를삭제하지않음.

- `initial` https://mistral.ai/news/mistral-large-4/ / UTC `2026-10-30T20:01:29.652880+00:00` / SHA256 `3bc91eebea3558c5d216d99dcfd4ec2b05f6c7abdcb39b93f5acf50ad455a5ff` / `data/raw/model_maintenance/2026-10-31/initial-3bc91eebea35.raw`. 6일 API 미리보기, 가중치 월말 계획, 초기 Coding 49.8과 Terminal28.3 및 평가 구성. 그때의 제공을 현재 공개 완료와 구분.

- `mistral3` https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512/raw/main/README.md / UTC `2026-10-30T20:01:35.146172+00:00` / SHA256 `8f8882191b7bc0e2a348b2f85b35180bc213f4c15da17e8028c8b5cb7a25cb5a` / `data/raw/model_maintenance/2026-10-31/mistral3-8f8882191b7b.raw`. 기존Large3 전체675B/활성41B·멀티모달/256k·공개정밀도·Apache2.0 관련절.현재 API가격/수명 재검증 아님.

- `deepseek` https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/raw/main/README.md / UTC `2026-10-30T20:01:40.607321+00:00` / SHA256 `b72b796e4f4c739eca5d0ad360a7679b39118ca7eb64891f7151a527b292c42a` / `data/raw/model_maintenance/2026-10-31/deepseek-b72b796e4f4c.raw`. Flash1017 카드 전체 소개/비교표와 Terminal42.3·ClaudeCode Harness/컨텍스트/표준권장/라이선스 표기. 자체 평가와 Mistral AA차트31의 조건 차이.

- `glm` https://huggingface.co/zai-org/GLM-5.3/raw/main/README.md / UTC `2026-10-30T20:01:45.909043+00:00` / SHA256 `ed1c0a4563c437a32f8953d637a1db9bd831de1b24bd3062a5ace9e04340b1cf` / `data/raw/model_maintenance/2026-10-31/glm-ed1c0a4563c4.raw`. GLM5.3 카드 소개·같은base의posttraining, 추론기본max·평가Harness 관련절.전체개별과제의재현 없음; 카드other라이선스와 호스트MIT표기를승계하지않음.

- `pricing-doc` https://docs.mistral.ai/inference/pricing / UTC `2026-10-30T20:02:32.082937+00:00` / SHA256 `17d95b707f118329d1a345752af125521c85c62f534dff96b64f95d806c08b59` / `data/raw/model_maintenance/2026-10-31/pricing-doc-17d95b707f11.raw`. Standard/USD 기본 표의ML4, GLM5.3, DS Flash1017 입력/캐시/출력, 표 원단위. Batch/Priority/지역·실청구 미검증.

- `lifecycle-doc` https://docs.mistral.ai/inference/model-lifecycle / UTC `2026-10-30T20:02:38.094892+00:00` / SHA256 `afd3f9de3ee5b18a37c4a7e3de6e3eb3b3da3557c282eb027822bbcb7fa11c7a` / `data/raw/model_maintenance/2026-10-31/lifecycle-doc-afd3f9de3ee5.raw`. Public Preview의 silent update/GA 미보장, 별칭과 고정판, 단계별 종료 정책. 모델의 개별 종료일 확인 없음.

- `nvfp4` https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B-NVFP4/raw/main/README.md / UTC `2026-10-30T20:02:43.587040+00:00` / SHA256 `25f7c255ebe5f63931061886bdce29d524e0ab505ac13500fd01e2e644c615d8` / `data/raw/model_maintenance/2026-10-31/nvfp4-25f7c255ebe5.raw`. FP8와 비교하는 NVFP4 카드·혼합 정밀도·Blackwell 대상·평가 그림과 원문 동일성 주장 관련절.

- `coding-image` https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/resolve/main/images/coding_index.png / UTC `2026-10-30T20:02:49.312308+00:00` / SHA256 `4e35ead45798b59d5722da1190ff1b5a08950b8b9ebc274eb4723efc81a2bf0e` / `data/raw/model_maintenance/2026-10-31/coding-image-4e35ead45798.raw`. 현재카드공식PNG시각독해.48/20/26/41/46/49.주차트JSON과상호대조.

- `intelligence-image` https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B/resolve/main/images/intelligence_index.png / UTC `2026-10-30T20:02:54.729028+00:00` / SHA256 `83e2b7d5191e6e01c3d2c64c143c191887340381b5a13bcad7f54f8495595982` / `data/raw/model_maintenance/2026-10-31/intelligence-image-83e2b7d5191e.raw`. 원PNG 시각독해. ML4 26/Beam18/DS Pro0813 23/Muse25/MiMo30/GLM32/DS Flash1017 32. 현재 카드 스냅샷, 실시간AA조회값 아님.

- `glm-doc` https://docs.mistral.ai/models/zai-glm-5-3 / UTC `2026-10-30T20:03:00.965762+00:00` / SHA256 `a5f54ce1edef236a96e9ea81087f40497347b6f949fc4b53638d799c636fd738` / `data/raw/model_maintenance/2026-10-31/glm-doc-a5f54ce1edef.raw`. 제3자Mistral 호스팅·GA·text/1M·max출력128k·현재가격. 원개발사별도가격/라이선스판정아님.

- `deepseek-doc` https://docs.mistral.ai/models/deepseek-v4-1-flash-1017 — 취득실패 `HTTP Error 404: Not Found`. 현재URL은다른성공원문으로보완했으며실패를삭제하지않음.

- `changelog` https://docs.mistral.ai/resources/changelogs / UTC `2026-10-30T20:03:07.789710+00:00` / SHA256 `f2fc873c4f4583b3e1eae88ce2d336e26fe79251c9c64a027e8a34f83ad514d6` / `data/raw/model_maintenance/2026-10-31/changelog-f2fc873c4f45.raw`. 6일PublicPreview와2주50%출시할인/weightscomingsoon,그밖의22일Flash호스팅·20일Voxtral·28SepGLMGA관련절.29일새가중치는別발표로검증.

- `news` https://mistral.ai/news/ / UTC `2026-10-30T20:03:13.506405+00:00` / SHA256 `0f0b79c4fd8ed794476fec8c9338b4381f86ca0801a951b2f00129be38c72e74` / `data/raw/model_maintenance/2026-10-31/news-0f0b79c4fd8e.raw`. 발견/범위확인;전문심층검토아님.

- `aa-method` https://artificialanalysis.ai/methodology/coding-agents-benchmarking / UTC `2026-10-30T20:03:43.312465+00:00` / SHA256 `193d6295326507eb04e7b83f4ebc5e1e671094e75459f409fbd86032eec04000` / `data/raw/model_maintenance/2026-10-31/aa-method-193d62953265.raw`. 현재 v2.0 구성/표본·반복·에러처리/효율·agent설정·v1.5에서의 변경 절.발표48을현재v2.0측정값으로확정안함.

- `aa-board` https://artificialanalysis.ai/agents/coding-agents / UTC `2026-10-30T20:03:48.900890+00:00` / SHA256 `7bc7a086a99c53ad7b17a58062c9850db059600c0efca93e70d08ce15e3ffd79` / `data/raw/model_maintenance/2026-10-31/aa-board-7bc7a086a99c.raw`. 발견/범위확인;전문심층검토아님.

- `vllm-recipe` https://recipes.vllm.ai/mistralai/Mistral-Large-4-1T-A52B / UTC `2026-10-30T20:03:57.499098+00:00` / SHA256 `a83f2d6c43520d183b314272aa048bfc34d80008a3a714924570358ec919aaa7` / `data/raw/model_maintenance/2026-10-31/vllm-recipe-a83f2d6c4352.raw`. 모델개요와해당런타임의배포예·장비별검증/Limitations/GB300 DCP의1M미검증·262144상한을실제읽음.전체표전사/실행없음.

- `nvfp4-evaluation` https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B-NVFP4/resolve/3d843073c9987de83d1f94a73a3184da8cf0dba2/images/fp8-vs-nvfp4-evaluations.png / UTC `2026-10-30T20:04:04.107406+00:00` / SHA256 `96832fb022f15e27e748d00e875c41d194c305bcc2f5a20e8c99cd55537ae42e` / `data/raw/model_maintenance/2026-10-31/nvfp4-evaluation-96832fb022f1.raw`. 고정revision평가그림을시각독해. GDP19.2/17.4,Terminal34.9/32.8,Cyber82.6/80.9,DeepSWE62.7/64.6와오차막대·하단출력토큰을확인.미공개표본/Harness보존.

## 검증과 발행 상태

research-check 1편 통과, 로컬 ai-models는59신규/1갱신, publish와4판 지식연결완료. 공개 배포와 선택 제출 소스 검증은 진행중이며 완료로 기록하지 않는다. codex-temp-lifecycle의별도scratch를마지막소비자까지유지하고필요한원문/화면근거는밖에보존한다.


## 제출 소스 검증 완료 — 공개 전

Git index의 관련10경로만기존main과함께내보내검사했다. 새clone/worktree/branch는없다. 공개state-20261030T022735Z-40991719928-1.tar.gz의DB와archive복원후214시험(145.550초)이통과했다. 선택소스의품질검사·Theo원문17개/비교800수집·publish·brief/review와실제Edge1280/390px검사를통과했다. 주거brief는복원상태의출력검사이며신규주거공고원문검토가아니다. 기본이미지경로대신같은HTML을Edge로렌더링했고390x1500PNG를시각확인했다. 기존image경로지연의원인수정으로세지않는다. ResourceWarning은기존미종료DB경고로따로남긴다.

소개5표/내부anchor/정확한전체표링크/3판역사페이지와모바일넘침없음,공식필터에서현재단가 .7/.07/2.1 USD/100만토큰·Cyber50.9·31일확인일·공식출처,기존사양1차→2차의원문값/09일→31일을확인했다. 이전Transcribe소개도확인했다. 실제PNG를직접읽었으며픽셀재현이나독자실험으로확대하지않는다. audit의이번소개는gated_agent_review이고저자자체검토이며기존29문서를승격하지않았다.

첫선택소스실행은PowerShell의inline prefix인수가파일명으로전달돼export전에실패했다. 경로를변수로전달하도록검증runner만수정하고재실행했다. 작업화면검사의‘이전’문구가정도실제‘변경기록’과1/2차·양날짜/실제DB역사로교정했다. 검증입력/검사수정이며제품코드를변경하지않았다. 원문/본문품질오류의수정과도별개다. 실패로그를보존했다.

필요한원문/QA JSON·PNG는data/raw와D:/9_codex_temp/2026-10-31/signal-models에보존한다. 사용한선택소스scratch는마지막소비자종료후공통runner가회수한다. 공개완료는Pages와실제공개URL검증후별도기록한다.


## 추가 후보의 중복 판별과 확인 한계

공식 모델 출시 기록을 넓게 재검색하면서 30일 GPT-6 Rosalind Research를 추가로 발견했다. OpenAI Docs 경로로 공식 자료를 찾고 실제 시스템 카드의소개·§2 학습·배포통제관련절을읽었다. §2는GPT-6 Astra와같은가중치이며이번출시에데이터추가/추가post-training을하지않았다고명시한다. 전문연구용접근·거절경계·배포통제가다른출시소식과새기반모델은구분한다. 사용자중복페이지금지원칙에따라이이름을새가중치모델로집계하거나Astra의중복소개페이지로만들지않았다. 전문배포서비스의상세능력·가격/접근변화는이모델소개발행의완료범위에포함하지않으며아침소식검토후보로남긴다. 제품이변경없다는뜻이아니다.

공식 시스템 카드 https://deploymentsafety.openai.com/gpt-rosalind-6 / UTC `2026-10-30T20:20:53.311259+00:00` / SHA256 `6c594486173304c96f456d802fc736156ce1eb0dc8094612cb129229aa38f0d3` / `data/raw/model_maintenance/2026-10-31/rosalind-system-6c5944861733.raw`. 원문제공일2026-10-30. 직접모델문서URL은404,Help출시노트직접HTTP는403이며웹원문에서출시기록을읽은범위와구분한다. 추가API사양이나실계정접근/요금을추정하지않았다.

복원주거brief PNG는과거마감표시가남은캐시를사용한다. active1/출력reviewPass를현재신청가능공고의증거로세지않는다. 이번작업은모델의내용/배포검증이며주거원문재조사나그기존상태판정수정은수행하지않았다.
