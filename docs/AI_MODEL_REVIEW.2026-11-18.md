# 2026-11-18 모델 소개와 누적 비교표 검토

기존 main과 Editorial을 사용한다. GPT-6.2 Astra·Sol, MAI Code 2·Flash, Cyber 2 Flash, Image 2.7·Flash, Realtime 1의 소개와 기존 Microsoft Decision 소개의 1.1 후속 판을 작성했다. 보고서와 공식 비교 관측을 새 불변 입력 및 두 publication manifest에 함께 등록한다. 다른 작업의 미제출 소스·문서·작성 카탈로그 변경은 제출하지 않는다.

## 원문과 변경 판정

- [GPT-6.2 발표](https://openai.com/index/introducing-gpt-6-2-astra-sol/), 두 API 모델 문서, 이전 모델 문서, [시스템 카드](https://deploymentsafety.openai.com/gpt-6-2-astra-sol)를 읽었다. API ID, 입력·출력 상한, Standard·긴 입력·캐시 쓰기·속도 요금과 구독 접근을 분리한다. 실제 브라우저에서 Agents’ Last Exam v1.1의 Max 점과 과제 비용을 읽었으며 본문의 다른 점수 차이를 이 설정에 대입하지 않았다. MentalHealthBench·PostTrainBench와 장애 보고의 퇴보도 설명한다. 원문 웹 도구와 실제 브라우저 열람은 성공했지만 직접 HTTP 403은 실패로 보존한다.
- [MAI Code 2·Flash](https://microsoft.ai/news/introducing-mai-code-2-and-mai-code-2-flash/)와 v3 모델 카드, [Copilot 단가](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing)를 읽었다. 80B 요약과 77B+3B, 약2.8T 총량을 구분한다. MSBench/Copilot CLI1.0.102·Max·하위 에이전트 비활성·3회 평균과 인프라 실패 포함을 보존한다. SWE Atlas의 Flash 우위, 영어 최적화와 안전 표의 한계도 남겼다. 경쟁 비용 비율은 50% 할인 기준이다. 2027-05-17의 정확한 전환 시각·시간대는 미확인이다. 카드 1·6쪽을 렌더링해 표와 숫자를 시각 대조했다.
- [Cyber 2 Flash](https://microsoft.ai/news/introducing-mai-cyber-2-flash/)는 공식 발표와 실제 제공을 구분한다. 905개 중 겹침92개를 제외한813개 CyberGym-E2E와 추론 예산, 오프라인 단가의 조건을 읽었다. 자격 고객의 보안 제품 교체는12월 중순부터 예정이며 일반 API 제공으로 표시하지 않는다.
- [Image 2.7·Flash](https://microsoft.ai/news/introducing-mai-image-2-7/)는10월27일 평가 공개와11월17일 공개 미리보기를 나눈다. 모델 카드의20B·32K·4,194,304픽셀은 상위 판의 사양이며 Flash에 확인하지 않은 규모·Elo를 복사하지 않는다. 편집1,215 Elo의4점 차이와 생성4위, 약35/10달러·1,000장이라는 근사 비용을 보존한다.
- [Realtime 1](https://microsoft.ai/news/introducing-mai-realtime-1/)의 실제 브라우저 평가 표와 MAI Labs 조건을 읽었다. Big Bench Audio 98.9와 tau-Voice57.5를 분리하고 경쟁 모델보다 낮은 완료율도 담았다. 시간당 정규화 평가 비용1.3548달러, 기본0.01달러/분과 별도 추론1/5달러·100만 토큰은 다른 단위다. 초기 애니메이션의0·중간 숫자를 점수로 사용하지 않았다. 마이크·로그인·음성 전송은 수행하지 않았다.
- [Decision 1.1](https://commandline.microsoft.com/microsoft-decision-model-ga/)의 GA·새 기반·이미지 입력·지역별0.042/0.046/0.05달러 및 출력 무료를 읽었다. 기존 `microsoft-decision-1-model-guide`의 다음 판으로 보존한다. AA지수68을 정답률68%로 바꾸지 않으며9범주 중7범주 선두의 한계와 자유 서술 미지원을 설명한다.

Theo 본문18편과 비교 원본806관측은 이번 수집에서 변경이 없었다. 기존 AI 공식 피드·모델 검색 후보도 갱신하고 신규 발표·재보도·앱 설정을 대조했다. 모든 제공자의 전 출시를 전수 검토한 것은 아니다. 외부 AA 후속 기사 URL의 웹 도구 열람 실패는 독립 검증 성공으로 기록하지 않는다.

## 작성과 보존

비추적 `data/raw/model_maintenance/2026-11-18/`에 획득 성공·실패, 원문 해시와 receipt, 관련 절, PDF와 시각 근거를 보존한다. 실제 브라우저에서 읽은 차트는 해당 선택 설정의 전사 receipt이며 완전한 HTTP 원문으로 표시하지 않는다. 공급자 측정·외부 평가의 공급자 인용과 독립 실행을 구분한다.

이전 공개 recipe의 model_introduction·Editorial 조합을 사용했다. 첫 화면과 본문을 분리해 같은 작성자가 자체 검토했으며 독립 에이전트·사람 독해 합격으로 기록하지 않는다. SDK 실습·가상 업무·응용 문제를 추가하지 않았다. 생성 DB·원문·HTML·PNG는 Git에 제출하지 않는다.

## 검증과 공개 상태

발행 입력의 품질 검사는 통과했다. 제출 소스의 영향 시험, 실제 출력·필터·이전 판·모바일 검사와 Pages·공개 URL 결과는 실제 확인 후 아래에 추가한다. 입력 등록과 source refresh만으로 배포 완료를 선언하지 않는다.


## 공개 완료와 실제 검증

기능 커밋 `de29240c8e6a2bfc364f58155d768cfb29b31bd3`을 origin main에 정상 push했다. [Pages44172745643](https://github.com/Hansihoo/signal-desk/actions/runs/44172745643)가 성공했고, 공개 소개9판과 전체 비교표의83관측이 검토 입력과 정확히 일치한다. 소개8편을 추가하고 기존 Decision을2판으로 갱신했다.

공개 이전의 현재 보고서140편 중 Decision을 제외한139편의 본문 지문이 같다. 보고서288판·모델3017판·Theo자료23판의 원문 지문이 모두 보존됐다. 실제 공개 Decision1판은10월12일의 제목과 Qwen3.5 기반 설명을 유지한다.

실제 Chrome/CUA에서 공개 소개9편의31표, 확인일·분류·전체 비교표 링크를 확인했다. 공개390/1280px에서는 client375/1265px와 문서 폭이 같아 페이지의 가로 넘침이 없다. 표준가·캐시·이미지 장당·음성 분당과 별도 추론·무료 출력0값, 평가판·실제 점수·원문 단위·조건을 공개 전체표에서 읽었다. OpenAI/Microsoft 필터, 원문 출처·최초 저장·원본 값 상세도 확인했다. 공개 모바일 소개와 Astra 평가 상세의 화면 이미지를 실제로 열어 검토했다.

공개 HTTP 검사에서는 소개의 자체·교차 참조 앵커, 비교표·이전 Decision·동반 메뉴583경로를 확인했다. 관련 없는 공통 사이드바540링크의 전수 재감사는 제외했다. 최초 전체 다운로드 검사가 느려 범위를 바로잡았으며, 최종 focused 검사는 exit0으로 완료됐다. 압축 공개 JSON과 원문/검증 receipt는 비추적 raw에 보존한다. 후속 내용 전용 검사는 별도 기록이며 최종 링크 검사와 구분한다.

제출 소스 전체214시험·품질·publish·audit가 통과했다. 로컬 주거 review의 기존 활성 공고0 실패는 모델 기능과 분리하며, 클라우드 Pages의 주거 검토 단계는 성공했다. 독립 모델 실행·실청구·한국어 실제 업무·사람 독해 시험은 하지 않았다. 기본 인증·전역 credential, 다른 미제출 변경과 예약은 바꾸지 않았다. 검증용 탭·viewport를 반환하고 소유 HTTP/검증 프로세스 및 일회성 제출 복사본을 정리했다.
