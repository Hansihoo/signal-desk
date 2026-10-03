나는 **AI/소프트웨어 1인 개발자가 실제로 돈을 벌 수 있는 기회 정보를 자동으로 수집·정리·시각화하는 웹사이트**를 만들고 싶다.

단순한 AI 뉴스 사이트가 아니라, 사용자가 보고 바로 다음 행동을 할 수 있는 **실행형 Opportunity Dashboard**가 목적이다.

## 1. 핵심 목표

매일 한국시간 기준으로 최신 정보를 수집해서 아래와 같은 실제 실행 가능한 기회만 보여주는 사이트를 만들어라.

수집 대상:

- AI / 개발 해커톤
- 개발 공모전
- 상금형 챌린지
- Bug Bounty
- Security / AI Safety Vulnerability Reward Program
- OSS Patch Reward
- 정부 / 기업 개발자 지원금
- Grant 프로그램
- Developer Program
- API / AI Agent / MCP / AI Platform 수익화 프로그램
- App Marketplace / Plugin Marketplace / Developer Marketplace
- AI 관련 프리랜스 개발 수요
- 1인 개발자 / Micro SaaS 실제 수익 사례
- 새롭게 생긴 개발자용 판매 / 배포 채널
- C++, Native, 보안, 개발자도구, Spreadsheet, Document Processing, 자동화와 연결되는 기회

중요한 것은 **“뉴스”가 아니라 “지금 내가 실제로 참여할 수 있는 기회”**이다.

---

## 2. 사이트에서 가장 중요하게 보는 데이터

각 Opportunity는 최소한 아래 필드를 가져야 한다.

```text
id
title
category
organization
status
description

reward_type
reward_amount_original
reward_currency
total_prize
max_individual_reward

deadline
deadline_timezone
days_remaining

eligibility
country_restrictions

official_url
apply_url
rules_url
submission_url
documentation_url

source_type
source_url
verified_at

is_verified
is_self_reported

created_at
updated_at
```

금액은 반드시 의미를 구분한다.

예:

```text
개인 최대 보상
총상금
지원한도
기본 보상
공식 지급액
MRR
ARR
창업자 자가보고
```

`총상금 $100K`와 `개인이 $100K를 받을 수 있음`을 같은 의미로 처리하면 안 된다.

---

## 3. 정보 수집 정책

공식 출처를 최우선으로 한다.

우선순위:

1. 공식 프로그램 페이지
2. 공식 documentation
3. 공식 GitHub
4. Devpost / Kaggle 등 실제 참가 플랫폼
5. 기업 공식 블로그
6. 신뢰할 수 있는 언론
7. 창업자 인터뷰 / Indie Hackers 등
8. 기타 커뮤니티

검색 결과 기사만 수집하지 말고 가능한 경우 항상 **실제 신청 페이지 / submission page / rules page**까지 찾아라.

예:

```text
Microsoft Bug Bounty
→ 뉴스 기사 X
→ MSRC Bounty Program
→ Scope
→ Submission Form
```

처럼 최종 실행 링크까지 가져와야 한다.

---

## 4. 필터링 규칙

다음 정보는 기본적으로 노출하지 않는다.

- 이미 마감된 해커톤
- 종료된 지원사업
- 신청이 불가능한 프로그램
- 공식 링크가 사라진 프로그램
- 단순 AI 뉴스
- 투자 뉴스
- 제품 출시 뉴스
- 확인되지 않은 SNS 정보
- 출처 없는 수익 인증

단, 과거 사례는 아래 목적에 한해서 별도 Case Study로 보관할 수 있다.

```text
실제 1인 개발자가 무엇을 만들었는가
얼마를 벌었다고 공개했는가
수익 모델은 무엇인가
고객은 어디서 확보했는가
가격 정책은 무엇인가
어떤 distribution channel을 사용했는가
```

이 경우 반드시 다음을 구분한다.

```text
VERIFIED
OFFICIAL
MEDIA REPORTED
SELF REPORTED
UNVERIFIED
```

---

## 5. 중복 제거

같은 Opportunity를 여러 사이트에서 발견해도 하나로 통합한다.

예:

