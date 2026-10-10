# AI 조사 출처 목록

등록 문서화일: 2026-10-09. 아래 공개 자료·접근 경로는 2026-10-08 조사에서 확인했다.
독자의 개발·도입·조직·경력 판단에 필요한 자료를 빠르게 찾기 위한 목록이다.
사이트 등록은 수집기 연결이나 예약 생성이 아니다. 제시한 주기는 목표 점검 주기이며 실제 실행 이력과 구분한다.
조사 범위·날짜·변경 판정은 [조사 운영](AI_RESEARCH_OPERATIONS.md)을 따른다.

## 이미 있는 수집 경로

현재 [AI 뉴스 수집 코드](../housing_watch/ai_news.py)의 `AI_FEEDS`에는 OpenAI·Hugging Face와
vLLM·llama.cpp·Ollama·LangChain·LangGraph·LlamaIndex·LiteLLM·promptfoo 릴리스의 10개 피드가 있다.
추가 Google News 탐색과 Theo 모델 자료 연결도 있다. 설정된 피드 수는 이번 실행의 성공 수가 아니다.
모델 누적 관측·전체 문서 수집은 [모델 운영](AI_MODEL_RESEARCH.md)의 경로를 유지한다.
아래 새 출처의 RSS·API·HTML 어댑터와 원문별 검토 상태 연결은 후속 구현이다.

## 우선 확인할 출처

