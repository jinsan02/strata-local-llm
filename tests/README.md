# tests — 훅 본체 단위 테스트

GPU·네트워크·모델 없이 돈다. CI 와 같은 조건이다.

```powershell
C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe -m pytest tests -q -p no:cacheprovider
```

| 파일 | 대상 |
| --- | --- |
| `test_hooks.py` | 커밋 메시지 규칙, pre-commit 경로 검사, 원장 append-only |

테스트를 통과시키려고 테스트를 약하게 고치지 않는다.
