# experiments — 원장과 run 기록

| 경로 | 내용 | git |
| --- | --- | --- |
| `LEDGER.tsv` | append-only 원장. 열은 `docs/LEDGER_SCHEMA.md` | 커밋 |
| `runs/<run_id>/config.json` | run 이 쓴 설정 | 커밋 |
| `runs/<run_id>/env.json` | run 시점 환경 (드라이버·엔진 커밋·모델 해시) | 커밋 |
| `runs/<run_id>/summary.*` | 집계 (중앙값·표준편차·반복 수) | 커밋 |
| `runs/<run_id>/raw/`, `*.log`, `*.jsonl` | 원시 스트림·로그 | git 밖 |

결과 커밋은 `record(<scope>):` 이고 이 폴더와 `reports/` · `docs/` 만 스테이지할 수 있다.
