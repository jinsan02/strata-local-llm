# H11 후보: 편집 뒤 정적 진단 — 재현 (2026-11-24)

근거: [`harness-survey-20261124.md`](harness-survey-20261124.md) C1 (2609.20804 편집 뒤 ruff/pyflakes, Aider · OpenCode).
pyflakes 는 어느 conda 환경에도 없어(설치는 다운로드 승인 필요) **표준 라이브러리로 같은 핵심만** 구현했다.

## 방법

- 대상: 64K 시기 실행 180건의 최종 작업 사본(`work/x3-runs`): x3h9 · y9 · x3h9t · y9t · x3k64h7 · x3h8.
- 모델이 바꾼 `.py` 마다 (숨은 테스트 파일 제외)
  - S 정적: 파싱 실패 · 정의 안 된 이름(`symtable`, 클래스 속성을 메서드에서 맨이름으로 부르는 경우 포함). 기준 커밋의 같은 파일과 비교해 **새로 생긴 것만**.
  - I import: 바뀐 src 모듈을 실제로 import.
- 진단기 selftest 13/13(정의 안 된 이름 · 클로저 · 컴프리헨션 · global · try-import · 늦은 정의 · walrus · except as · 문법 오류).
- 스크립트: `scripts/bench/replay_lint.py`(selftest `scripts/bench/selftest_replay_lint.py` 13/13), 결과 `work/stage/replay_lint.json`(git 제외).

## 결과

| | 실행 | S 걸림 | 비고 |
|---|---:|---:|---|
| 실패 | 51 | **5** | 정의 안 된 이름 4 (y5 `timedelta` 3 · x3h8 metadata 도우미 함수 1), 들여쓰기 문법 1 (x3h9t marker, T1 · H10 b 가 잡는 종류) |
| 통과 | 129 | **0** | 헛경보 없음 |

- I(import 검사)는 S 이상을 잡지 못했다. flask 에서 걸린 것은 전부 `flask/__main__.py` 를 import 하면 CLI 가 도는 탓(진단기 쪽 문제) → **I 는 버린다.**
- 안 걸린 import_or_syntax 8건: 7건은 y3(테스트 작성 과제, 테스트 파일 수집 실패), 1건은 x3h8 marker(숨은 테스트가 없는 이름을 import). 정적 진단 범위 밖.
- 운영 기준 x3h9 30회: 걸림 0. y9 30회: 2(y5 r1 · r5).

## 상한 확인: import 한 줄만 넣고 다시 채점

| 실행 | 원래 diff 다시 채점(대조) | `from datetime import timedelta` 한 줄 추가 |
|---|---|---|
| y9 y5 r1 | 6/20 (원장과 같음) | **20/20 통과** |
| y9 y5 r5 | 4/20 (원장과 같음) | **20/20 통과** |
| y9t y5 r4 | 12/20 (원장과 같음) | **20/20 통과** |

- 세 건 모두 **나머지는 다 맞았고 import 하나가 빠져 실패**했다. 회귀 146개는 그대로 통과.
- 모델이 경고를 보고 import 를 넣는다면 y9 는 21 → 최대 23/30 (y5 1/5 → 3/5). x3h9 는 걸림 0 이라 변화 없음 예상.

## H11 설계안 (측정 전)

- edit_file 이 `.py` 에 성공한 직후, 결과 문자열 끝에 **새로 생긴** 정적 문제만 덧붙인다(막지 않음):
  `주의: 이 편집 뒤 정의되지 않은 이름 'timedelta' (sessions.py 41행). import 가 빠졌는지 확인하라.`
- 기준은 그 파일의 **이번 실행 첫 상태**(원래부터 있던 문제는 알리지 않음). 표준 라이브러리만(환경 무관), 파싱 실패는 T1 · H10 b 와 겹치므로 이름 검사만.
- 워커에도 같은 함수를 쓴다.
- 측정: x3h11 · y11 각 30회, 대조 x3h9 24/30 · y9 21/30, RULES 12 일반 변경 규칙. X4b 가 끝난 뒤.
