# scripts/local — 본체 안에서 로컬 LLM 쓰기

본체(`desktop-5070`)에서 돈다. 서버는 127.0.0.1 전용으로 띄우고(키는 `.secrets\`), Claude Code CLI 는 본체에 복사한 2.1.328 을 쓴다.
결과 · 배경은 [`docs/x4-results-20261124.md`](../../docs/x4-results-20261124.md).

| 스크립트 | 하는 일 |
| --- | --- |
| `strata-up.ps1` | 떠 있는 서버를 내리고 127.0.0.1 로 띄운다(64K · E2). `-Tailscale` · `-LlmMode` |
| `session-start.ps1` | **작업 시작 전 한 번.** git 상태 · 안 올린 커밋 · 작업 트리 · 도는 측정/워커 · 서버(`strata-status.ps1`) · 디스크 · 원장 마지막 줄 · STATE '지금'을 한 화면에, 끝에 '확인할 것'. 읽기만 한다. `-Fetch` · `-StateLines N` |
| `strata-status.ps1` | 프로세스 · 주소 · 응답 · RAM · GPU |
| `strata-down.ps1` | 내리기 |
| `claude-desk.ps1` | Claude Code 를 서버에 붙인다. `-TestEnv packaging|flask` 면 그 conda 환경으로 pytest 가 돌고 **인터넷은 막힌다**(프록시 변수). `-InFile <파일>` 은 지시문을 stdin 으로. 나머지 인자는 claude 에 그대로 |
| `x4d-task.ps1` | X3 · Y 과제 하나를 본체에서 풀고(Bash 는 `python -m pytest` · `git diff/status` 만) `x4_grade.py` 로 채점. 끝나면 도구 입력에 금지 경로 · 네트워크 흔적이 있는지 `meta.audit` 에 적는다 |
| `x4d-batch.ps1` | 8과제 x 2회 일괄(WMI, ssh 를 끊어도 산다). `-Prefix` · `-Only "과제:회차,..."` |

- 서버가 떠 있으면 RAM 여유가 1GB 안쪽이다(클라이언트 실행 중 최소 0.45GB 관측). 클라이언트는 한 번에 하나만 돌린다.
- 워커(`scripts/worker`)는 `STRATA_BASE_URL` 이 없으면 127.0.0.1 을 쓰므로 그대로 된다. 노트북에서 쓰려면 `strata-up.ps1 -Tailscale`.
- 11-24 x4b dg r2 에서 모델이 `python -c` 로 GitHub 원본을 받았다. 그래서 `python -c` 를 허용하지 않고 프록시로 막는다. 원시 소켓까지 막지는 못하니 audit 결과를 같이 본다.
