# 전체 원고의 독자 중심 다듬기 — 2026-10-09

## 범위와 보존

사용자는 음성 보고서의 보강 방식을 전체에 적용하라고 요청했다. 현재 작성 보고서와 모델 해설 34편을 모두 읽고, 메인에 표시되는 제목·소개·요약과 각 본문의 설명을 다듬는다. 새 수집 자동화나 디자인 개편은 포함하지 않는다. 모델 원문 14문서와 이전 88판, 기존 ID·순서·원문의 날짜·조건을 보존한다. 새 판은 `config/reader_refinement.2026-10-09.json`에 만들며 적용 후 덮어쓰지 않는다.

## 수정 원칙

- 소개는 ‘이 글에서 확인한다’는 목차 설명 대신 실제로 알아야 할 내용을 담는다.
- 용어는 역할과 사례 안에서 정의한다. 모델·제품·연결 규칙·추론 설정을 같은 축으로 섞지 않는다.
- 주 사례의 입력·중간 값·기대 결과를 유지한다. 값이 다른 계산은 별도 가정임을 밝힌다.
- 점수의 분모·평가판·과제당 비용·구독 환산의 조건을 적는다. 가정과 관측을 구분한다.
- 현재 지원 여부를 확인하지 않은 설정 안내를 실행 튜토리얼로 제시하지 않는다.

## 독자 질문과 변경 범위

| 글 ID | 읽은 뒤 답할 질문 | 주요 변경 필드 |
| --- | --- | --- |
| a2a-cli-agent-connections | 외부 AI에 맡긴 일이 실제로 끝났는지 어떻게 알 수 있는가? | deck, description, explanation, highlights, summary, tables, title |
| agent-evaluation-checklist | AI가 그럴듯한 답을 한 것과 실제 업무를 성공한 것을 어떻게 구분하는가? | deck, description, explanation, highlights, summary, title |
| document-rag-grounding | 내 자료의 현재 조건을 근거로 답하게 하려면 무엇을 준비하고 어디를 고쳐야 하는가? | deck, description, explanation, highlights, summary, title |
| hackathon-tech-roadmap | AI 해커톤에 앞서 어떤 기능부터 배우고 무엇을 완성해야 하는가? | deck, description, explanation, highlights, summary, title |
| llm-model-comparison | 공개 모델 순위를 실제 업무의 모델 선택에 어떻게 사용해야 하는가? | deck, description, explanation, highlights, learning, summary, title |
| mcp-apps-workflows | AI가 찾은 목록을 직접 고르고 같은 자료로 질문을 이어가려면 무엇을 연결해야 하는가? | deck, description, explanation, highlights, summary, title |
| openai-api-migration | 종료되는 서비스가 내 코드의 어디에 영향을 주며 무엇을 시험한 뒤 교체해야 하는가? | deck, description, explanation, highlights, learning, references, source_note, summary, title |
| voice-agent-architectures | 기존 텍스트 앱에서 음성 입력·답변·조건 변경을 어디까지 구현해야 하는가? | explanation |
| aws-activate-credits | 내 기업은 어느 경로로 신청하며 크레딧이 실제 청구액을 얼마나 줄이는가? | deck, description, explanation, learning, result, title |
| aws-partner-hackathon | 누가 참가할 수 있으며 AI 메시징 작품에서 무엇을 실제로 보여줘야 하는가? | deck, description, explanation, highlights, summary, title |
| github-marketplace-paid-apps | PR 앱의 설치와 결제를 어떤 데이터로 연결해야 유료 기능을 정확히 제공하는가? | deck, description, explanation, highlights, summary, title |
| github-pages-storage | 발행 주기·첨부·이전 판을 고려하면 무료 사이트에 얼마나 오래 쌓을 수 있는가? | deck, description, explanation, title |
| google-oss-reward-status | 코드 기여가 어느 보상 프로그램에 해당하며 현재 신청할 수 있는가? | deck, description, explanation, title |
| nlnet-restack-call | 내 개발 아이디어가 지원 범위에 맞으며 검증 가능한 제안을 어떻게 구성하는가? | deck, description, explanation, highlights, summary, title |
| openai-safety-bounty | 답변 품질 문제와 실제 권한 침범을 어떻게 구분하고 어떤 증거를 제출하는가? | deck, description, explanation, highlights, summary, title |
| tally-small-saas-case | 공개된 SaaS 성장 사례에서 실제 매출·유료 기능·실험 가설을 어떻게 구분하는가? | deck, description, explanation, learning, title |
| upwork-ai-integration-demand | AI 연동 수요 자료가 보여주는 것은 무엇이며 고객에게 실제로 무엇을 납품해야 하는가? | deck, description, explanation, highlights, summary, title |
| office-business-directions | 문서 AI 제품이 실제 업무의 어느 단계를 맡고 남은 연결은 무엇인가? | deck, description, explanation, title |
| polaris-government-opportunities | 문서 AI 기술을 정부 제조 과제로 제안하려면 어떤 자격·협력·개발 성과가 필요한가? | deck, description, explanation, highlights, summary, title |
| polaris-sales-opportunities | 문서 AI가 고객 업무에 쓸 만한지 어떤 결과와 비용으로 판단해야 하는가? | deck, description, explanation, highlights, summary, title |
| model-reading-claude-opus-5-5-model-guide | Cursor High와 xHigh를 고를 때 어떤 근거가 필요한가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-codex-6-model-guide | 기본 설정으로 xHigh를 쓰라는 추천이 Max 점수로 증명되는가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-codex-claude-200usd-capacity-report | 월 $200이면 어느 서비스에서 더 많은 일을 할 수 있는가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-codex-model-comparison | 비용 배수 25.8이면 25.8달러라는 뜻인가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-codex-model-guide-20260909 | Luna의 두 점수가 다르면 저장소에서 길 찾기가 약하다고 결론 내려도 되는가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-coding-agent-index | v1.3보다 새 판의 점수가 낮으면 모델이 퇴보한 것인가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-coding-agent-index-v1-4 | 표의 비용 효율 표시와 차트의 상위 15개는 같은 후보들인가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-gemini-4-argon-model-guide | 할인 때 싼 평가 비용이면 앞으로도 같은 가격으로 쓸 수 있는가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-gpt-6-1-sol-model-guide | 종합 지표 51로 같으면 두 모델을 같은 용도로 써도 될까? | deck, description, explanation, highlights, result, summary, title |
| model-reading-grok-4-7-report | 표에 $3.74·$6.01·$8.82가 있으면 가장 싼 경로를 고르면 되는가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-llm-coding-benchmark-reference-company-v6 | SWE-Atlas와 Atlas QnA 열은 동일한 시험인가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-llm-models | 8B·Q4이면 메모리 4GB만 있으면 충분한가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-model-cost-performance | Token cost 열이 낮으면 API 청구도 낮은가? | deck, description, explanation, highlights, result, summary, title |
| model-reading-windows-codex-max-guide | 화면에 Max가 보이면 모델이 실제 Max로 실행된 것인가? | deck, description, explanation, highlights, result, summary, title |

