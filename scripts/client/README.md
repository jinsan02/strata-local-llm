# scripts/client — 노트북에서 부르는 스크립트

본체(`desktop-5070`)가 아니라 **노트북**에서 돈다. Tailscale 로 본체 STRATA 서버(포트 8080)를 부른다.
노트북에는 Python 이 없으므로 PowerShell 만 쓴다. 한국어가 든 `.ps1` 은 **UTF-8 BOM** 으로 저장한다(Windows PowerShell 5.1).

| 스크립트 | 하는 일 |
| --- | --- |
| `strata-remote.ps1` | TCP 연결 → `/v1/models` → 짧은 질문 하나. 연결 확인용 |
| `claude-local.ps1` | Claude Code 를 STRATA 에 붙여 실행 (그 프로세스에만 환경 변수) |
| `codex-local.ps1` | Codex 를 별도 `CODEX_HOME` 으로 실행 |

- 주소 기본값 `http://100.121.174.83:8080` (`STRATA_BASE_URL`), 창 크기 기본 32768 (`STRATA_CONTEXT`, 서버 `--context` 와 같게)
- API 키는 노트북 사용자 환경 변수 `STRATA_API_KEY` 에 있다(11-18 설정, 원본은 본체 `.secrets\` — git 제외). 커밋하지 않는다. 환경 변수가 없으면 스크립트가 `strata-local` 을 쓰는데, 키가 걸린 서버는 이를 401 로 거부한다
- 여기서 잰 시간에는 Tailscale 왕복이 섞인다. 원장 측정은 본체에서 한다 (`docs/RULES.md` 6번)

설정 순서는 `docs/ENVIRONMENT.md` '노트북에서 호출'.
