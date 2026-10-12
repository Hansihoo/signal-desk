# DevOps 가격 정렬 실습

DevOps r13의 학습용 코드다. `src`의 입력 규칙과 API → 12개 테스트 →
버전별 `.pyz` 파일 → 실제 HTTP smoke → 교체와 복구를 연결한다.
Python 기본 HTTP 서버는 로컬에서만 실행하며 실제 운영용 서버가 아니다.

이 폴더에서 PowerShell로 실행한다. 외부 패키지를 설치하지 않는다.

```powershell
python --version
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
python build.py v1
python smoke.py dist/v1.pyz
python dist/v1.pyz --port 8001
```

두 번째 PowerShell에서 상태와 사용자 요청을 확인한다.

```powershell
Invoke-RestMethod http://127.0.0.1:8001/health
$body = '{"products":[{"id":"a","price":10},{"id":"b","price":2},{"id":"c","price":1}]}'
$result = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8001/sort -ContentType "application/json" -Body $body
$result.version
$result.products
```

기대 결과는 버전 `v1`, 순서 `c, b, a`다. 첫 창에서 Ctrl+C로 종료한다.
`build.py v2`와 `smoke.py dist/v2.pyz`를 실행하고, v2를 8001에서 실행해
두 번째 창의 요청을 반복한다. v2를 종료하고 **저장한 v1 파일**을 다시 실행하면
버전이 v1로 돌아온다. 두 버전은 표기만 바꾼 교체 연습이며 정지 시간이 있다.
동일 버전 파일은 덮어쓰지 않으며 새 결과가 필요하면 새 버전명을 사용한다.

`ci.example.yml`은 별도 학습용 저장소의 `.github/workflows/ci.yml`로 사용할
설정 예시다. 이 저장소의 실제 CI로 등록하지 않는다. 원격 CI와 운영 서버 배포는
실행하지 않았다. 실제 환경의 권한·비밀 값·트래픽 전환·DB 호환성은 별도 구현한다.

2026-10-12 Windows/Python 3.8.5에서 정상12개/의도적 정렬 오류/복원,
v1→v2→같은 v1 파일의 HTTP 요청, 지문 불일치·버전 덮어쓰기 거부를 실행 확인했다.
생성 파일은 코드 저장소에 넣지 않는다. 단계의 이유와 운영 조건은
[DevOps r13 원고](../../config/devops_implementation.2026-10-12.r13.json)에 있다.

r13의 3.3에서 시험용 포트8001을 확인한 뒤 종료하고, 3.4에서 검사한 파일을
`releases/v1`에 복사해 운영 연습용 포트8002로 실행한다. 4.2는 v2를 교체하고
저장한 같은v1 파일로 복구하는 명령과 실제 응답을 연결한다. 웹 다운로드는 r13
원고에 보존한 파일 바이트로 생성되므로 이 폴더의 후속 수정이 이전 실습을 바꾸지 않는다.
