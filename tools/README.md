# tools — 훅 본체와 검사기

표준 라이브러리만 쓴다 (CI 가 pytest 만 깔고 돈다).

| 파일 | 하는 일 | 부르는 곳 |
| --- | --- | --- |
| `repo.py` | git 인덱스·원장 읽기 공용 | 아래 셋 |
| `check_commit_msg.py` | 커밋 메시지 규칙 | `.githooks/commit-msg`, CI, `verify.ps1` |
| `precheck.py` | 금지 경로·바이너리·크기·lockbox·원장 | `.githooks/pre-commit` |
| `validate_ledger.py` | 원장 헤더·열 수·status·append-only | pre-commit, CI, `verify.ps1` |

규칙 문서와 이 코드가 다르면 코드가 맞다. 규칙을 바꾸면 `docs/` 와 여기를 같은 커밋에서 고친다.
