# 2026-10-29 AI 모델 검토

독자의 질문은 Carbon이 Argon과 주요 경쟁 모델에 비해 어떤 장단점을 보이며 현재 이용과 비용 조건이 무엇인가다.28일 공식 발표된 새 모델을 선정했다.13일 Argon 공개 확대와 구별하며 처음 발견한 과거 모델을 모두 새 출시로 세지 않는다.

## 실제 취득과 검토 범위

Theo model-pages --collect는16문서 동일/실패0,ai-models --collect는800원본관측 동일/실패0이었다. 별도 signal_review collect733후보/21발견경로와 AI피드는 수집 성공이며 전 원문의 검토는 아니다. 아래 선택 원문 관련절을 실제 검토했다. 전 제공자 심층 검토나 모델 실행은 수행하지 않았다.

Google 발표 본문과 비교 이미지 전체,5쪽 평가 PDF2–4쪽 방법/5쪽 표를 읽었다. AA v5.0,모델별 추론 설정과 작업비용,현재 공식 API/요금/카드 목록을 대조했다. AA의Carbon1M/입출력과 공식API미공개를 구별했다. Argon의출력한도/옵션을Carbon에이식하지않는다.

- FrontierSWE2 61.2는 Astra65.5와Opus62.3보다 낮고 OSWorld offline81.5도Opus87.2보다 낮다.
- OSWorld82과제/3실행최대,ALE17일판122과제5시간/26일업데이트미적용,GraphWalks200문제를보존했다.
- 보안결과는guardrail없는설정,Gemini자체/외부기관/경쟁공개값을구분했다. ExploitGym6h/10h와표단일값의연결미확인은유지했다.
- Carbon출시2/10USD1M,95%캐시할인에서0.10계산,예고표준4/20과만료일/별도표준캐시미확인을분리했다. Argon12월1일일정으로대체하지않는다.
- AA작업비용7.76/6.24/10.04와출력200M/54M/220M은평가기관설정별결과이며실청구나공통회사작업비용이아니다.

AA수집기의응답크기상한실패뒤선정한원문에한해16MiB상한으로재취득해실제bytes/UTC/hash를보존했다. 공개backlog크기제한은바꾸지않았다. PDF취득은성공했으나HTML텍스트변환의재귀실패가있어PDF추출/시각확인으로읽었다. 수집과변환/독해의성공을구분하며일반수집기코드는변경하지않았다.

## 취득 영수증과 선택 관련절

