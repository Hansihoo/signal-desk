# Research delivery research and experience plan

검토일: 2026-10-03. 상태: 조사 완료, 메인과 대표 보고서 두 페이지 시안 구현. 분야 확대·데이터 계약·일정은 후속 검토안.

## User intent and accepted scope

Theo는 여러 분야에서 수집한 정보를 빠르게 선택하고 이해하기를 원한다. 메인에서 각 분야의 최근 핵심 내용을 보고, 한 번 클릭해 정리된 보고서를 읽고, 필요한 경우 공식 자료로 이동한다. 수집량보다 독자가 판단하는 데 걸리는 시간을 줄이는 것이 목표다.

상위 연구 범위는 **개발 관련 정보**다. 개발 수익 기회는 하위 주제다. 기존 첨부 명세는 그 하위 주제의 요구사항으로 보존한다. AI 개발 등 기존 분야와의 분류 관계는 구현 시 정리하되 안정적인 링크와 과거 기록을 보존한다. 주거·뉴스 등 다른 연구 분야도 함께 보이는 메인 구조를 유지한다.

초기에는 기존 자료를 분야별로 정리하고 현재 유효성을 확인한다. 다음 주인 2026-10-05 시작 주부터 개발 정보는 주 1회 신규·변경 내용을 검토하고 의미 있는 내용이 있을 때 반영하는 방향이 합의됐다. 정확한 요일·시각과 긴급 항목의 예외 운영은 아직 정하지 않았다. 기존 배포 워크플로의 일일 주기는 현재 유지되고 있다.

## Research method and evidence limits

실제 리서치 서비스의 공식 도움말, 공개 편집 방법, 기술 평가 체계와 사용자 경험 원칙을 비교했다. 로그인한 유료 제품의 내부 기능을 직접 시험한 결과가 아니다. 서비스 제공자가 설명한 기능과 Signal Desk에 대한 설계 판단을 아래에서 구분한다. 홍보상의 시간 절감·정확도 수치를 성능 근거로 사용하지 않는다.

## Observed delivery patterns

