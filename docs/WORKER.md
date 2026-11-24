# 로컬 LLM 을 주 에이전트 · 워커로 쓰기

본체 STRATA(M0 · E0 · 32K)를 두 가지로 쓴다. 측정(X3 · B1 등)과 같은 GPU 를 쓰므로 **측정 체인이 도는 동안에는 쓰지 않는다**
(워커는 체인을 감지하면 `busy` 로 거부한다).

| 방식 | 구조 | 준비 상태 (11-18) |
| --- | --- | --- |
| **주 에이전트** | 노트북 Claude Code · Codex 의 모델을 STRATA 로 바꿔 실행 (`scripts/client/`) | Codex 연결 · 응답 확인. Codex 0.169 `exec` 가 쓰기 샌드박스로 열리지 않는 문제는 X4 에서. 노트북에 Claude Code CLI 없음 |
| **워커** | 클라우드 Claude · Codex(지휘자)가 MCP 도구 `delegate_code_task` 로 작은 작업을 넘기고 diff 를 받음 (`scripts/worker/`) | 자체 점검 5/5, 노트북 → ssh → MCP → 실제 모델 끝까지 1건 통과 |

## 1. 서버 띄우기 (공통)

ssh 에서 그냥 띄우면 ssh 가 끝날 때 같이 꺼진다(T-012). 운영용은 WMI 로 띄운다. 키는 실행 시 `.secrets` 에서 읽는다.

```powershell
powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\launch_serve.ps1                  # 32K, Tailscale 주소 (노트북 · 본체 워커 둘 다)
powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\launch_serve.ps1 -Host_ 127.0.0.1  # 본체 안에서만
powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop                # 내리기
```

노트북에서는 `ssh desktop-5070 "powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\launch_serve.ps1"`.
준비까지 약 1분(11-18: 63초). 로그 `engine\serve-detached.log`. 32K 에서 엔진이 RAM 을 거의 다 쓰므로(T-003) 본체에서 무거운 일을 같이 하지 않는다.

## 2. 주 에이전트

`scripts/client/README.md` 와 `docs/ENVIRONMENT.md` '노트북에서 호출'. 요약:

```powershell
.\scripts\client\codex-local.ps1                  # 대화형
.\scripts\client\claude-local.ps1                 # Claude Code CLI 가 설치돼 있어야 한다 (npm i -g @anthropic-ai/claude-code)
```

11-18 확인: Codex 0.169 → STRATA Responses API 연결 · 답 17초, 입력 약 9.3K 토큰. 남은 문제(X4):
`model_max_output_tokens` 를 이 버전이 무시한다, `exec -s workspace-write` 에서도 권한 프로필이 루트 읽기 전용이라 파일을 못 쓴다,
`strata` 모델 메타데이터가 없다는 경고. 샌드박스를 끄는 `--dangerously-bypass-approvals-and-sandbox` 는 쓰지 않는다.

## 3. 워커

```
지휘자 (노트북 Claude Code · Codex, 클라우드 모델)
   │  MCP stdio  ─ ssh desktop-5070 python scripts/worker/mcp_server.py
   ▼
strata_worker.py: 서버 · 측정 체인 확인 → 잠금 → 대상 커밋을 별도 작업 트리로(work/worker/<id>) →
   X3 탐색 루프(list_files · grep · read_file · edit_file, configs/worker.json 의 하네스) → test_cmd →
   실패 시 diff + 로그로 1회 보완 → diff · 테스트 결과 · 통계 반환 (원시 기록 work/worker/logs/<id>.json)
```

도구: `delegate_code_task(task, repo, ref?, files?, test_cmd?, max_steps?, repair?, keep_worktree?)` · `worker_status` · `discard_worktree(worker_id)`.
반환 `status`: `done` · `tests_failed` · `no_change` · `rejected`(11-24, 위임 전 확인에서 막힘) · `busy` · `server_down` · `error`. done 이 아니면 `handoff` 안내가 붙는다.

### 등록 (지휘자 쪽, 사람이 한다 — 클라이언트 설정 변경)

Claude Code (노트북):

```powershell
claude mcp add strata-worker -s user -- ssh desktop-5070 C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe C:\strata-lab\scripts\worker\mcp_server.py
```

