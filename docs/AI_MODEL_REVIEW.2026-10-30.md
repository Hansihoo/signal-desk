# 2026-10-30 AI 모델 검토

질문은 긴 문서 파싱과 녹음 음성 이해의 새 모델이 기존/경쟁 대안보다 어디서 낫거나 부족하고 비용과 제공 조건이 무엇인가다. Unlimited OCR2는27일 공개의 상세 소개 누락 보완이며 Nemotron3.5Transcribe는28일 공식 출시다. 오늘 처음 발견한 자료를30일 신규 출시로 바꾸지 않는다.

## 실제 취득과 원문 검토

Theo model-pages 수집은 신규1(Carbon원본),동일16/실패0. 원문 HTML·공유정렬JS·catalog해시를 누적 보존했다. ai-models는800원본관측 동일/실패0이며 전체 모델/공식 평가의 재검증을 뜻하지 않는다. signal_review는692후보 취득/20경로성공,hn-newest 연결종료1건이며 제목을원문확인으로취급하지않는다.

OCR15쪽PDF의1/5~12쪽 선택절과10/11쪽표1~4전체를pypdf추출및PNG시각독해로확인했다. MP84.59/Marathon77.06와단일페이지Overall94.02<TeleOCR96.91/Ovis96.47,표TEDS89.60<이전90.16을보존한다. 1.77GB는B1의KV캐시이고1315TPS는B16이다. 전체VRAM/최소GPU요구량으로바꾸지않는다. 저자의Marathon100문서/중영언어/whole-document경쟁입력실패의빈예측및평가기시간상한을설명했다. 전역정보보존불가/제목계층한계와작은페이지창손실을남겼다.

Transcribe현재카드의선택사양/언어표/영어9·장문·다국어7·FLEURS한국어/cpWER평가와방법,28일공식글을읽었다. 5.33/4.71영어WER,30B/인코더포함34B,양자화예정/현재공개파일목록의차이를기록했다. FP8/NVFP4메타데이터와7/5safetensors파일은확인했지만다운로드·실행하지않았다. 한국어CER2.78와한국어미포함7언어WER4.62는별개이며QA는영어학습이다. DeepInfra0.00200USD/음성1분을원문단위로보존하고NVIDIA공통요금으로승계하지않는다. 최적화NIM2238음성초/초는공개런타임에없는최적화를포함한다.

IBM29일Switch4.1.1은기반모델불변패치다. 발표10언어와연결ASR현재카드7언어/21일표기가충돌하고동일조건의업데이트판이확인되지않아새기반모델로발행하지않는다. Decision어댑터변경의심층비교는보류했다. AppleAnySpeechRecognizer/AnyDecisionModel은기존모델의라이브러리/이식경로를새기반모델로세지않는다. DeepSeekCyber는LLMGateway설명의제3자abliterated1017변형이며DeepSeek공식29일출시증거로채택하지않았다. 전제공자심층전수검토와SKY후보는완료되지않았다.

HF모델LICENSE404는그대로실패로보존하고공식저장소MIT와카드표기를대조했다. Baidu가격표는PaddleOCR-VL/일반문서파싱으로UnlimitedOCR2가격매핑이없어단가미확인이다. PDF기본python에는pypdf/fitz가없어번들pypdf와Poppler로읽었다. 첫출력cp949문자오류는UTF8출력으로교정했으며취득실패와구분한다.

## 원고와 검증의 현재 상태

새불변보고서2편/quality2패키지와41사실을양manifest에연결했다. 같은작성자가본문을제외한첫화면을별도읽고OCR대화이력을제거했으며본문과원문표를대조하고문장띄어쓰기를수정했다. research-check2편통과,로컬ai-models41신규/publish완료. 지식원장에실제1판source_hash/document_digest를연결하고두질의의본문반환을확인했다. 독립에이전트/사람독해시험,모델실행·한국어실업무·청구·계정시험은없다.

제출소스시험/실제화면/공개배포는아래완료기록에추가한다. 이시점은공개완료가아니며다른dirty작업을제출하지않는다.

## 원문 취득 영수증과 실제 관련절

- `ocr-card`: https://huggingface.co/baidu/Unlimited-OCR-2/raw/main/README.md / UTC `2026-10-29T20:02:20.859948+00:00` / SHA256 `fc4f2f4c3b7382a19fdfc1a02b0ba17382fe493a41408fb44bc2d982279c8e34` / `data/raw/model_maintenance/2026-10-30/ocr-card-fc4f2f4c3b73.raw`. 27일출시/28일학습지원과새SR-SWA,Transformers/SGLang본문·페이지창/메모리·출력제한관련절. 코드실행없음.

