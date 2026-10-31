# 2026-11-01 Mage-VL-Cowork 신규 모델 검토

현재 상태: 신규소개1판/전체표40관측과실제공개검증완료. [성공한 Pages41238839569](https://github.com/Hansihoo/signal-desk/actions/runs/41238839569). 아래공개전표현은당시기록이며현재결과는끝의공개완료절을따른다.

목표는 새 컴퓨터 사용 모델의 이전 Mage-VL 대비 변화와 경쟁 평가의 강약점·제공/표준비용을 비교하는 것이다. 작업 유형은 신규 모델 소개와 검토 사실의 동시 추가이며 UI 변경은 없다. 영향은 새 report ID의1판 및 전체표40개 관측이다. 위험은 최종RL/이전SFT·설정문맥/실제운용·자체호스팅/관리형API·데이터생성비/요금을 섞는 데 있다. 검증 계획은 원문/별도 첫화면·본문 검토, 품질검사, 정확한 제출소스 테스트/publish/brief/review, PC/390px·공개 값/단위/출처·날짜·이전 이력 보존이다.

## 발견과 실제 검토 범위

Theo model-pages17개와 ai-models800원본관측은 수집 성공/신규0·변경0이다. ai-models 수집 DB실행은성공했으나stdout의안내문때문에후속ConvertFrom-Json만실패했다. 이를원문수집실패나추가신규로기록하지않는다. signal_review는21연결경로553항목을수집했고실패0이다.목록·검색은발견경로이며본문검토가아니다.공식Microsoft공개체크포인트로추적하고기존report/지식검색에소개가없음을확인했다.현재모든공급자/후보전문을전수검토했다고보고하지않는다.

HuggingFace저장소생성은30Oct12:13UTC,보고서는October2026이다.별도일자발표를추정하지않고확인일1NovKST와구분했다. Mage-VL중간판에GUI·코드/터미널·통합SFT와RL을추가한별도체크포인트다.기반의영상/스트리밍이나Microsoft365제품기능출시로승계하지않는다.4B표기와공개텐서4741793792,실제32768문맥과config262144를병기했다.

PDF30쪽중1/9/12~18/23쪽관련절을읽고14쪽표2·3및17쪽표4·5를PNG로시각대조했다. OSWorld361(GoogleDrive제외)/50단계·두실행65.33/66.75평균66.04→66.0,GPTmini같은361한실행을보존했다. GPTmini69.6·Office68.0과Scale68.7/Office70.6/전문89.5,웹Fara68.0>앞선MageSFT58.6을반대근거로넣었다. 최종RL웹점수는미보고다. Static643과live웹을합치지않고호출/추론토큰을시간·청구액으로바꾸지않았다. 본문+10.16pp와정확66.04계산+10.20pp의표시정밀도차이를보존했다.

OpenAI의정확GPT5.4-mini공식문서와현재Standard표의입력.75/캐시.075/출력4.50USD/100만토큰을대조했다. HTTP가격표의숫자는동적 표용 내장 props에있어일반본문파서에는없었다.공식문서와HTML의행원값을확인해고정영수증과해시를보존한다. Mage의표준API가격미확인·Apache2.0와자체GPU/VM·권한환경을분리하고논문의과제당.906→.158데이터생성비(일회성작성/디버깅제외)를서비스요금으로전환하지않았다.

초기초안의research_type을report-v1에직접넣은필드오류와8자미만원문anchor는품질검사에서검출되어배치생성전에수정했다.유형은불변request/recipe의model_introduction에보존한다.공식mini표기와가격동적props에맞춰실제anchor를고쳤다.잘못추정한Mage-VL-4B경로401은발견실패로보존하고실제Mage-VL카드로보완했다.독립배포실패나제품코드수정으로세지않는다. PDF텍스트출력은cp949문자를UTF8로교정했고원문취득과별개다.

별도first-screen.json의제목/설명/도입만읽고GUI코드통합·데스크톱열세·SFT웹/운영차이를설명할수있는지검토한후본문/원문표를재대조했다.같은작성자의자가검토이며독립에이전트/사람시험이아니다. 가상업무/SDK/실습/응용문제는넣지않았다.실제본문지문1판에검토원장·로컬지식색인을연결하고두독자질의반환을확인했다.연구스킬과hash-bound authoring조합을보존했다.

## 원문 취득 영수증과 실제 독해 범위

- `license` https://huggingface.co/microsoft/Mage-VL-Cowork/raw/main/LICENSE / UTC `2026-10-31T20:00:19.852587+00:00` / SHA256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30` / `data/raw/model_maintenance/2026-11-01/license-cfc7749b96f6.raw`. Apache2.0 전문의 허여·재배포4항/고지·변경표시·상표/무보증을 읽음. 개별사업 법률승인 아님.

- `config` https://huggingface.co/microsoft/Mage-VL-Cowork/raw/main/config.json / UTC `2026-10-31T20:00:19.857127+00:00` / SHA256 `b1af304453ea5af1a296aa012ab85402e2e811b693aebfb6a2bbaa8bdd908ee5` / `data/raw/model_maintenance/2026-11-01/config-b1af304453ea.raw`. llava_onevision2·Qwen3 계열, max_position_embeddings262144와정밀도/사용자정의코드 확인. 실제32K 운용과구분.

- `metadata` https://huggingface.co/api/models/microsoft/Mage-VL-Cowork / UTC `2026-10-31T20:00:19.859695+00:00` / SHA256 `1447974a27900fb2b3fa39fa8dc759b38e8adbc93c553fce8acf5b5167bb6483` / `data/raw/model_maintenance/2026-11-01/metadata-1447974a2790.raw`. 공개/비게이트 상태, 생성UTC/수정UTC/revision 및 BF16 텐서 총계 확인. 생성 시각을 별도 정식 발표일로 바꾸지 않음.

- `card` https://huggingface.co/microsoft/Mage-VL-Cowork/raw/main/README.md / UTC `2026-10-31T20:00:19.879254+00:00` / SHA256 `40ba50f7cdea886de5f5bddd0de2aae25d9fa2dff7a5e930f8ea49518968851e` / `data/raw/model_maintenance/2026-11-01/card-40ba50f7cdea.raw`. 모델 개요·별도 5단계 학습·입출력/32K 문맥·메모리·데스크톱/웹/학습 단계 표·고정 런타임·주의 조건을 실제 읽음. 66.04와 반올림 66.0/증분 불일치 및 SFT 58.6을 구분. 실행 없음.

- `base-card` https://huggingface.co/microsoft/Mage-VL-4B/raw/main/README.md — HTTP Error 401: Unauthorized / UTC `2026-10-31T20:00:19.857162+00:00`. 미확인경로실패,실제공식base카드로보완.

- `family` https://microsoft.github.io/Mage/ / UTC `2026-10-31T20:00:20.174065+00:00` / SHA256 `62e2458c6f536796b2f55dd336b3927b4156121dd02f103a372e18df5b4bf383` / `data/raw/model_maintenance/2026-11-01/family-62e2458c6f53.raw`. 발견·보조범위확인;별도전문심층검토아님.

- `project` https://microsoft.github.io/Mage/cowork/ / UTC `2026-10-31T20:02:14.421879+00:00` / SHA256 `ab3c077e06f63d683132aea758ba6840ca238f2acf6993474e3c578ece9861e9` / `data/raw/model_maintenance/2026-11-01/project-ab3c077e06f6.raw`. 공식 프로젝트 본문/평가표·모델/논문/코드 연결 확인. 두 데모 속도는 전체 성능으로 일반화하지 않고 소개에서 제외.

- `paper` https://raw.githubusercontent.com/microsoft/Mage/main/assets/mage_vl_cowork_tech_report.pdf / UTC `2026-10-31T20:02:14.509133+00:00` / SHA256 `b826e9dc82035f52bf2ed0dc9dc68a2031d6b3d050caa297348f6e9b347021e4` / `data/raw/model_maintenance/2026-11-01/paper-b826e9dc8203.raw`. 30쪽 기술 보고서의 1·9·12~18·23쪽 관련절 독해, 14쪽 표2/3과17쪽 표4/5를 PNG로 시각 대조. Google Drive 제외361·반복횟수/Static643·SFT판/데이터 생성비와 제외비용. 전체30쪽의 독립 검증 아님.

- `qwen` https://huggingface.co/Qwen/Qwen3.6-27B/raw/main/README.md / UTC `2026-10-31T20:02:14.526573+00:00` / SHA256 `bb936d6da51014f1edc9aa4cf9abf28d98695b7616ad56adfeeebfa752051d3d` / `data/raw/model_maintenance/2026-11-01/qwen-bb936d6da510.raw`. Qwen3.6-27B 공식 카드의27B·시각입출력·262144 및1010000확장/Apache2.0 관련절. 그 문맥이 Mage 비교 실행에 쓰였는지 미확인.

- `base` https://huggingface.co/microsoft/Mage-VL/raw/main/README.md / UTC `2026-10-31T20:02:14.534286+00:00` / SHA256 `e84630ce6e4d4f636dc280b28065357c22aa1a373d29e7404a8a5dcfbbd81f45` / `data/raw/model_maintenance/2026-11-01/base-e84630ce6e4d.raw`. Mage-VL 기반의 이미지·영상·codec-native streaming 및 4B/Apache2.0 관련절. Cowork에 영상 기능·동일 과제 기준값을 승계하지 않음.

- `fara` https://huggingface.co/microsoft/Fara1.5-4B/raw/main/README.md / UTC `2026-10-31T20:02:14.633174+00:00` / SHA256 `817286a8d5f1fc05dc2ea36655dfa20b8a747aa39c57fa84c5be6be33b051faa` / `data/raw/model_maintenance/2026-11-01/fara-817286a8d5f1.raw`. Qwen3.5-4B 기반/스크린샷 지각·DOM/AX 미사용·262144·MIT·참고 실행/장비 관련절. Mage의 DOM표현과 구분; 장비조건을 Mage로 승계하지 않음.

- `eval` https://huggingface.co/microsoft/Mage-VL-Cowork/raw/main/osworld_eval/README.md / UTC `2026-10-31T20:02:14.738841+00:00` / SHA256 `fa8ebfb603bdc0fb4a8207a6d2dfe078096dc79d3ae4e529981c3c9d892a0a93` / `data/raw/model_maintenance/2026-11-01/eval-fa8ebfb603bd.raw`. OSWorld 참고 구현 전체. history3/images3/1920x1080·50단계/온도.7·topp.8·턴4096·네이티브SGLang generate/도구 실행조건 확인. 코드 실행 없음.

- `repo` https://raw.githubusercontent.com/microsoft/Mage/main/mage_vl_cowork/README.md / UTC `2026-10-31T20:02:14.769917+00:00` / SHA256 `28632d12e7cfcccc9b59c084fcf466fdcb3ac0cf5ebc2401ccb83874963816bf` / `data/raw/model_maintenance/2026-11-01/repo-28632d12e7cf.raw`. 발견·보조범위확인;별도전문심층검토아님.

- `weight-index` https://huggingface.co/microsoft/Mage-VL-Cowork/raw/main/model.safetensors.index.json / UTC `2026-10-31T20:02:14.789791+00:00` / SHA256 `1a8a4de6a736179dbd39a264ba09555ba7b37e552fc3fde746382a28faba1014` / `data/raw/model_maintenance/2026-11-01/weight-index-1a8a4de6a736.raw`. 발견·보조범위확인;별도전문심층검토아님.

- `mini` https://developers.openai.com/api/docs/models/gpt-5.4-mini / UTC `2026-10-31T20:04:10.196300+00:00` / SHA256 `c6e6cc3a3a681fa2cbddb5d03a4118f8e8ed9053193492f2b7213ce0ba71db82` / `data/raw/model_maintenance/2026-11-01/mini-c6e6cc3a3a68.raw`. 정확한 GPT5.4-mini 공식 모델 문서의 입출력/400000·272000·128000/추론 설정·snapshot·지역처리 조건. 모델규모 미공개 유지.

- `price` https://developers.openai.com/api/docs/pricing / UTC `2026-10-31T20:04:12.798261+00:00` / SHA256 `5c3217d1076c8cf3baa68f6100fc16cfc8471dad5765a4862e20edeac7b1343d` / `data/raw/model_maintenance/2026-11-01/price-5c3217d1076c.raw`. 공식 현재 Standard 표의 정확mini .75/.075/4.50 USD/100만토큰과 캐시·지역·reasoning 과금조건 독해. Batch/Flex/Priority와 혼합하지 않음; 청구시험 없음.

- `lifecycle` https://developers.openai.com/api/docs/deprecations / UTC `2026-10-31T20:04:15.386763+00:00` / SHA256 `99f1a2e7be6142988cc4341f4a8b0f53b06a2ead70c3203a2b93dea211c047fb` / `data/raw/model_maintenance/2026-11-01/lifecycle-99f1a2e7be61.raw`. 발견·보조범위확인;별도전문심층검토아님.

## 발행 상태

로컬 research-check1편/40신규사실·publish/지식연결완료. 선택제출소스와공개검증은아직진행중이다. 모델설치·독립추론/한국어/Windows·실계정/실청구·전체공급자전수검토는미수행이다.


## 제출 소스 검증 완료 — 공개 전

다른작업을제외한Git index10경로와기존main을별도owned scratch로내보냈다.새branch/clone/worktree는만들지않았다.검증한공개state-20261031T020713Z-41158444995-1.tar.gz에서DB와archive만안전경로검사후복원했고SQLite integrity는ok다. 214개테스트(117.290초),품질검사/publish/audit·brief/review가통과했다.원문17/800수집은이번실행의기존checkout에서이미완료했고선택소스에서는불필요하게반복하지않았다.

실제Edge1280/390px에서소개5표·인용anchor·전체모델표링크·모바일넘침없음을확인했다.공식필터의Microsoft관측에서OSWorld66/361조건과PDF출처·1Nov확인일,웹58.6의SFT판/최종RL미보고,실제32768과설정262144·API미확인을확인했다.표의실제선택열에서OpenAI mini .75/.075/4.5 USD/100만토큰과공식가격URL/확인일을대조했다.기존Mistral사양1차→2차·09일→31일및소개3판링크도보존된다.본검사PNG는직접시각확인했다.

brief는공개상태의주거출력회귀검사이며새주거공고원문검토가아니다.같은HTML을Edge로PNG생성한뒤review했다.원래이미지경로의지연원인을고친것으로세지않는다.기존ResourceWarning은별도수명경고이며이번모델실패와구분한다.외부스크립트의첫실행은PYTHONPATH누락으로draft생성전에실패해실제프로젝트경로를지정했다.품질검사의지원anchor·report-v1필드오류는배치작성전에수정했다.검사실패가있으면로그에보존하고제품코드를변경하지않는다.

첫화면검사의문맥숫자검사는32768무구분문자열을가정해실패했다. 실제renderer는en-US천단위표시로32,768/262,144를보여주므로검사기대값만교정했다. 제품코드는바꾸지않고같은선택소스의publish/품질·brief/review/화면검사를다시수행했다.이미통과한단위시험은불필요하게반복하지않았으며첫실패는selected-check.log,수정후성공은selected-browser-recheck.log에별도보존한다.

원문은data/raw/model_maintenance/2026-11-01,계획/초안·선택검증로그/JSON·PNG와재현스크립트는D:/9_codex_temp/2026-11-01/signal-models에필수근거로유지한다.선택소스·상태시험복사본은마지막소비자종료후공통runner가회수한다.독립모델실행/사람시험없음은변함없다.공개완료는Pages및실제URL검증뒤기록한다.


## 실제 공개 완료 — 2026-11-01 05:30 KST

소스`c99b19ad5234bd864a52e4f439fa0a4be3b2e56c`를기존main에정상push했고 [Pages41238839569](https://github.com/Hansihoo/signal-desk/actions/runs/41238839569)가성공했다.실제Actions의테스트·공개수집/publish·brief/review·상태저장·Pages배포완료를확인했다.후속완료기록커밋은문서만이며skip ci로추가배포하지않는다.

공개 [Mage-VL-Cowork 소개1판](https://hansihoo.github.io/signal-desk/preview/mage-vl-cowork-model-guide.html)과 [전체모델비교표](https://hansihoo.github.io/signal-desk/preview/ai-models.html)가동시에반영됐다.소개본문과40신규사실의payload/정확값·원단위/조건·원문URL/1Nov확인일이검토입력과같다.기존89현재보고서와220이전보고서판/기존model2269현재·2376이전판/Theo원본17현재·19이전판을정확보존했다.현재보고서는90편/221판,모델2309관측/2416판이다.신규소개와관측은1판이며새모델의없는과거판을만들지않았다.

실제공개Edge1280/390px에서제목·5표·본문목적/요약·내부anchor·전체표링크와모바일넘침없음을확인했다.Microsoft공식보기의66/361과제/PDF원문·날짜,58.6의앞선SFT판/최종RL미보고,실제32768과설정262144·API미확인,OpenAI가격보기선택열의.75/.075/4.5USD/100만토큰과가격출처/확인일을확인했다.기존Mistral사양1차→2차·09일→31일/소개3판링크도동작한다.공개PC/모바일·평가/가격화면PNG를직접읽었다.

이는원문문헌/작성자독해·배포/화면검증이다.가중치설치나독립성능재현,한국어회사문서/Windows앱/실계정/청구/사람시험을수행했다고확대하지않는다.초기발견경로실패·가격동적표파서·지원anchor/JSON필드교정과수집성공을구분한기록은보존했다.공개한표와본문에서상대열세·실제제공조건과미확인은유지된다.

필수근거는data/raw/model_maintenance/2026-11-01과D:/9_codex_temp/2026-11-01/signal-models에보존한다.계획·품질/원문영수증·PDF원표PNG·선택/공개검증로그와JSON/실제화면은삭제가능으로표시하지않았다.선택소스/공개DB시험복사본은마지막소비자종료후공통scratch실행기가회수했다.다른작업의미제출변경과기존로컬지식레지스트리는이제출에포함하지않았다.
