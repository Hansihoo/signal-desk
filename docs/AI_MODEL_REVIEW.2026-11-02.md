# 2026-11-02 Surya 2.5와 SenseNova Loop 모델 검토

현재 상태: 상세 소개2편과전체표86관측의공개반영/실제검증완료. [Pages41346862726](https://github.com/Hansihoo/signal-desk/actions/runs/41346862726). 아래공개전기록은당시상태이며최종결과는끝의공개완료절을따른다.

목표는 문서 OCR과 문서/도구 모델의 이전 및 경쟁 대안 대비 변화, 성능의 반대 결과, 실제 제공과 비용을 비교하는 것이다. 콘텐츠 추가이며 UI나 기존 실행 코드 변경은 없다. 위험은 다른 평가판/장비/추론조건, 코드와 가중치 라이선스, 데모와 제품출시, 저장 규모와 반복 계산을 합치는 것이다. 검증은 원문 관련절/원차트, 별도 첫화면과 본문, 품질, 정확한 제출소스 테스트/publish/brief/review, 실제 PC/모바일 및 공개 값/단위/출처/날짜/이전판 보존이다.

## 실제 발견과 내용 검토 범위

Theo model-pages17개/전체표원본800관측을 취득했으며 해당 원본 신규0/변경0이다. signal_review는21경로723항목 취득 성공/실패0이다. 목록과 검색은 발견경로이며 원문 검토나 전공급자 전수검토가 아니다. 기존 소개/보고서ID와 대조했다. Nemotron3.5Retriever는기존22Oct소개이며재보도, Mage는1Nov완료건으로반복하지않는다. Heretic/Memdoor/boot-sector데모를새기반출시로분류하지않는다.

Surya2.5의발표는29Oct이고공식HF저장소생성25Oct/최종수정29Oct와다르다. SenseNovaLoop의공식발표는30Oct이고저장소생성28Oct/수정1Nov와구분한다. 2Nov는이번확인일이며늦은확인이다.

Surya공식발표/카드의OPB짝비교,현재데이터셋순위표,olmOCR/91언어전체표,H100/M4및appendix의분모/출력상한/DPI/후처리를대조했다. 같은패키지83.3과현재순위표83.1,표시85.9−83.3과반올림전+2.7을분리했다. Chandra종합90.1,MiniCPM표89.1/Unlimited표79.7,영어/러시아어·OldMath하락을포함했다. 표HTML과행열좌표미지원,가중치수정OpenRAIL/경쟁서비스및Share-a-Like문구와코드Apache2.0을분리했다. 관리형Convert4/10USD/1000페이지는Surya전용API가아니며현재표준과과거할인가를합치지않는다.

SenseNova공식PNG를직접시각독해해8평가와비교모델수치를전사했다. 단위/표본/harness/추론예산미공개를임의%로채우지않고내부PPT평가를외부표준/실제PPTX검증으로승격하지않았다. Terminal40.45<Qwen27B47.19/Nanbeige49.44및Banking18.56<19.59를보존했다.32층/56회계산과9B/14.6B계산표기,262144학습/설정/미검증실사용을구분했다. 카드BF16/FP32설명과HF F32약94억+BF16약2.4억집계/38138420672파일바이트차이를명시했다. MTP제공/DSpark-Dflash2학습중,파일존재와문서리소스표TBA/보고서TBD시차를유지했다. 직전동일체크포인트통제평가나구조인과효과는확정하지않는다.

본문없는first-screen파일2개를따로읽고목적/변화/한계가설명되는지확인한뒤본문과원문표를대조했다. 같은작성자검토이며독립에이전트/사람시험이아니다. 초안highlights빈배열은발행전체약검사에서검출해고쳤다. 제품코드나기존불변배치를변경하지않았다. research-check2편통과/86개공식관측과로컬publish완료,실제1판지문에로컬검토원장/지식색인과두독자질의를연결했다. 지식plain-text출력의advisory문자열형식오류는JSON출력으로회피했고별도구현을고치지않았다.

## 공식 원문 취득 영수증과 실제 독해 범위

- `surya-blog` https://api.datalab.to/blog/surya-2-5 / UTC `2026-11-01T20:05:10.734274+00:00` / SHA256 `68bda59efaf05ccdc0191bc77346a27299d349fb1a17a29a7dc5226bc9df126a` / `data/raw/model_maintenance/2026-11-02/surya-blog-68bda59efaf0.raw`. 29Oct 발표, 실제 0.23.0 전환, 어휘/표현 변화, OPB와 olmOCR/다국어 평가의 방법/반대 결과, H100·M4속도/상한/표본 및 appendix와 한계, 관리형 별도 Chandra 경로를 읽음. 전 코드/실행 재현 없음.

- `surya-card` https://huggingface.co/datalab-to/surya-ocr-2.5/raw/main/README.md / UTC `2026-11-01T20:05:10.039836+00:00` / SHA256 `ba8c3eda9c7c7823a2d2a2a2abd26a8a9ce32be7f46948566b966caae0a2a154` / `data/raw/model_maintenance/2026-11-02/surya-card-ba8c3eda9c7c.raw`. 모델 개요, 689M, 단일 VLM과 별도 검출기, 표 HTML과 행/열좌표 한계, 상업 사용, OPB/olmOCR/91언어 및 H100/M4 평가와 조건 관련절. SDK 예제 실행 없음.

- `surya-config` https://huggingface.co/datalab-to/surya-ocr-2.5/raw/main/config.json / UTC `2026-11-01T20:05:10.014000+00:00` / SHA256 `37b7e37ff4ca2e6ec7c67e2808b61274c0d08aeef80bb03349637743ae7db2ec` / `data/raw/model_maintenance/2026-11-02/surya-config-37b7e37ff4ca.raw`. 88526어휘/24층/262144위치범위/모델타입/mtp0 확인. 장문 지원이나 최소 자원을 추정하지 않음.

- `surya-license` https://huggingface.co/datalab-to/surya-ocr-2.5/raw/main/LICENSE / UTC `2026-11-01T20:05:10.020776+00:00` / SHA256 `636dfb8eb19efc5835ed6efb878f8b694a93f028c715d2547d831e2a55440276` / `data/raw/model_maintenance/2026-11-02/surya-license-636dfb8eb19e.raw`. 수정 OpenRAIL-M 본문과 부속서A의 전년총매출/누적조달 5M초과, 개인연구 예외, 경쟁서비스 별도제한 및 결과물/표시/Share-a-Like 관련절. 법률 승인 없음.

- `surya-meta` https://huggingface.co/api/models/datalab-to/surya-ocr-2.5 / UTC `2026-11-01T20:05:10.017049+00:00` / SHA256 `b818883c8408ae8f52081170c5858817de2ec43d2c24762a25a3bf87c846b02d` / `data/raw/model_maintenance/2026-11-02/surya-meta-b818883c8408.raw`. 발견/보조 자료이며 별도 전문 검토로 세지 않는다.

- `surya-prev` https://huggingface.co/datalab-to/surya-ocr-2/raw/main/README.md / UTC `2026-11-01T20:05:10.031442+00:00` / SHA256 `7b43065e8610d9d80c8f4ae222a775b4e945ba93b10c57cb2dd165f36dc0b775` / `data/raw/model_maintenance/2026-11-02/surya-prev-7b43065e8610.raw`. 이전 Surya2 개요/같은 가중치 라이선스와 표 좌표 역할 관련절. 기존 정확도 수치와 현재 같은 패키지 재평가를 별개로 보존.

- `surya-languages` https://huggingface.co/datalab-to/surya-ocr-2.5/raw/main/static/docs/multilingual.md / UTC `2026-11-01T20:05:10.013043+00:00` / SHA256 `d84cb92dda5ba96d15bba016806e5790cae3d218cb39b1b847a3bf44b34db5b2` / `data/raw/model_maintenance/2026-11-02/surya-languages-d84cb92dda5b.raw`. 91언어/36089시험과 언어별범위, 한국어77.3/77.9·영어94.3/90.3·러시아어77.8/71.7 등의 전체 표를 읽음. 문자정확도/자사실험으로 전환 안함.

- `surya-release` https://api.github.com/repos/datalab-to/surya/releases/tags/v0.23.0 / UTC `2026-11-01T20:05:10.259393+00:00` / SHA256 `ebc61718fd6ff2f9883a0c51ce493578553d03d4cf1e0a36ebba10c33f0348b8` / `data/raw/model_maintenance/2026-11-02/surya-release-ebc61718fd6f.raw`. 0.23.0 실제 발표 UTC/기본 Surya2.5 체크포인트와 표 HTML/행열 기능 분리/실험 MLX·이전2로 고정 경로를 읽음.

- `loop-card` https://huggingface.co/sensenova/SenseNova-Loop-9B-Preview/raw/main/README.md / UTC `2026-11-01T20:05:10.239891+00:00` / SHA256 `64056fd1c17c33827e6d7ca8b1fe479868f374f7cc7e3e4d30e25e090ab19a31` / `data/raw/model_maintenance/2026-11-02/loop-card-64056fd1c17c.raw`. 30Oct발표,32/56층·9B/14.6B·2stream/mHC/262144,입출력/영중태그·MTP제공/DSpark/Dflash2학습중,구현파일/참고버전과TBD모순을 읽음. 데모를제품출시로 취급안함.

- `loop-config` https://huggingface.co/sensenova/SenseNova-Loop-9B-Preview/raw/main/config.json / UTC `2026-11-01T20:05:10.247458+00:00` / SHA256 `3069b497e0a9ba70b1f74561831cbab0df0ccc4247f3ae106054c1632360ef51` / `data/raw/model_maintenance/2026-11-02/loop-config-3069b497e0a9.raw`. 반복4~27층2회와mHC2/20,262144,custom auto_map 및text/vision구성 확인. 단순Qwen호환/영상지원 승계 안함.

- `loop-meta` https://huggingface.co/api/models/sensenova/SenseNova-Loop-9B-Preview / UTC `2026-11-01T20:05:10.242721+00:00` / SHA256 `94e8e26ce5fa2cb293219e1401706b12ad62fd38feffab2ea16fb4a7273b4a9e` / `data/raw/model_maintenance/2026-11-02/loop-meta-94e8e26ce5fa.raw`. createdAt28Oct15:34UTC와lastModified1Nov09:33UTC,revision·공개파일/F32와BF16 텐서총수 확인. 실제발표30Oct와구분.

- `loop-index` https://huggingface.co/sensenova/SenseNova-Loop-9B-Preview/raw/main/model.safetensors.index.json / UTC `2026-11-01T20:05:10.272190+00:00` / SHA256 `5014b5de96f5d3a46eea22b4bf3823697e5211bd615f9011ba71ee3a1c0bace2` / `data/raw/model_maintenance/2026-11-02/loop-index-5014b5de96f5.raw`. metadata total_size38138420672바이트와8가중치파일키 확인. 최소VRAM/최소GPU로 변환안함.

- `loop-repo` https://raw.githubusercontent.com/OpenSenseNova/SenseNova-Loop/main/README.md / UTC `2026-11-01T20:05:31.314415+00:00` / SHA256 `27adeed025a6456fbaf280163d53402754c5bde906582b936e330e21f909b994` / `data/raw/model_maintenance/2026-11-02/loop-repo-27adeed025a6.raw`. 발견/보조 자료이며 별도 전문 검토로 세지 않는다.

- `loop-license` https://raw.githubusercontent.com/OpenSenseNova/SenseNova-Loop/main/LICENSE / UTC `2026-11-01T20:05:31.510728+00:00` / SHA256 `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4` / `data/raw/model_maintenance/2026-11-02/loop-license-c71d239df917.raw`. Apache2.0 전문의사용/재배포4항·고지·변경표시·상표/무보증 관련절. 개별사업 법률승인 아님.

- `loop-chart` https://huggingface.co/sensenova/SenseNova-Loop-9B-Preview/resolve/main/assets/loop9b-benchmark-results.png / UTC `2026-11-01T20:06:08.465302+00:00` / SHA256 `a7545bb81c6078c504b84eb6126fbc91b40391ed59bda6d593e1d3aa46a109d9` / `data/raw/model_maintenance/2026-11-02/loop-chart-a7545bb81c60.png`. 공식PNG를원해상도시각독해해8평가/Loop·Qwen3.5-9B/27B·Qwen3.6-35B-A3B·Nanbeige값과내부RaccoonPPT각주를 수동전사. 정확단위/표본/harness/추론예산 미표시 유지.

- `opb-card` https://huggingface.co/datasets/datalab-to/omni_parse_bench/raw/main/README.md / UTC `2026-11-01T20:06:07.301934+00:00` / SHA256 `efdf45a881ad64a80f82bb6399c57346e1a02384dce5f6450a575da8daeb9cfa` / `data/raw/model_maintenance/2026-11-02/opb-card-efdf45a881ad.raw`. 현재 순위표의 종합/텍스트/표/레이아웃, 16288/2937/2343/92언어, 권장설정/어댑터·이전Surya83.1/별도재평가83.3 및 과거가격/실측비용 한계 관련절. 제공자 자체평가로 유지.

- `datalab-price` https://www.datalab.to/pricing / UTC `2026-11-01T20:06:08.436987+00:00` / SHA256 `0bd13ccac9ca2417d959208588a24bfadf57629502ea706e6627bb9f0dc3623a` / `data/raw/model_maintenance/2026-11-02/datalab-price-0bd13ccac9ca.raw`. 현재 Convert fast/balanced4,accurate10 USD/1000page와 합산/EU25%/보존25 또는스타트업33할인/가중치 규모FAQ 관련절. Surya전용API/실청구 아님.

- `qwen35-card` https://huggingface.co/Qwen/Qwen3.5-9B/raw/main/README.md / UTC `2026-11-01T20:06:07.044425+00:00` / SHA256 `c5f5a8c2dddab69cfbf05279235aa5fddb137939a06539c4c7637aa900fef6d0` / `data/raw/model_maintenance/2026-11-02/qwen35-card-c5f5a8c2ddda.raw`. Qwen3.5-9B의9B/32층/시각입력·262144와1010000확장/Apache2.0 관련절. Loop직전초기체크포인트로 가정안함.

- `qwen36-card` https://huggingface.co/Qwen/Qwen3.6-27B/raw/main/README.md / UTC `2026-11-01T20:06:07.088710+00:00` / SHA256 `bb936d6da51014f1edc9aa4cf9abf28d98695b7616ad56adfeeebfa752051d3d` / `data/raw/model_maintenance/2026-11-02/qwen36-card-bb936d6da510.raw`. Qwen3.6-27B의27B/64층/262144와1010000확장/Apache2.0 관련절. 차트의35B-A3B 성능을27B로 옮기지 않음.

## 발행 상태

로컬 품질/86사실/지식연결 완료. 선택 제출소스와 공개 검증은 진행 중이다. 모델 실행, 한국어 회사 문서, 최소 자원, 실제 청구, 독립/사람 독해 시험은 수행하지 않았다.

## 정확한 제출 소스의 로컬 검증

Git index의선정10경로와HEAD만을공통소유scratch로내보냈다. 새clone/worktree/.git는만들지않았다. 공개11월스냅샷state-20261101T015828Z-41263184163-1.tar.gz의SHA256 b8f5de8db948dfec637cc9ecd4667cf1398f98267074403deb67d3ee0daa33d6를검증하고DB/archives만안전복원했다. 독립Python경로로214시험130.706초/품질2편/publish/audit/brief390및review통과. 92보고서/2395모델관측중새소개2편/86사실의JSON이정확하다. 기존시험의SQLite ResourceWarning은별도이며실패는없었다. 주거PNG는기존출력계약검사로보았으며과거공고내용의현재자격/마감을재검증한것은아니다.

IAB의file프로토콜정책거절은그대로보존하고재시도하지않았다. 공개예정HTML3개와CSS만복사한격리폴더를127.0.0.1의운영체제할당포트로읽었다. 고정8766의OS10013은예약포트접근실패이며권한/보안설정을변경하지않았다. CUA로두소개1280px DOM/내부anchor와390px첫화면스크린샷을읽고가로넘침없음을확인했다. SuryaPC스크린샷,비교표연결과공식보기/검색/상세를확인했다. Surya85.9원문/단위/2Nov확인일/1차,Convert4/10USD/1000페이지열,Loop262144/32층56회/Terminal40.45·정확단위미공개/원문차트·1차를실제UI에서대조했다. 초기의AXcheckbox와실제DOMbutton역할차이/검색30행표시때문에잘못지정한검사locator만고쳤고제품코드/원고는변경하지않았다.

공통scratch는검증소비자종료후정상정리됐다. 요구근거/최종선정HTML과로그는D:/9_codex_temp/2026-11-02/signal-models에보존한다. 공개배포와실제공개JSON/화면검증은다음단계다.

## 공개 완료 — 2026-11-02 05:33 KST

Source `3cfb80e80c8a3560e2fe0554c5818225fca6079a`를 기존main에일반push했고 [Pages 41346862726](https://github.com/Hansihoo/signal-desk/actions/runs/41346862726)가성공했다. 신규 [Surya2.5](https://hansihoo.github.io/signal-desk/preview/surya-2-5-model-guide.html), [SenseNovaLoop](https://hansihoo.github.io/signal-desk/preview/sensenova-loop-9b-preview-model-guide.html)와 [전체비교표](https://hansihoo.github.io/signal-desk/preview/ai-models.html)가같은작업에서반영됐다. source-refresh만의완료로세지않는다.

공개research-data의새소개2편과86개관측원본/fields/실제출처/2Nov확인일/1차가검토입력과정확히같다. 다른90현재보고서/221이전판/90report_versions,기존2309모델관측/2416이력및Theo17현재/19이력이전부같다. 현재92보고서/223이전판,2395모델관측/2502이력이다. 보고서2편/전체표/기존Mistral3판HTTP200을확인했다.

CUA로공개소개와전체표의검색/공식보기/상세를열어실제85.9·평가판/출처/확인일,Loop40.45·원문차트단위미명시/1차,Convert4/10USD/1000페이지/관리형별도조건과소개→전체표연결을대조했다. 공개PC/390px에서본문과표가보이고가로넘침이없음을확인했다. 별도UI증거/페이지영수증과public-before/after비교를보존한다. 실제모델추론/한국어회사문서/최소장비/실청구/독립사람독해는미수행이다.

검증증거는D:/9_codex_temp/2026-11-02/signal-models에유지한다. 요구된원문/품질·UI/테스트·공개보존증거이므로일회성scratch삭제대상으로등록하지않는다. 공개예정파일만제공한로컬서버는종료했고임시뷰포트는복원했다. 다른dirty변경과로컬지식원장은제출하지않았다.