## 실제로 발견해 수정한 결함

평가 글의 상태 정확도 84%와 답·상태 모두 정답인 80%를 혼합한 문장을 바로잡았다. RAG에서는 소득 지수 110인 신청자를 ‘110 이하’라는 다른 조건으로 바꾼 해석 사례를 고쳤다. 해커톤 글은 로컬 조회·도구 왕복의 학습 계획과 실제 SDK 실행 범위를 구분했다. API 이전은 분류 지시가 없는 요청에서 category JSON을 기대하던 생략을 없앴다.

AWS·Tally의 별도 계산 가정을 표시했고, AWS 서비스료 합계를 앱 전체 운영비로 확대하지 않도록 했다. Marketplace 설치·구매·저장소의 관계와 PR·workflow의 뜻, Pages 표본 20편의 가정, 비공개 OSS 등급의 미확인 상태를 설명했다. 일반 AI바우처와 별도 제조 AX 공고의 역할·자격을 섞은 초안도 독립 검토 후 수정했다.

모델 해설은 반복 결론을 주제별 판단으로 바꿨다. $2,155×4.348의 외삽, Argon $1.99×2의 조건, 필터와 Index 산식의 구분, 종합 점수 동점의 한계, 가중치와 전체 실행 메모리의 차이를 직접 설명했다. 원문 비용 툴팁의 집계 단위를 유지한다.

## 근거와 날짜

기준본은 공개 source66b3c8b의 현재 34편·88판·원문14문서를 실제 확보한 `all-refinement-before.public.json`이다. 원문별 기존 수집·확인일은 글을 다시 썼다는 이유로 올리지 않는다. 모델 비용 단위는 이 기준본에 들어 있는 원문 HTML의 열 머리글·툴팁을 읽은 범위다. 현재 상품 조건을 새로 전수 조회한 것이 아니다.

추가로 OpenAI Docs MCP에서 종료 공지·Realtime 가이드·gpt-realtime-2.1-mini 모델 페이지를 실제 확보했다. 확인 범위는 deprecated/legacy의 뜻과 tts-1 권장 대체의 Realtime 접점이다. 보존 경로·확보 시각은 `data/raw/research_teaching_2026_10_09/all-refinement-openai-acquisition.json`에 있다. 기존 speech 요청의 단순 모델 문자열 변경과 세션 연결 변경을 구분한다. 실제 API 호출은 하지 않았다.