- `ocr-pdf`: https://huggingface.co/baidu/Unlimited-OCR-2/resolve/main/Unlimited-OCR-2.pdf / UTC `2026-10-29T20:02:28.629203+00:00` / SHA256 `1eb5885f4ddfa4ec6fbff375092377f30b5d6a5e034ec4936213f125bf2f9444` / `data/raw/model_maintenance/2026-10-30/ocr-pdf-1eb5885f4ddf.pdf`. 15쪽논문1쪽개요,5~9쪽구조/학습/평가방법,10~11쪽표1~4전체와12쪽한계. 표10/11PNG시각대조. 그림수치전수전사아님.

- `ocr-config`: https://huggingface.co/baidu/Unlimited-OCR-2/raw/main/config.json / UTC `2026-10-29T20:02:34.721966+00:00` / SHA256 `607d130a70d5af5a35329aa237acd68651f45504c62cc7ced981066f4e781126` / `data/raw/model_maintenance/2026-10-30/ocr-config-607d130a70d5.raw`. 131072위치범위와희소참조설정;API한도또는실제길이보장으로전환안함.

- `ocr-old`: https://huggingface.co/baidu/Unlimited-OCR/raw/main/README.md / UTC `2026-10-29T20:02:40.610927+00:00` / SHA256 `4f573db255db5262bfe2ea92e459bfc11635a456f210e3a96289bb9605077a55` / `data/raw/model_maintenance/2026-10-30/ocr-old-4f573db255db.raw`. 기존1판공개일/제공·라이선스·입력/실행관련절;새2판과구분.

- `ocr-old-config`: https://huggingface.co/baidu/Unlimited-OCR/raw/main/config.json / UTC `2026-10-29T20:02:46.566639+00:00` / SHA256 `55e6c5179eea054a3fca99e3e41424649d22f574fba4c5f0737ef9c9095526e4` / `data/raw/model_maintenance/2026-10-30/ocr-old-config-55e6c5179eea.raw`. 이전32768위치범위와현재설정차이관련필드.

- `marathon`: https://huggingface.co/datasets/baidu/MarathonDocBench/raw/main/README.md / UTC `2026-10-29T20:02:52.529772+00:00` / SHA256 `9a17518e0b952bc6143c406fa388363e8c868cb3990bb80967baa9b8ac5a8326` / `data/raw/model_maintenance/2026-10-30/marathon-9a17518e0b95.raw`. 100문서/중영언어/약18k쪽,MPDocBench-Parse교체평가기/시간상한,whole-document경쟁실패빈예측/분모유지·지표변환관련절.

- `ocr-license`: https://huggingface.co/baidu/Unlimited-OCR-2/raw/main/LICENSE — 취득실패 `HTTP Error 404: Not Found`. 변경없음으로분류하지않음.

- `ocr-price`: https://cloud.baidu.com/doc/OCR/s/fmr1p39gb / UTC `2026-10-29T20:03:00.600625+00:00` / SHA256 `3011bf14c9737618f159219f9b819fb42a93efbea341e31f667a3bbaeafb00bf` / `data/raw/model_maintenance/2026-10-30/ocr-price-3011bf14c973.raw`. 공식Unlimited-OCR API안내와기존경로관련절;2판동일상품가격확인불가.

- `switch`: https://huggingface.co/blog/ibm-granite/granite-switch-4-1-1 / UTC `2026-10-29T20:03:06.574901+00:00` / SHA256 `ac77e00b4c8c31a3a663262d4bb52f280b2abba5ac761fc4f99a6b8aead78e91` / `data/raw/model_maintenance/2026-10-30/switch-ac77e00b4c8c.raw`. 발견/범위판정만;본문전수검토아님.

- `apple-ports`: https://huggingface.co/blog/anydecisionmodel / UTC `2026-10-29T20:03:13.112513+00:00` / SHA256 `d0abcc9a3b872f0409aee4c511b53bf827f846924609f6daea9a56c63354f72e` / `data/raw/model_maintenance/2026-10-30/apple-ports-d0abcc9a3b87.raw`. 발견/범위판정만;본문전수검토아님.

- `nvidia-candidate`: https://news.hada.io/topic?id=36196 / UTC `2026-10-29T20:03:22.175288+00:00` / SHA256 `10502aa8c7132baab0deed503f4588a4fc2fa6d965a214155c28fbb95773d887` / `data/raw/model_maintenance/2026-10-30/nvidia-candidate-10502aa8c713.raw`. 발견/범위판정만;본문전수검토아님.