작업 하나가 수 분 걸릴 수 있으므로 Claude Code 를 띄우기 전에 `MCP_TOOL_TIMEOUT=1800000`(ms)을 환경 변수나 `settings.json` 의 `env` 에 둔다.

Codex (`~/.codex/config.toml`, 평소 설정):

```toml
[mcp_servers.strata-worker]
command = "ssh"
args = ["desktop-5070", "C:\\ProgramData\\anaconda3\\envs\\strata_local_llm\\python.exe", "C:\\strata-lab\\scripts\\worker\\mcp_server.py"]
startup_timeout_sec = 30
tool_timeout_sec = 1800
```

본체에서 지휘자를 돌리면 `ssh desktop-5070` 없이 python 경로부터 쓴다. 명령줄로 직접:
`python scripts\worker\strata_worker.py --repo <경로> --task "..." --test-cmd "..."` (`--status`, `--drop <id>`).

### 맡길 작업의 크기

X3 과제 크기가 기준이다: 파일 1~3개, 수십 줄, 할 일 · 경계 조건 · 확인 명령이 분명한 티켓(X3 15회 중 12~14회 통과, 회귀 0).
설계, 여러 모듈 리팩터링, 원인을 모르는 디버깅, 운영 작업은 지휘자가 한다. 11-24 A안: 위임 기준 · 위임 전 확인(precheck) · 실패 넘기기(handoff)는 [`delegation-20261124.md`](delegation-20261124.md). 티켓 예:

```json
{"task": "textutil/slug.py 의 slugify 를 고쳐라. 규칙: (1) 앞뒤 공백 제거 후 소문자, (2) 영숫자가 아닌 연속 문자는 하이픈 하나, (3) 앞뒤 하이픈 제거, (4) str 이 아니면 TypeError. 테스트 파일은 고치지 마라.",
 "repo": "C:\\work\\myrepo", "files": ["textutil/slug.py", "tests/check_slug.py"],
 "test_cmd": "set PYTHONPATH=. && C:\\path\\python.exe tests\\check_slug.py"}
```

### 주의

- `repo` 는 **본체의** 저장소 경로나 git URL 이다. 커밋된 상태만 보인다 — 노트북 변경은 먼저 push 하고 URL + `ref` 로 준다.
- 결과는 원본에 적용되지 않는다. 지휘자가 diff 를 검토하고 `git apply` 한다(`base_commit` 기준).
- `test_cmd` 는 본체 `cmd.exe` 에서 작업 트리를 현재 폴더로 돈다. 인터프리터는 절대경로로, import 경로가 필요하면 `set PYTHONPATH=. &&`.
  11-18 첫 실제 시험이 이것 때문에 `tests_failed` 였다(모델은 보완 턴에서 '코드는 맞고 실행 환경 문제' 라고 답하고 더 고치지 않음).
- 서버가 단일 슬롯이라 한 번에 한 작업(잠금 `work/worker/busy.lock`). ssh 가 끊기면 진행 중인 작업도 끊긴다.
- 테스트는 `PYTHONDONTWRITEBYTECODE=1` 로 돈다(보완 시도에서 옛 `.pyc` 가 고친 소스를 가리는 문제, 자체 점검에서 발견).

### 점검 기록

| 날짜 | 무엇 | 결과 |
| --- | --- | --- |
| 11-18 | `selftest_worker.py` (가짜 응답): 한 번에 성공 · 보완 후 성공 · 경로 거부 · 잠금 · MCP 프로토콜 | 5/5 |
| 11-18 22:35 | 노트북 → ssh → MCP → STRATA 32K, slugify 티켓 | `done`, 43초, 모델 호출 5회, 최대 입력 2,019 토큰, 편집 1회, 테스트 7/7 |

### 다음 (X5 워커 위임)

1. H3 · 채택 확인 뒤 `configs/worker.json` 을 채택 하네스로 바꾼다(같은 커밋에 근거).
2. X4(주 에이전트 기준선) 뒤 A/B: 같은 과제 묶음을 '클라우드 단독' vs '클라우드 지휘 + 로컬 워커'로 — 통과 수 · 회귀 · 클라우드 토큰 · 총 시간.
3. 지휘자가 큰 요청을 X3 크기 티켓으로 쪼갤 때 품질이 유지되는지가 첫 질문이다.