```text
Microsoft Bug Bounty
Microsoft Security Bounty
MSRC Bounty Program
```

을 서로 다른 항목으로 만들지 않는다.

가능하면 다음 기준으로 deduplication 한다.

```text
organization
canonical title
official URL
program ID
```

그리고 기존 항목의:

```text
deadline
reward
scope
rules
status
```

가 변경됐을 때만 업데이트 이벤트를 기록한다.

---

## 6. 상태 관리

각 Opportunity는 다음 상태 중 하나를 가진다.

```text
OPEN
ALWAYS_OPEN
DEADLINE_SOON
CLOSED
UNKNOWN
```

DEADLINE_SOON 기준은 기본 14일 이내로 한다.

사이트 기본 화면에서는:

```text
OPEN
ALWAYS_OPEN
DEADLINE_SOON
```

만 노출한다.

CLOSED 항목은 Archive로 이동한다.

---

## 7. 사이트 화면

메인 화면은 뉴스 사이트보다 **Developer Opportunity Dashboard** 형태로 만든다.

첫 화면에 바로 보여야 하는 정보:

```text
현재 실행 가능 기회 수
14일 이내 마감 수
상시 프로그램 수
오늘 새로 발견된 기회 수
오늘 변경된 기회 수
```

그 아래 핵심 Opportunity Card를 보여준다.

카드 예:

```text
Google AI VRP

AI Security
ALWAYS OPEN

개인 최대
$30,000

[공식 프로그램]
[Scope]
[제보하기]
```

주관적인:

```text
추천
비추천
좋음
별점
성공 가능성
```

같은 데이터는 만들지 않는다.

객관적인 데이터만 제공한다.

---

## 8. 상세 페이지

각 Opportunity 상세 화면은 다음 순서를 따른다.

### 주제 / 핵심

프로그램명  
운영 회사  
상태  
보상  
마감  
직접 실행 버튼

### 요약

개요식으로:

```text
무엇인가
누가 가능한가
무엇을 제출하는가
얼마를 받을 수 있는가
언제까지인가
```

### 데이터

구조화된 테이블 제공.

```text
Reward
Deadline
Eligibility
Country
Submission
Scope
Rules
```

### 결과 / Action

실제로 사용자가 바로 할 수 있는 Action을 보여준다.

예:

```text
[공식 규칙 열기]
[계정 생성]
[Scope 확인]
[Submission Form]
[SDK Documentation]
[참가 신청]
```

### 참고자료

정보 출처와 마지막 검증일을 보여준다.

---

## 9. Dashboard 시각화

장식용 차트보다 의미 있는 데이터를 보여준다.

필요한 시각화:

```text
마감일까지 남은 기간
카테고리별 열린 기회 수
Reward range
신규 Opportunity 수
변경된 Opportunity 수
상시 / 기한형 비율
```

임의의 scoring은 만들지 않는다.

---

## 10. 검색 / 필터

최소 다음 필터를 지원한다.

```text
Category
Status
Organization
Reward Type
Minimum Reward
Deadline
Country
Source Type
```

추가로:

```text
C++
Security
AI
Agent
MCP
Native
Spreadsheet
Document
Automation
Developer Tool
```

같은 기술 태그 필터가 필요하다.

---

## 11. 데이터 수집 구조

수집 시스템과 사이트를 분리해서 설계한다.

예:

```text
Collectors
    ↓
Normalizer
    ↓
Verifier
    ↓
Deduplicator
    ↓
Database
    ↓
API
    ↓
Dashboard
```

Collector는 source별 adapter 형태로 만든다.

예:

```text
DevpostCollector
KaggleCollector
MicrosoftBountyCollector
GoogleBugHunterCollector
OpenAIBountyCollector
GitHubCollector
GovernmentProgramCollector
```

Collector가 실패해도 전체 수집이 멈추지 않도록 한다.

---

## 12. AI 사용 방식

LLM은 다음 용도로 사용한다.

```text
제목 normalize
설명 요약
카테고리 분류
tag 추출
eligibility 요약
reward type 분류
중복 후보 탐색
```

하지만 아래 데이터는 LLM이 만들어내면 안 된다.

