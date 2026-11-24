# scripts/local — 본체 안에서 로컬 LLM 쓰기

본체(`desktop-5070`)에서 돈다. 서버는 127.0.0.1 전용으로 띄우고(키는 `.secrets\`), Claude Code CLI 는 본체에 복사한 2.1.328 을 쓴다.
결과 · 배경은 [`docs/x4-results-20261124.md`](../../docs/x4-results-20261124.md).

| 스크립트 | 하는 일 |
| --- | --- |
| `strata-up.ps1` | 떠 있는 서버를 내리고 127.0.0.1 로 띄운다(64K · E2). `-Tailscale` · `-LlmMode` |
| `strata-status.ps1` | 프로세스 · 주소 · 응답 · RAM · GPU |
| `strata-down.ps1` | 내리기 |
| `claude-desk.ps1` | Claude Code 를 서버에 붙인다. `-TestEnv packaging|flask` 면 그 conda 환경으로 pytest 가 돈다 |
| `x4d-task.ps1` | X3 · Y 과제 하나를 본체에서 풀고(테스트 실행 허용) `x4_grade.py` 로 채점 |

- 서버가 떠 있으면 RAM 여유가 1GB 안쪽이다. 클라이언트는 한 번에 하나만 돌린다.
- 워커(`scripts/worker`)는 `STRATA_BASE_URL` 이 없으면 127.0.0.1 을 쓰므로 그대로 된다. 노트북에서 쓰려면 `strata-up.ps1 -Tailscale`.