- `deepseek-updates`: https://api-docs.deepseek.com/updates/ / UTC `2026-10-29T20:03:29.228656+00:00` / SHA256 `9abda5ba89b86be5d82ad045864dbe5047e0908b45c161d8a4631d4d5fcb6f18` / `data/raw/model_maintenance/2026-10-30/deepseek-updates-9abda5ba89b8.raw`. 발견/범위판정만;본문전수검토아님.

- `transcribe-card`: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B/raw/main/README.md / UTC `2026-10-29T20:04:09.543384+00:00` / SHA256 `62f799b5a4c82b3bae74b4b0bfb4919a93d69483b6691f73682a786b8da65ab1` / `data/raw/model_maintenance/2026-10-30/transcribe-card-62f799b5a4c8.raw`. 발표일28일,전체요약/언어표/입출력/하드웨어/라이선스/평가환경/영어9·장문·7언어·FLEURS한국어·cpWER표와NIM조건. 모든개별평가프롬프트전수독해아님.

- `transcribe-blog`: https://huggingface.co/blog/nvidia/nemotron-transcribe-granary / UTC `2026-10-29T20:04:17.290819+00:00` / SHA256 `09d3c07e3e8d2998cac8998e38b2cc564685768dbd8d9361b52ec09c52c237f2` / `data/raw/model_maintenance/2026-10-30/transcribe-blog-09d3c07e3e8d.raw`. 28일공식본문의전사40/번역31/화자13/1h8화자·영어QA,발표5.33/30B와양자화예정,AA/외부평가조건. 의료실험세부전수검토아님.

- `transcribe-config`: https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B/raw/main/config.json / UTC `2026-10-29T20:04:25.362479+00:00` / SHA256 `671882895b3711f93b2e88149e11271f4591680e2756976a43a2967992c946c7` / `data/raw/model_maintenance/2026-10-30/transcribe-config-671882895b37.raw`. 발견/범위판정만;본문전수검토아님.

- `switch-asr`: https://huggingface.co/ibm-granite/granite-speech-5.0-470m-turboctc/raw/main/README.md / UTC `2026-10-29T20:04:31.306341+00:00` / SHA256 `5a7f12bfee3bb82051df616fe55bae0fd987b43a6106c91c8ce0c006b9c07f62` / `data/raw/model_maintenance/2026-10-30/switch-asr-5a7f12bfee3b.raw`. 현재카드7언어/470M/21일출시/5.51vs5.78/Apache2.0·작동조건. Switch29일글10언어와충돌해새변경확정안함.

- `switch-core`: https://huggingface.co/ibm-granite/granitelib-core-r1.0/raw/main/README.md / UTC `2026-10-29T20:04:37.302067+00:00` / SHA256 `97186a9a4877d9bfc8547895a0cff92a726bb867c76480bb547e041f7848d2ae` / `data/raw/model_maintenance/2026-10-30/switch-core-97186a9a4877.raw`. 발견/범위판정만;본문전수검토아님.

- `switch-base`: https://huggingface.co/ibm-granite/granite-switch-4.1-30b/raw/main/README.md / UTC `2026-10-29T20:04:43.293919+00:00` / SHA256 `c82180973946365494b72be5448640f23fe32b5797405fbfd7342d3161f6fbe9` / `data/raw/model_maintenance/2026-10-30/switch-base-c82180973946.raw`. 발견/범위판정만;본문전수검토아님.

- `ocr-git-license`: https://raw.githubusercontent.com/baidu/Unlimited-OCR/main/LICENSE / UTC `2026-10-29T20:05:10.533736+00:00` / SHA256 `d985048c6d69429d685fdbe7557340aa0897c0fd8dc038299b148b9c75dc3383` / `data/raw/model_maintenance/2026-10-30/ocr-git-license-d985048c6d69.raw`. MIT저작권/재배포고지/무보증전문. HF별도LICENSE404와구분.

- `transcribe-previous`: https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3/raw/main/README.md / UTC `2026-10-29T20:05:16.583428+00:00` / SHA256 `7a4306a43f395e3a716e77f1d81c03db18a0a355d7b566bb1d6307213ba0302b` / `data/raw/model_maintenance/2026-10-30/transcribe-previous-7a4306a43f39.raw`. 기존Parakeet0.6B/25유럽언어/라이선스와24분full·3hlocal attention조건. 직접직전판으로지칭안함.

- `transcribe-price`: https://deepinfra.com/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B / UTC `2026-10-29T20:06:42.538492+00:00` / SHA256 `648306c2e09734893781bb777befe0d80604d154aa647642f7386d07dd2bba2e` / `data/raw/model_maintenance/2026-10-30/transcribe-price-648306c2e097.raw`. DeepInfra공개페이지분당0.00200USD/현재spec·서비스계층설명. 실제계정/청구미검증.