- `launch`: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/ / UTC `2026-10-28T20:01:13.398310+00:00` / SHA256 `d84533cfb6dd470a4a359d7505b49fcaf2a8177b95d10ed7cab0d77a6b318fcc` / `data/raw/model_maintenance/2026-10-29/launch-d84533cfb6dd.raw`. 28일 새 발표, 제한/Fairwind/일반확대 미정, 할인2/10과95%/표준4/20 및 내부 정렬/주입 평가지표를 읽음. 만료일 미공개.
- `chart`: https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini_4_carbon__evals-table.width-1200.format-webp.webp / UTC `2026-10-28T20:01:23.002784+00:00` / SHA256 `bf06006b602be15bc91f0a65d2b4ced392aeb4f4ca69fa0466ae068dc594bed3` / `data/raw/model_maintenance/2026-10-29/chart-bf06006b602b.webp`. 공식 비교 이미지 전체를 시각 독해. AA v5/코딩/OSWorld/GraphWalks/시각/과학/사이버 선택 수치와 Carbon 열세를 전사/재대조.
- `google-method`: https://deepmind.google/models/evals-methodology/gemini-4-carbon / UTC `2026-10-28T20:03:00.292361+00:00` / SHA256 `729c10bcdcd68998f4ba3b0e81376788886e38e473c33c700ea9bd609bca45ad` / `data/raw/model_maintenance/2026-10-29/google-method-729c10bcdcd6.raw`. 5쪽 PDF의2–4쪽 방법과5쪽표를 읽음. 최고thinking/pass@1 예외, ALE17일판122과제5h, OSWorld82과제3실행max, GraphWalks200문제, cyber Harness/시간/표본을 대조.
- `aa`: https://artificialanalysis.ai/models/gemini-4-carbon / UTC `2026-10-28T20:01:29.586210+00:00` / SHA256 `2e1e557c3dc2d1eeb453b8028e8cf1c417d37dd49fa645299d0bb5a0a50a1f52` / `data/raw/model_maintenance/2026-10-29/aa-2e1e557c3dc2.raw`. 직접취득 현재 페이지의High59/1M/입출력/표준4/20/200M/작업7.76과 지수판을 읽음. API소개문구를 일반공개 증거로 채택하지 않음.
- `aa-method`: https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index / UTC `2026-10-28T20:01:35.723298+00:00` / SHA256 `8e5ba6fcf84815eedd4500c403ad4239671a7dcf0e64aa22898c3975cf047020` / `data/raw/model_maintenance/2026-10-29/aa-method-8e5ba6fcf848.raw`. 9개지표 v5.0과 독립측정, 작업비용의토큰/캐시/추론/가중치를 읽음.
- `opus-aa`: https://artificialanalysis.ai/models/claude-opus-5-5 / UTC `2026-10-28T20:02:11.988966+00:00` / SHA256 `db88ef38ac227d2270f2467c76d8084bf6eca6b8f0125a4cbd40aa5250cc18ad` / `data/raw/model_maintenance/2026-10-29/opus-aa-db88ef38ac22.raw`. Max Default Fallback 58/작업10.04/전체출력220M을 읽음.
- `astra-aa`: https://artificialanalysis.ai/models/gpt-6-astra / UTC `2026-10-28T20:02:19.510712+00:00` / SHA256 `fa7ec146bd55456018e4e3a6e24e0c097299d5d5465f5e88db95d4edd3678b75` / `data/raw/model_maintenance/2026-10-29/astra-aa-fa7ec146bd55.raw`. Max57/작업6.24/전체출력54M을 읽음.
- `argon`: https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-argon/ / UTC `2026-10-28T20:01:42.548707+00:00` / SHA256 `69f6a695842335004519726073ee6c6b0fe2a1f2cde611016f7ac2763c8af93c` / `data/raw/model_maintenance/2026-10-29/argon-69f6a6958423.raw`. 13일개발자제공확대와유료API/앱/Ultra조건,기존모델임을 확인.
- `api-models`: https://ai.google.dev/gemini-api/docs/models / UTC `2026-10-28T20:01:56.714416+00:00` / SHA256 `2a6442d63c46d41ad8b9741876a2aa68599a7bc654a935b20654e472d0a3cb48` / `data/raw/model_maintenance/2026-10-29/api-models-2a6442d63c46.raw`. 현재Gemini4공개목록의Argon ID와Carbon부재를 실제확인. 부재를 개발/테스트모델없음으로 해석안함.
- `pricing`: https://ai.google.dev/gemini-api/docs/pricing / UTC `2026-10-28T20:02:03.833366+00:00` / SHA256 `7ebde42c5eaec4618ccd5feba577a42a527ea7a98f6fb4951146da875711ddf1` / `data/raw/model_maintenance/2026-10-29/pricing-7ebde42c5eae.raw`. Argon Standard2/.10/10 11월30일까지→4/.20/20 12월1일,implicit캐시와다른처리요금. Carbon항목없음.
- `argon-api`: https://ai.google.dev/gemini-api/docs/models/gemini-4-argon / UTC `2026-10-28T20:03:14.579329+00:00` / SHA256 `6300ab3195520022638aba72f3375e9d899765485f0928c09edd2937a1a08217` / `data/raw/model_maintenance/2026-10-29/argon-api-6300ab319552.raw`. 입출력/PDF/통합1048576/기본65536과longdecode를 분리. Carbon에승계안함.
- `claude-prices`: https://platform.claude.com/docs/en/about-claude/pricing / UTC `2026-10-28T20:03:24.269679+00:00` / SHA256 `5cb73823b211f78fea691bc70185589aa14a3d67e25a8dde47fad70cc69ca195` / `data/raw/model_maintenance/2026-10-29/claude-prices-5cb73823b211.raw`. Opus5.5기본4/20/캐시읽기.20,5m쓰기5와1h쓰기8을 실제요금행에서확인.
- `openai-spec`: https://developers.openai.com/api/docs/models/gpt-6-astra / UTC `2026-10-28T20:03:31.452390+00:00` / SHA256 `dd1b7f62d447e76b54143c9bdcbc3c5edb1b39c3e28dcad7ab82516cd44a35cc` / `data/raw/model_maintenance/2026-10-29/openai-spec-dd1b7f62d447.raw`. Astra문맥1050000/최대출력128000,텍스트이미지→텍스트,10/1/50과272K초과전체요청2배/1.5배를확인.
- `claude-spec`: https://platform.claude.com/docs/en/about-claude/models/overview / UTC `2026-10-28T20:03:39.345358+00:00` / SHA256 `d7a2eb3b10e57dbaf4b03c93c148c5ba273d561e8b350fc8af0727c464582712` / `data/raw/model_maintenance/2026-10-29/claude-spec-d7a2eb3b10e5.raw`. Opus5.5모델ID/1M/최대128K/텍스트이미지입력과제공플랫폼을읽음.
- `model-cards`: https://deepmind.google/models/model-cards/ / UTC `2026-10-28T20:03:07.533381+00:00` / SHA256 `2290d2390fddbb2288036d009a0b0c66d41055e8c6d5fd5680dd81aab556e3be` / `data/raw/model_maintenance/2026-10-29/model-cards-2290d2390fdd.raw`. 현재카드목록Gemini절에Carbon없음과Argon13일카드를확인. 전구글미공개단정안함.