```text
reward amount
deadline
URL
country restriction
official status
```

이 데이터는 원문에서 직접 추출해야 한다.

확인할 수 없으면 NULL 또는 UNKNOWN으로 저장한다.

절대 추측하지 않는다.

---

## 13. 검증 시스템

각 Opportunity에는:

```text
last_verified_at
verification_status
```

가 있어야 한다.

주기적으로 원본 페이지를 다시 확인해서:

```text
페이지 존재 여부
deadline 변경
reward 변경
status 변경
apply link 변경
```

을 감지한다.

중요 변경 발생 시 Change Log를 남긴다.

---

## 14. 자동 실행

한국시간 기준 매일 정기적으로 데이터를 갱신한다.

기본:

```text
매일 19:00 수집
매일 19:30 검증 / dedup
매일 20:00 Daily Report 생성
```

Daily Report에는:

```text
새로운 Opportunity
상태 변경 Opportunity
마감 임박
새로운 수익 사례
```

만 포함한다.

어제와 동일한 내용은 반복하지 않는다.

---

## 15. Daily Report

매일 `/reports/YYYY-MM-DD` 페이지를 생성한다.

구조:

```text
주제 / 핵심
↓
요약
↓
데이터
↓
결과
↓
참고자료
```

또한 HTML 다운로드 기능도 제공한다.

예:

```text
Download HTML
```

PDF는 이후 추가할 수 있도록 구조만 고려한다.

---

## 16. 기술 방향

기술 스택은 네가 현재 환경을 확인한 뒤 결정하되 다음 조건을 만족해야 한다.

- 유지보수하기 쉬울 것
- 1인 개발 프로젝트에 적합할 것
- 배포가 쉬울 것
- DB migration이 쉬울 것
- scheduler / cron 실행 가능할 것
- scraping / API collector를 추가하기 쉬울 것
- 비용을 최대한 낮게 유지할 것

프론트엔드는 SEO와 server rendering을 고려한다.

배포 환경은 가능하면 현재 프로젝트 구조를 보고 적절한 방식을 선택한다.

---

## 17. 첫 번째 구현 범위

처음부터 모든 사이트를 수집하려 하지 않는다.

MVP에서는 아래 소스부터 구현한다.

```text
Microsoft Security Response Center
Google Bug Hunters
OpenAI / Bugcrowd
Devpost
Kaggle
GitHub
```

먼저 이 소스들만으로 완전히 동작하는 시스템을 만든다.

그 다음 확장 가능하게 구조를 만든다.

---

## 18. 초기 Seed 데이터

첫 구현에서는 최소 아래 프로그램을 실제 데이터로 넣고 수집/검증 흐름이 동작하는지 확인한다.

```text
Microsoft Bug Bounty
Google AI VRP
Google Chrome VRP
Google OSS Patch Rewards
OpenAI Security Bug Bounty
OpenAI Safety Bug Bounty
```

이 데이터는 hard-code하는 것이 아니라 가능한 경우 실제 source에서 가져오도록 한다.

---

## 19. 구현 진행 방식

먼저 현재 repository를 분석하라.

그 후:

```text
1. Architecture 제안
2. DB schema
3. collector interface
4. 첫 source collector
5. normalization / dedup
6. API
7. dashboard
8. opportunity detail
9. scheduler
10. daily report
11. deployment
```

순서로 구현한다.

중간마다 내가 승인하도록 멈추지 말고 합리적인 판단을 내려 계속 구현하라.

모호한 부분은 MVP에 적합한 방향으로 결정한다.

---

## 20. 최종적으로 원하는 상태

배포된 사이트에서 매일 들어가면:

```text
오늘 새로 생긴 돈 벌 수 있는 개발 기회는 무엇인가?
지금 신청할 수 있는 것은 무엇인가?
얼마를 받을 수 있는가?
마감은 언제인가?
나는 어디를 클릭하면 바로 시작할 수 있는가?
```

를 1~2분 안에 파악할 수 있어야 한다.

이 프로젝트의 핵심은 AI 뉴스 수집기가 아니라:

**"1인 개발자를 위한 실시간 개발 수익 기회 데이터베이스 + 실행 대시보드"**

이다.