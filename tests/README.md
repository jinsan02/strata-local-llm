# tests — 훅 · 공용 도구 · 워커 규칙 단위 테스트

GPU·네트워크·모델 없이 돈다. CI 와 같은 조건이다.

```powershell
C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe -m pytest tests -q -p no:cacheprovider
```

| 파일 | 대상 |
| --- | --- |
| `test_hooks.py` | 커밋 메시지 규칙, pre-commit 경로 검사, 원장 append-only |
| `test_repo_error_type.py` | 원장 note 의 `error_type` 읽기 · '통과' 판정(`tools/repo.py`) |
| `test_route_summary.py` | 워커 위임 기록 `route.jsonl` 집계(`scripts/worker/route_summary.py`) |
| `test_worker_precheck.py` | 워커 위임 전 확인 · 지휘자 넘기기 규칙(`scripts/worker/strata_worker.py`, git 만 필요) |

테스트를 통과시키려고 테스트를 약하게 고치지 않는다.