## 원고 및 로컬 검증

새불변소개/품질배치와62관측facts를두manifest에동시등록했다. 본문5표/5설명절과출처15개,장단점/가격/제한제공을분리했다. 같은작성자가title/description/deck만따로읽고본문/원문을대조했다. 독립리뷰어나사람독해시험은아니다.

research-check1편과audit현재판gated_agent_review,ai-models입력62신규와publish를확인했다. 현재본문1판의source_hash/document_digest를새불변로컬검토원장에연결하고실제검색에서본문/출처를반환했다. 현재usable_with_limits이며계정접근/한국어실무/성능재현/과금은미수행이다.

로컬Edge1280/390px에서소개5표와전체표공식평가61.2실제셀,Google필터/원문/29일확인일/출시2/.1/10및표준4/20,기존LFM3이전판을확인했다. 페이지너비넘침/JS오류는없었다. 첫검사의행1개가정은검색이공통suite/condition과effort라벨도포함하기때문에실패했다. 제품필터를변경하지않고정확한모델접두행을선택하도록검사기를고쳐통과했다.

제출소스의전체시험/공개상태복원/publish/brief/review,원격배포와실제공개검증은후속절에기록한다. 이시점은공개완료가아니다. 다른dirty작업은제출하지않는다.


## 제출 소스 검증

선택한10개경로의index만LF로내보내다른작업을제외했다. 공개snapshot state-20261028T020414Z-40618663688-1.tar.gz의DB와archive만복원해전체214시험,Theo수집/모델입력/publish/brief/review 및실제Edge1280/390px를확인했다. 수집원문/DB/HTML/PNG는제출하지않는다. 새소개내부경로/fragment188개가정상이다. 자세한실제출력은외부검증폴더selected-check.log와local-browser.json에보존했다. 기존brief PNG명령은임시Edge가종료되지않아해당작업소유PID만검증후정리했고원명령exit1을보존했다. 같은선택소스fixture가살아있는동안별도Playwright임시프로필로390x1500 PNG를생성해시각확인한후review12항목PASS와모델브라우저검사를별도로완료했다. 이대체검증을원명령성공이나렌더러원인수정으로기록하지않는다. 복원된주거표시/기한은형식검사이며최신공고자격재검토가아니다. owned scratch와자식프로세스는종료후정리했다. 정상push와실제공개결과는후속절에기록한다.


## 실제 공개 검증 완료 — 2026-10-29 05:34 KST

소스78acacf를 main에 정상push했고 [Pages40762896056](https://github.com/Hansihoo/signal-desk/actions/runs/40762896056)는success로완료됐다. CI시험/공개상태복원/수집·사이트생성/주거briefing검사/누적snapshot저장/Pages배포가통과했다.

실제공개research-data.json에서보고서87편/217판,모델2169관측/2275판을확인했다. 기존86현재보고서/216문서판과2107관측/2213모델판,Theo16현재/18문서판은전체값을대조해보존됐다. 새소개1판전체payload와62개사실의원문/수치/조건/날짜가검토입력과정확히같다.

공개Edge1280/390px에서소개5표,전체표공식평가FrontierSWE2 61.2실제셀,Google필터/원문/29일확인일/출시2/.1/10과표준4/20·미확인,이전LFM3판을확인했다. JS오류와페이지너비넘침은없다. 새소개/전체표/이전모델3주소는HTTP200이다. 실제모델/한국어업무/계정접근/청구/독립재현/사람독해시험은수행하지않았다.

- [Carbon소개](https://hansihoo.github.io/signal-desk/preview/gemini-4-carbon-model-guide.html)
- [전체모델비교표](https://hansihoo.github.io/signal-desk/preview/ai-models.html)

원본bytes와공개전후JSON은data/raw/model_maintenance/2026-10-29에비추적으로보존했다. D:/9_codex_temp/2026-10-29/signal-models에는원문/본문검토및로컬·공개검증스크립트/요약/PNG를필수증거로보존한다. 임시선택소스/DB/백업압축/브라우저프로필은owned scratch종료시정리했다. 기존다른dirty작업은제출하지않았다. 원PNG명령의대기문제는대체검증과구분해앞절에보존하며원인수정완료로보고하지않는다.