## 검토 상태와 한계

초기 진단은 기술8편·사업12편·모델14편을 서로 다른 에이전트가 전체 읽었다. 변경 뒤에도 각 담당자가 실제 수정 원고를 다시 읽었으며 최종 기술8·사업12·모델14 모두 필수 수정 0건이다. 기술의 이전 지적27건 중24건은 해소됐고 사례 전환·선택 심화 용어·반복 표현3건은 비차단 편집 의견으로 남겼다. 최종 파일 bytes SHA256은 `13a9e0271c78a43e9d5bb5cb265051f7aaa6850c656fb0a9fff2fbd314f9364c`다. 편별 정규화 JSON 지문도 최종 입력과 대조했다.

별도의 새 에이전트는 본문과 이전 판정을 받지 않고34편의 첫 화면만 읽었다. 실제 지적을 수정한 결과는 19 Pass/15 Revise →25/9 →33/1 →34/0이다. 마지막 첫 화면 입력 지문은 `deb87670a2095dfbd1e83598d2c8fdfe5e468586238eb0ec292992d83ae84d51`다. 이는 최소한 주제와 정보가 읽힌다는 에이전트 판정이며, 본문 검토와 합쳐 사람의 학습 승인으로 해석하지 않는다.

| 독립 검토 기록 | 실제 확인 범위 | 최종 기록 SHA256 |
| --- | --- | --- |
| all-refinement-technology-final-review.json | 기술8편 전체 본문·27지적 대조·로컬 개념 예시 일부·제공 공식3문서 특정 절 | 35f68d81a7f26d3d9b583d02aec1468109e3fb69ca5b2455df617557abde1d08 |
| all-refinement-opportunity-final-review.json | 사업·지원·기회12편 전체 원고·선정 조건과 가상 값·첫 화면 재독 | 9cde7fe761551137bf7ca29bc8a7afe74d32b95384974fb5608aa46f519ff121 |
| all-refinement-model-final-review.json | 모델14해설 전체 원고·원문 비용 단위·근거 문장31개와 입력 지문 | 8138e77b29410d2045ed9dc14ce76d9b1b62b1f191381d019525053bfe42b43e |
| all-refinement-first-screen-review.json | 제목·소개·요약·핵심·범위만 실제 읽고 변경한 첫 화면 재독 | 최신 입력 지문은 위에 기록 |

기록은 등록된 `reports/research-teaching-2026-10-09/` 보존 root에 있다. 실제 초보 사람의 학습 시험, 유료 API·SDK 실행, 제품 구매, 취약점 공격·보상 신청, 정부 자격 확정·제출은 수행하지 않았다. 에이전트 Pass와 출력 검사는 사용자 이해 승인을 뜻하지 않는다.

## 로컬 발행·출력 검증

- 새 불변 배치 `reader-refinement-2026-10-09`를 적용했다. 정규화 보고서 배열 지문은 `24538da0d11c90f3b40d3961c15761deeaf6134065cad6881b3f3ab6927ec70f`이며 파일 bytes 지문과 구분한다. 현재34편/전체122판이고 기존88문서·모델14원문·ID/순서를 보존했다.
- 기존 전체109시험과 새 배치 적용 뒤 발행5시험을 통과했다. 현재34편은 입력과 정확히 같고 주 설명이 모두 이전 판과 다르다. 로컬 문서 링크40건, HTML195개/내부 참조9676건 오류0을 확인했다.
- brief·summary desk·review 명령을 실행하고 기존 주택 요약·통합 PNG를 육안 확인했다. 저장된 기존 데이터의 회귀 검사이며 새 주택 공고 수집을 뜻하지 않는다.
- 앱 내부 브라우저의 신뢰된 연결을 사용할 수 없어 별도 Playwright/Edge로 화면을 검사했다. 초기253개 기능/폭 검사는 통과했지만 브라우저의 자동 `/favicon.ico` 요청404 때문에 전체 결과가 실패했다. 별도 재현으로 정확한 경로를 확인했고 본문 오류와 구분해 기록했다. 본문/기능 오류를 무시한 것이 아니다. 초기 실패 receipt도 보존한다.
- 모바일 메인·MCP·음성·RAG 검색 설명·Argon 비용·문서 AI 도입 화면 PNG를 읽고 문장/표/코드 표시를 확인했다. 전체34편·원문14페이지 해설·이전 음성판의 실제1280/390/320px 최종253개 검사를 통과했다. 본문 콘솔 오류0이며 관측한 선택적 아이콘404 한 건은 별도 배열에 남겼다. 공개 배포는 아래에 후속 기록한다.

공개 배포와 정확한 공개 데이터·화면 검증은 진행 중이다.