- `ocr-api-price`: https://cloud.baidu.com/doc/OCR/s/rmvt5uvkv / UTC `2026-10-29T20:06:48.501498+00:00` / SHA256 `418277df0d53d43067c0db9f81c36f6696e20a6e9edb67de721bda35b3e8b8bd` / `data/raw/model_maintenance/2026-10-30/ocr-api-price-418277df0d53.raw`. 29일갱신PaddleOCR-VL/일반문서파싱가격표본문. UnlimitedOCR2전용매핑없어다른단가승계안함.

- `openmdw`: https://openmdw.ai/license/1-1/ / UTC `2026-10-29T20:06:54.660225+00:00` / SHA256 `09e0806ccede5afe048168f777e239a40d6e5a20ac9fa87680d8dfa0371ffd1f` / `data/raw/model_maintenance/2026-10-30/openmdw-09e0806ccede.raw`. OpenMDW1.1허용·배포고지·소송종료·무보증및이용자권리확인책임전문;법률자격판단아님.

- `transcribe-fp8`: https://huggingface.co/api/models/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B-FP8 / UTC `2026-10-29T20:07:00.633846+00:00` / SHA256 `fb5f8a5e6b1d4ae028743cd31050c479736f389bb542e04dcb01611f4f1012cd` / `data/raw/model_maintenance/2026-10-30/transcribe-fp8-fb5f8a5e6b1d.raw`. 공식공개모델id/gated=false/7개safetensors파일목록·갱신시각. 다운로드/실행검증아님.

- `transcribe-nvfp4`: https://huggingface.co/api/models/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B-NVFP4 / UTC `2026-10-29T20:07:06.434984+00:00` / SHA256 `d0738f1ac35fb5d31f94fc2f802cd85dfbad2b77e86dc8d0edd1037101aa5b8d` / `data/raw/model_maintenance/2026-10-30/transcribe-nvfp4-d0738f1ac35f.raw`. 공식공개모델id/gated=false/5개safetensors파일목록·갱신시각. 다운로드/실행검증아님.


## 제출 소스 검증 — 공개 배포 전

다른 작업을 제외한 Git index의 10개 경로만 기존 main 소스와 함께 일회성 폴더에 내보냈다. 새 clone/worktree/branch는 만들지 않았다. 공개 상태 `state-20261029T021413Z-40805022112-1.tar.gz`의 DB와 archive를 복원한 뒤 214개 테스트가 179.944초에 통과했다. Python 3.15의 기존 미종료 DB ResourceWarning은 남아 있으며 오류를 숨기지 않았다. 모델 원본 수집, 비교표 원본 수집, publish, brief, review가 통과했다. 주거 brief는 복원 상태의 출력 확인이며 최신 주거 공고 원문 검토가 아니다. 기본 이미지 실행 대신 정확히 같은 brief HTML을 별도 Edge로 렌더링하고 390×1500 PNG를 실제 읽었다. 이전 이미지 실행 지연의 근본 원인 수정으로 보고하지 않는다.

실제 Edge 1280/390px에서 두 소개의 제목·5개 표·전체 비교표 링크·모바일 overflow, Baidu 필터와 OmniDocBench v1.6 Table TEDS 89.60의 상세 출처·확인일, NVIDIA 필터와 DeepInfra 0.002 USD/음성 분 단위 상세·실제 선택 열을 확인했다. LFM3의 이전 판 표시, Theo Carbon 원본의 3개 표·검색·정렬과 sandbox, 기존 작성 Carbon 소개도 확인했다. PC/모바일 소개, 분당 요금 표, 주거 brief PNG를 시각 대조했다. 단일 신규 모델 레코드에 과거 판 표시가 있다는 잘못된 검사 가정을 제거했고, 실제 이력이 있는 LFM3 검사로 검증했다. 모바일 스크린샷은 resize 후 scroll 위치를 초기화했다. 제품 코드를 바꾼 것은 아니다.

처음 검증 실행은 index 준비가 끝나기 전에 시작해 검증 전에 취소했다. 취소를 통과로 세지 않는다. 재실행의 테스트/수집/발행/화면 결과는 `D:/9_codex_temp/2026-10-30/signal-models/selected-check.log`와 `local-browser.json`에 보존한다. 검증 폴더는 마지막 소비자 종료 후 scratch 실행기가 정리한다. 필요 근거인 이 외부 QA 폴더와 data/raw 원문은 유지한다.

로컬 research-audit의 이번 두 소개는 gated_agent_review이며 사람/독립 실행 검토가 아니다. 전체 기존 문서의 미검토 상태를 이 작업으로 승격하지 않았다. 공개 배포·공개 payload/이력/화면 검증은 아직 완료 전이다.