| 사례 | 공식 자료에서 확인한 전달 방식 | Signal Desk에 적용할 설계 판단 |
| --- | --- | --- |
| Feedly Market Intelligence | 개별 기사 요약과 여러 기사를 함께 분석하는 분야별 Overview를 구분한다. Board/Feed에서 뉴스레터 내용을 만들고 편집할 수 있다. [기능 설명](https://docs.feedly.com/article/811-how-to-use-ai-in-automated-newsletter) | 분야 핵심은 관련 자료를 종합해 작성한다. 기사 요약을 여러 개 붙이는 것만으로 분야 분석이 완성되지는 않는다. |
| AlphaSense | 관심 회사·주제·검색의 자료를 위젯으로 모니터링하고, 질문에 대한 분석에는 원문으로 연결되는 인용을 제공한다. [대시보드](https://help.alpha-sense.com/hc/en-us/articles/41809206884243-Leveraging-and-Customizing-Your-Dashboard), [분석과 인용](https://help.alpha-sense.com/hc/en-us/articles/41666587181203-Interacting-with-Generative-Search) | 첫 화면의 브리핑과 상세 보고서를 연결하고, 보고서의 주요 주장 가까이에 공식 근거를 둔다. 많은 위젯보다 독자의 관심과 판단에 맞춘 범위가 우선이다. |
| Axios HQ Smart Brevity | 처음에 새로 알려야 할 사실과 그 사실이 독자에게 중요한 이유를 제시한다. [편집 원칙](https://axioshq.com/insights/two-keys-to-keeping-busy-readers-engaged) | 제목 다음에 변화와 영향을 각각 한 문장으로 적는다. 중요한 이유를 독자가 추측하도록 남겨 두지 않는다. |
| Thoughtworks Technology Radar | 기술을 분류하고 Adopt/Trial/Assess/Caution 단계와 설명을 제공한다. Trial에는 실제 운영 소프트웨어에서 사용한 경험이 필요하다. [공식 FAQ](https://www.thoughtworks.com/radar/faq) | 단순 소개에 적용 맥락과 검토 상태를 보탠다. Signal Desk의 '시험해 볼 만함'은 자체 실사용 검증을 뜻하지 않으며 근거를 별도로 표시한다. 기존 Radar의 등급을 그대로 자동 복제하지 않는다. |
| President's Daily Brief | 주요 현안의 간결한 종합 정보를 명확한 언어로 제공하고 수신자의 선호·피드백에 맞춰 전달한다. [CIA 공개 설명](https://www.cia.gov/legacy/museum/artifact/barack-obamas-presidents-daily-brief-binder/) | 수신자의 관심과 현재 판단 과제를 먼저 정한다. '회장에게 보고하는 비서'라는 사용자의 비유는 독자에 맞춘 선별·맥락·후속 확인으로 구현한다. |

정보를 단계적으로 펼치는 방식은 중요한 내용을 먼저 제시하고 상세 내용을 요청 시 제공하는 원칙과 맞는다. 다만 사이트 내부의 단계가 늘면 탐색 부담이 생긴다. 메인에서 보고서로 직접 이동하게 하고 분야·분류 페이지를 필수 경유지로 만들지 않는 설계를 제안한다. [NN/g Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)

분석의 품질에는 출처의 질, 불확실성, 사실과 분석자의 판단 구분이 포함된다. 이를 보고서의 간결함과 함께 유지한다. 정보기관의 정책 역할을 복제하는 것은 아니며, Signal Desk의 '다음 확인 제안'은 자체 제품 기능이다. [ODNI Analytic Standards](https://www.dni.gov/files/documents/ICD/ICD-203.pdf)

## Recommended product shape

세 화면 역할을 조합한다.

| 역할 | 독자의 질문 | 화면 |
| --- | --- | --- |
| 메인 브리핑 | 이번에 무엇을 먼저 알아야 하는가? | 핵심 변화와 분야별 브리핑을 선별한 대시보드 |
| 한 장 보고서 | 무엇이 바뀌었고, 내 개발에 어떤 의미가 있는가? | 결론·근거·제약·다음 확인을 함께 읽는 문서 |
| 자료실 | 다른 정보나 지난 내용을 찾을 수 있는가? | 분야/분류 트리, 검색, 기본 자료와 과거 보고서 |

주요 동선: **메인 → 보고서 → 공식 자료**. 메인 → 분야 → 분류 → 자료 동선은 추가 탐색용이다. 현재 트리는 자료실 탐색 역할을 맡는다.

Overview는 여러 정보의 관계를 파악하는 요약 역할이고, 보고서는 개별 판단을 설명하는 내용 단위이며, 대시보드는 그 내용을 고르는 화면이다. 별개 대안으로 하나만 선택할 필요가 없다.

## Homepage proposal

1. **이번 주 핵심 변화**: 기간과 한 문장의 전체 상황, 우선 확인할 보고서 최대 3~5개. 유효한 보고서가 적으면 실제 개수만 표시한다.
2. **분야별 브리핑**: 각 분야 이름, 핵심 변화 1개, 의미 1문장, 마지막 성공 검토일. 보고서 제목은 해당 보고서로 직접 연결하고 분야 이름은 분야 페이지로 연결한다.
3. **계속 확인할 항목**: 미해결 주요 변경이나 가까운 마감이 있을 때만 표시한다. 지난주 보고서라도 아직 중요한 항목은 남길 수 있다.
4. **자료실·지난 브리핑**: 전체 검색, 트리, 기본 자료, 날짜별 기록은 별도 영역에서 접근한다.

10개 분야가 있다고 매주 10개 새 보고서를 채우지 않는다. 변화가 없는 분야는 확인일과 '새 변경 없음'만 간결하게 표시한다. 확인 실패 또는 검토 미실행을 '변경 없음'으로 표시해서는 안 된다. 오래된 자료는 발표일·검토일을 보인다.

모든 자료에 큰 카드를 주거나 수집 건수·그래프로 공간을 채우는 것은 우선 구현 범위에 넣지 않는다. 비교·추세·일정을 실제로 더 쉽게 이해하게 만드는 경우에 표나 차트를 사용한다.

메인 항목의 공통 문법:

- 제목: 알려야 할 사실이나 변화.
- 변화: 이전 상태에서 무엇이 달라졌는지 한 문장.
- 의미: 적용 대상에게 어떤 선택·작업이 영향을 받는지 한 문장.
- 표시: 우선 확인 수준, 신규/수정 여부, 검토일. 실제 자료에 필요한 표시만 노출한다.
- 동작: 보고서 읽기.

## One-page report proposal

한 장은 한 화면 높이를 강제한다는 뜻이 아니라 **한 주제를 한 웹 문서에서 판단할 수 있다**는 뜻이다. 모바일에서는 자연스럽게 스크롤한다. 필수 판단 내용을 접힌 영역에 숨기지 않는다.

| 순서 | 내용 | 작성 기준 |
| --- | --- | --- |
| 1 | 핵심 판단 | 읽고 나서 무엇을 알아야 하는지 1~2문장. 아직 판단할 수 없으면 부족한 근거를 명시. |
| 2 | 무엇인가 / 무엇이 바뀌었나 | 기본 자료는 용도·대상을 설명하고 변경 보고서는 이전/현재 차이를 설명. |
| 3 | 왜 중요한가 / 누구에게 해당하나 | 실제 개발 상황과 비용·호환성·작업 방식 등의 영향. 직접 관련 없는 경우도 구분. |
| 4 | 핵심 근거 | 필요한 사실·수치·비교를 짧은 문장이나 표로 표시. 주요 주장 가까이에 근거 링크. |
| 5 | 제약과 불확실성 | 공식 발표의 주장, 독립 검증, 자체 확인을 구분. 빠진 정보와 상반된 근거가 결론에 미치는 영향. |
| 6 | 다음 확인 | 관련 문서를 읽기, 작은 시험을 하기, 업데이트를 지켜보기 등 근거에 맞는 제안. 행동이 필요 없을 수도 있음. |
| 7 | 공식 자료 / 확인 이력 | 문서·릴리스·정책·신청 링크를 목적별로 구분하고 발표일·검토일·수정 내용을 보존. |

보상·마감 필드는 기회 주제에만 필요하다. 도구 비교에는 비교표, 구현 자료에는 사용 조건, 업데이트에는 변경점이 들어간다. 공통 보고서 뼈대에 분야별 필드를 붙이고 모든 분야를 기회 양식에 맞추지 않는다.

외부 문서의 특정 절로 직접 연결할 수 있으면 해당 링크를 사용한다. 그럴 수 없으면 어떤 절·내용을 확인할지 적는다. 다른 사이트의 본문 강조 기능을 보장하지 않는다.

## Editorial and storage model proposal

수집 자료와 발행 보고서를 별도 단위로 다룬다. 하나의 이슈에 여러 출처가 연결될 수 있고 하나의 보고서는 그 이슈에 대한 종합 설명이다. 기사 URL마다 새 보고서를 자동 생성하는 방식은 메인에 그대로 적용하지 않는다.

작업 흐름: 공개 자료 수집 → 동일 이슈 묶기 → 이전 상태와 변경 비교 → 근거 정리 → 중요성 판단 → 보고서 검토 → 메인 선별.

- 중요성: 독자의 관심·적용 가능성·영향·시급성·근거 수준을 함께 검토한다. 최신 날짜나 인기만으로 정렬하지 않는다.
- 판단 표시: '지금 확인 / 이번 주 검토 / 참고'처럼 우선순위를 표현한다. 적용 추천의 근거와 검증 상태는 별도로 기록한다.
- 기본 자료와 변경 보고서: 기본 자료는 계속 찾아볼 페이지로 유지하고, 변경 보고서는 바뀐 내용과 기존 페이지를 연결한다.
- 안정적인 이슈/보고서 ID, 연결된 출처, 주장별 근거, 검토일, 변경 이력, 선별 이유를 저장할 계약이 필요하다. 정확한 DB 스키마는 다음 구현 설계에서 정한다.
- 기존 SQLite·원본 보관·정적 HTML 생성 원칙을 유지한다. 공개 브리핑에는 공개 자료만 사용한다.
- 주간 발행본은 당시 검토된 보고서 버전을 참조해야 한다. 현재 페이지가 수정되어도 과거 판단을 소급 변경하지 않는다. 전체 자료를 매번 복사하는 보관 비용도 함께 검토한다.
- GitHub Pages는 결과를 전달하는 역할을 유지한다. 근거를 읽고 분석·검토하는 실행 단계는 별도 작업이다. 화면 개선만으로 분석이 자동 완성되지는 않는다. 유료 모델/API 선택은 이번 계획에서 확정하지 않는다.

## Initial population and weekly operation

### Initial phase

기존 후보 자료를 전부 같은 비중으로 게시하기보다 분야별 기본 자료와 중요한 현재 이슈를 우선 정리한다. 대표 분야 3개에서 기본 안내·변경 분석·비교 보고서를 하나씩 작성해 템플릿을 시험한다. 실제 출처를 읽고 확인한 내용으로 채운다. 자료가 없으면 대기 상태를 유지하고 예시 데이터를 실제 수집 결과로 표시하지 않는다.

### Weekly review, beginning the week of 2026-10-05

검토할 출처 목록과 범위를 먼저 정한다. 신규 자료와 중요한 내용 변경을 비교한 뒤 기존 문서를 수정하거나 새 보고서를 발행한다. 의미 있는 변경이 없으면 새 발행본을 만들지 않고 내부 검토 결과를 보존한다. 정확한 요일·시각과 긴급 보안/짧은 마감의 예외는 후속 운영 결정이다. 다른 연구 분야의 기존 수집 주기는 별도 결정 없이 변경하지 않는다.

## Implementation phases and acceptance

| 단계 | 산출물 | 완료 기준 |
| --- | --- | --- |
| 1. 내용 계약 | 대표 보고서 3개와 주장별 근거 | 결론·대상·근거·제약·후속 확인이 채워지고 사실/판단 구분. |
| 2. 두 화면 시안 | 메인 브리핑과 한 장 보고서 | 메인에서 분류 페이지를 거치지 않고 보고서로 이동. 공식 근거까지 통상 두 번의 링크 이동. 트리는 선택 탐색용으로 접근. |
| 3. 저장·선별 연결 | 이슈/보고서/출처 연결과 버전 보존 | 중복 이슈, 신규/수정 구분, 지난 보고서 근거 보존, 빈 분야·실패 상태 확인. |
| 4. 주간 검토 운영 | 출처 검토 기록과 변경 시 발행 | 변경 없음·변경 있음·수집 실패를 구분하고 일정이 운영 설정과 일치. |

시안의 사용성 목표는 메인에서 약 30초 안에 먼저 읽을 항목을 고르고, 보고서에서 약 3분 안에 핵심과 다음 확인을 설명할 수 있는 것이다. 이는 검증할 목표이며 입증된 성과가 아니다. 계정·분석 추적 없이 Theo의 실제 탐색 과제로 확인한다. 키보드·모바일 430px·공식 링크·기존 보관 페이지 회귀도 확인한다.

현재 `review`는 데이터·출력의 운영 품질 검사다. 근거가 결론을 뒷받침하는지 검토하는 편집 검증은 추가로 필요하다.

## Current implementation gap

현재는 전체 자료 목록·분야/분류 트리·개별 출처 기록·보고서 양식이 있다. 개발 수익 기회 분야는 HTML 틀이며 실제 수집은 없다. 기존 개별 출처 기록의 해석·검토 및 결론은 작성 대기다. 자동 핵심 선별, 여러 자료의 종합 분석, 일반화된 주장별 근거 저장, 주간 변경 시 발행은 아직 구현되지 않았다.

후속 사용자 요청에 따라 메인과 대표 보고서 한 편만 `/preview/`에 시안으로 구현했다. 보고서는 제목·주제→개요식 요약→시각 데이터→결과→참고내용 순서다. [템플릿 계약](BRIEFING_TEMPLATE.md)을 참고한다. 다른 분야의 상세 보고서나 수집·보관·일정으로 확대하지 않았다.

## Reader-facing revision of the two-page pair

On 2026-10-03 Theo rejected implementation/tutorial language on the preview pages.
The actual Stanford AI Index 2026 takeaway publication and Thoughtworks Radar Vol.34
were examined. Subject-led titles, outline copy, a proportionate evidence chart,
and concise references replace prototype labels and reading instructions. This
changes only the homepage and one report; see BRIEFING_TEMPLATE.md for the revised
contract. Other topic views and the weekly editorial automation remain deferred.

## Initial researched content, 2026-10-04

The latest request authorizes collection and HTML. The same report contract now
serves ten reviewed development subjects from 21 official/first-party URLs. The
curated main leads directly to stable report pages, which lead to official evidence.
Current SQLite documents, immutable revisions and once-only reviewed batches preserve
the data independently of design. Numeric comparisons and sourced condition tables
replace empty placeholders in these reports. The legacy feed/topic outlines remain;
automatic synthesis and weekly change-only review are still pending. See
[RESEARCH_DATA.md](RESEARCH_DATA.md) for the implemented contract and evidence limits.