| 출처 ID·공식 경로 | 찾을 내용 | 근거를 읽을 때의 제한 | 목표 점검 |
| --- | --- | --- | --- |
| `openai-news` · [OpenAI News](https://openai.com/news/) | 모델·제품·지원 조건의 발표와 변경 | 공급사 발표. 성능·활용 효과는 평가 조건과 독립 근거를 추가 확인 | 일일 후보 |
| `google-deepmind` · [Google DeepMind](https://deepmind.google/blog/) | 모델·연구·산업 적용 | 발표와 실제 제공 범위, 연구와 제품을 구분 | 일일 후보 |
| `github-changelog` · [GitHub Changelog](https://github.blog/changelog/) | 코딩 도구·플랫폼의 실제 기능 변경 | 출시 상태, 계정·플랜·적용일 확인 | 일일 후보 |
| `anthropic-engineering` · [Anthropic Engineering](https://www.anthropic.com/engineering) | 에이전트·문맥·운영의 설계 사례 | 해당 환경의 방법론. 모든 업무의 성공 조건으로 일반화하지 않음 | 일일 후보 |
| `anthropic-research` · [Anthropic Research](https://www.anthropic.com/research) | 모델 능력·안전·평가 연구 | 방법·표본·실험 조건과 저자의 해석 확인 | 일일 후보 |
| `huggingface-blog` · [Hugging Face Blog](https://huggingface.co/blog) | 오픈소스 모델·데이터·도구와 실행 사례 | 공식·커뮤니티 글의 저자 구분, 라이선스·환경·실행 여부 확인 | 일일 후보 |
| `palantir-ontology` · [Palantir Ontology](https://www.palantir.com/docs/foundry/ontology/overview) | 업무 개체·관계·작업을 AI와 연결하는 설계 | 특정 플랫폼의 설계. 온톨로지 일반 개념·대안과 구분 | 주간·개정 시 |
| `aws-knowledge-bases` · [Amazon Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html) | 지식베이스·검색·데이터 연결의 기능과 조건 | 지원 지역·권한·비용·데이터 갱신 조건은 적용 전에 재확인 | 주간·개정 시 |
| `thoughtworks-radar` · [Technology Radar](https://www.thoughtworks.com/radar) | 기술을 채택·시험·평가하는 관점과 새 주제 발견 | 편집진의 경험·판단. 프로젝트의 자체 검증 등급으로 복제하지 않음 | 주간·새 판 |
| `dora-research` · [DORA Research](https://dora.dev/research/) | 개발 조직·AI 활용·성과의 관계 | 보고서별 표본·측정·상관과 인과의 한계 확인 | 주간·새 자료 |
| `metr-research` · [METR Research](https://metr.org/blog/) | AI 작업 능력·개발 생산성의 실험과 평가 | 특정 과제·참여자·모델·도구 조건을 보존 | 일일 후보 |
| `atlassian-fde` · [Atlassian FDE 사례](https://www.atlassian.com/blog/how-we-build/meet-the-forward-deployed-engineer) | 기업 AI 도입에서 FDE가 맡는 역할과 업무 | 2026-10-07의 회사 자체 사례. 추가 발견은 [블로그](https://www.atlassian.com/blog)에서 탐색 | 주간·관련 채용 |
| `stanford-canaries` · [Stanford Canaries Dashboard](https://digitaleconomy.stanford.edu/project/indicators/canaries-dashboard/) | AI와 고용 변화의 관찰 자료 | 국가·연령·직무·기간·데이터 범위와 인과 추정 한계 확인 | 주간·데이터 갱신 |
| `oecd-ai-work` · [OECD AI at Work](https://www.oecd.org/en/about/programmes/ai-in-work-innovation-productivity-and-skills.html) | 업무·생산성·숙련·정책 변화 | 국가·산업·조사 시점과 지표 정의를 한국 적용과 구분 | 주간·새 연구 |
| `ilo-ai-work` · [ILO Artificial Intelligence](https://www.ilo.org/topics-and-sectors/artificial-intelligence) | 직무·업무의 AI 노출과 전환 | 업무 노출을 실제 해고·실업으로 바꾸지 않음 | 주간·새 연구 |
| `bok-ai-work` · [한국은행 AI·지역 인력시장 자료](https://www.bok.or.kr/portal/bbs/P0002353/view.do?menuNo=200433&nttId=11064752&pageIndex=1) | 한국의 AI·지역별 인력시장 변화 | 2026-09-15 자료. 연결된 BOK 이슈노트 목록에서 후속 자료 탐색; 측정 기간·지역·방법 확인 | 주간·새 자료 |
| `stanford-ai-index` · [Stanford AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report) | AI 산업·투자·도입·사회 변화의 기준 자료 | 연간 종합 자료. 각 수치의 실제 조사 기간·원출처와 다음 판 확인 | 새 판·필요 시 |
| `anthropic-economic-index` · [Anthropic Economic Index](https://www.anthropic.com/economic-index) | AI가 어떤 업무에 어떻게 쓰이는지 | Claude 이용 데이터의 범위를 전체 산업·고용 대표 표본으로 간주하지 않음 | 주간·새 자료 |
| `owasp-genai` · [OWASP GenAI Security](https://genai.owasp.org/) | AI 앱·에이전트의 보안 실패와 방어 | 권고·위협 모델을 실제 환경과 비교; 실제 사고 근거는 별도 확보 | 일일 후보 |
| `nist-ai-rmf` · [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) | 도입·운영의 위험·책임·평가 체계 | 프레임워크와 법적 의무를 구분하고 적용 대상 확인 | 주간·개정 시 |
| `arxiv-ai` · [arXiv cs.AI](https://arxiv.org/list/cs.AI/recent) | 새로운 기법·평가 문제 발견 | 논문별 개정·심사 상태, 방법·코드·재현 확인; 필요하면 cs.CL·cs.SE로 확대 | 일일 후보 |
| `hacker-news` · [Hacker News](https://news.ycombinator.com/) | 새 도구·실무 문제·논쟁의 초기 발견 | 탐색용. 주장·수치는 원문·공식 자료로 추적하고 댓글을 검증 근거로 대체하지 않음 | 일일 후보 |
| `geeknews` · [GeekNews](https://news.hada.io/) | 한국 개발자가 주목하는 기술과 실무 변화 | 탐색용. 번역·요약의 생략과 원문 의미를 확인 | 일일 후보 |

정적 사례 문서 하나를 피드처럼 취급하지 않는다. 문서 개정 확인과 같은 분야의 새 자료 탐색을 구분한다.
이 목록의 등록일·경로 확인일은 매 항목의 모든 주장에 대한 현재 검토일이 아니다.

## 채용·도입 성과를 보완하는 경로

FDE, AI 엔지니어, 데이터·도메인 역할은 관련 회사의 공식 채용 페이지와 실제 공고를 추가 확인한다.
회사·지역·경력·공고 ID·업무·요구 역량·실제 수집 시각·모집 상태를 기록한다.
재게시·지역별 중복을 제거하고, 여러 시점에 같은 정의로 비교해야 수요 추이를 논할 수 있다.
검색 결과나 일부 공고 수만으로 인력시장 규모를 계산하지 않는다.

기업의 실제 도입 성과는 공식 고객 사례와 기업 공시·IR, 가격·제공 조건, 독립 평가로 보강한다.
계획한 기능, 출시된 기능, 회사가 주장한 성과, 독립적으로 확인한 성과를 구분한다.
공개 외주·지원사업은 공고의 기간·대상·자격을 확인한다. 비공개 고객·제안·가격 자료는 공개 목록에 넣지 않는다.

새 질문에 맞는 원출처를 발견하면 정확한 주소, 역할, 제한과 접근 조건을 확인한 뒤 이 목록을 갱신한다.
미확인 채용 API나 피드 주소는 만들어 적지 않는다. 유료·로그인 자료는 실제 접근 가능 범위를 먼저 기록한다.

## 수집기 연결 시 남길 항목

2026-10-10 해커톤 수동 조사에서 공식 행사 규정·주최 회고·정부/대학 공고와 MDN/Node.js/GitHub/모델 개발 문서를 사용했다. 정확한35개 URL, 원문 날짜·수집·검토 범위는 [검토 기록](ai/AI_RESEARCH_REVIEW_LOG.md)과 [조사 문서](AI_HACKATHONS.2026-10-10.md)에 남겼다. `ai-hackathons-2026` 보고서 발행이며 새 수집기나 예약 실행 연결은 아니다. 원문 확보에 실패한 해양과학 후보는 보류했다.

- 안정적인 출처 ID, 찾을 질문·독자, 원문·목록 주소, 공급사·독립 연구·탐색용 등의 역할.
- 확인된 RSS·Atom·API·HTML 경로, 목표 주기, 실제 연결 상태와 검증일.
- 마지막 시도·성공, 확보 범위, 원문·첨부 검토 범위, 오류·제한·다음 확인.
- 원문 발표·수정일 근거와 정밀도, 실제 수집·검토 시각, 중복·변경·과거 판 보존 방법.

위의 문서용 ID는 기존 수집기의 source ID를 임의로 바꾸라는 지시가 아니다.
연결 완료는 원문·날짜 추출, 반복 수집 무변경, 수정 반영, 실패 시 보존을 확인한 뒤 표시한다.
월간 점검에서 범위의 균형과 끊어진 경로를 검토하고 [검토 기록](ai/AI_RESEARCH_REVIEW_LOG.md)에 공백을 남긴다.
