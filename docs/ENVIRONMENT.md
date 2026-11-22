# 실행 환경

환경은 설치하고 잊는 것이 아니라 **버전이 찍히는 실험 변수**다.
툴체인이나 드라이버를 바꾸면 결과가 달라질 수 있고, 그 사실이 기록에 없으면
나중에 두 측정을 비교할 수 없다. 실측 사양은 [`../env/hw-20261118.md`](../env/hw-20261118.md).

## 하드웨어

```
호스트  DESKTOP-053T952 (Tailscale <본체 Tailscale 주소>, SSH 별칭 desktop-5070, 사용자 jinsan)
GPU     NVIDIA GeForce RTX 5070 Ti 16GB (16303 MiB), sm_120 (Blackwell)
Driver  616.92 (CUDA UMD 13.4)
CPU     AMD Ryzen 9 9900X 12C/24T
RAM     DDR5 32GB (16GB×2, 6000MT/s)
SSD     WD_BLACK SN850X 2TB NVMe
PAGE    C:\pagefile.sys 64GB 고정 (2026-11-19 12:08~, 이전 자동 4.6GB) — 커밋 한도 약 37GB → 95GB
```

**원격 운영 (2026-11-19)**: Tailscale '무인 실행' 켬(로그인 전에도 연결 → 재부팅 뒤 ssh 가능), sshd 자동 시작,
절전 · 최대 절전 '안 함', Windows 업데이트 12-10 까지 일시 중지(밤 체인 중 자동 재시작 방지). 원격 데스크톱은 계정이 암호 없는
로그인(Windows Hello)이라 쓸 수 없다 — 화면이 필요하면 본체 앞에서. Defender 매일 02:00 빠른 검사는 밤 측정과 겹친다(사람이 옮길 것).
페이지 파일을 바꾼 뒤의 측정(11-19 12:08~)은 그 전 수치와 섞어 비교하지 않는다.

## 저장소 위치

`C:\strata-lab` (git). 그 아래 `engine\` `data\` `downloads\` 는 git 밖이다.

## Python — conda

Anaconda Distribution 2026.07-1 을 `C:\ProgramData\anaconda3` (AllUsers) 에 설치했다.
Navigator 포함. 실험용 환경은 **`strata_local_llm`** (Python 3.12) 하나다.

- 채널은 **conda-forge 만** 쓴다. 기본 채널(repo.anaconda.com)은 이용약관 동의가
  필요해서 쓰지 않는다. 환경의 `.condarc` 가 `channels: [conda-forge]`, `strict` 로 고정한다
- `conda activate` 에 의존하지 않고 **인터프리터 절대경로**를 쓴다:

  ```
  C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe
  ```

- 이 PC 에는 다른 conda 설치(`C:\Miniconda3`, `C:\Users\jinsan\miniconda3`,
  `C:\llm_tokenizer\.conda`)가 있다. 다른 프로젝트의 것이므로 건드리지 않는다

패키지를 바꿨다면 선언 파일을 갱신하고 `chore(env):` 로 커밋한다:

```powershell
C:\ProgramData\anaconda3\Scripts\conda.exe env export -n strata_local_llm --no-builds > env\strata_local_llm.yml
```

## 빌드 툴체인

| 도구 | 버전 | 근거 |
|---|---|---|
| VS 2022 Build Tools | C++ 워크로드 | STRATA 소스는 C++20, VS2019 불가 |
| CUDA Toolkit | 13.2.2 (드라이버 제외) | CUDA 13.0~13.2 ↔ VS2022, 13.3 ↔ VS2026 |
| CMake | 4.1.2 | |
| Ninja | 1.13.1 (`C:\tools\ninja`) | |

빌드: `-DCMAKE_CUDA_ARCHITECTURES=120`. 설치 스크립트는 `scripts/install-*.ps1`,
설치 로그는 `env/install-*.log`.

## 버전 관리 파일

| 파일 | 역할 | git |
|---|---|---|
| `env/hw-*.md` | 하드웨어 실측 | 커밋 |
| `env/strata_local_llm.yml` | conda 환경 선언 | 커밋 |
| `env/install-*.log` | 설치 기록 (해시·종료 코드) | 커밋 |
| `env/startup-backup*.reg` | 시작 프로그램 해제 전 값 (`reg import` 로 복원) | 커밋 |
| `C:\ProgramData\anaconda3` | 실제 바이너리 | **제외** |

## 노트북에서 호출 (Tailscale)

목표: 로컬 LLM 이 완성되면 노트북의 코딩 도구(Claude Code · Codex · OpenCode)가 본체 STRATA 를 부른다.
STRATA v0.2.15 의 `strata connect` 가 이 셋을 공식 지원한다(`strata connect <app>` 로 설정 안내 출력).

```
노트북 (Tailscale 100.104.230.60)  ──tailnet──▶  desktop-5070 (<본체 Tailscale 주소>):8080  STRATA 서버
  scripts/client/*.ps1                                --access tailscale, API 키
```

### 1. 본체 방화벽 — 사람이 한다 (보안 설정)

STRATA 는 방화벽을 바꾸지 않는다(`strata_cli/launch/access.py`). Windows 의 허용 팝업은 SSH 세션에서는 뜨지 않으므로,
본체에서 **관리자 PowerShell** 로 한 번 실행한다. Tailscale 주소 대역(100.64.0.0/10)에서 오는 8080 만 연다.

```powershell
New-NetFirewallRule -DisplayName "STRATA 8080 (Tailscale only)" -Direction Inbound -Protocol TCP -LocalPort 8080 -RemoteAddress 100.64.0.0/10 -Action Allow -Profile Any
```

되돌리기: `Remove-NetFirewallRule -DisplayName "STRATA 8080 (Tailscale only)"`

### 2. 본체 서버

측정과 운영은 `strata launch`(서명된 설치 엔진 전용)가 아니라 E0 소스 빌드 경로로 띄운다:
`scripts\serve-ctx.ps1` → `engine\serve\server.py --engine strata --config engine\strata-qwen36-ctx<N>.json` → `engine\engine\strata.exe --serve --native`.

```powershell
powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context 32768                         # 본체 측정용, 127.0.0.1
powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Context 32768 -Host_ <본체 Tailscale 주소>   # X4: 노트북에서 부를 때
powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\serve-ctx.ps1 -Stop
```

이 PC 의 실행 정책은 기본값(Restricted)이라 `.ps1` 은 `-ExecutionPolicy Bypass` 를 붙여 실행한다(T-015). ssh 에서 띄운 서버는 ssh 가 끝나면 같이 꺼지므로(T-012), 노트북 클라이언트 · 워커용 운영 서버는 `scripts\launch_serve.ps1`(WMI, 기본 32K · Tailscale)로 띄운다 — [`WORKER.md`](WORKER.md).

**API 키 (2026-11-18 설정)**: 서버는 `STRATA_API_KEY` 를 키로 쓴다(`/v1/*` 에 `Authorization: Bearer` 또는 `x-api-key`).

| 위치 | 내용 | git |
| --- | --- | --- |
| 본체 `C:\strata-lab\.secrets\strata-api-key.txt` | 키 원본(43자, `secrets.token_urlsafe(32)`) | **제외** (`.gitignore` 의 `.secrets/`) |
| 본체 사용자 환경 변수 `STRATA_API_KEY` (jinsan) | 서버 · 러너가 읽는다. 새 ssh 세션부터 적용 | — |
| 노트북 사용자 환경 변수 `STRATA_API_KEY` | `scripts/client/*.ps1` 가 읽는다 | — |

- 키가 설정된 뒤로는 127.0.0.1 서버도 키를 요구한다(키 없음 · `strata-local` → 401, 실제 키 → 200, 11-18 확인). 러너는 같은 환경 변수를 읽으므로 그대로 동작한다.
- `serve-ctx.ps1` 은 루프백이 아닌 주소로 열 때 키가 없거나 16자 미만 · `none` · `strata-local` 이면 서버를 내리기 전에 거부한다.
- 키를 바꾸려면 `.secrets\strata-api-key.txt` 를 지우고 다시 만든 뒤 두 PC 의 사용자 환경 변수를 같이 바꾼다. 키 값은 로그 · 채팅 · 커밋에 쓰지 않는다.

코딩 도구는 프롬프트가 커서 **32K 창**이 필요하다 (Claude Code 전체 15.6K · 단순 모드 1.25K, Codex 8.6K 토큰). 측정 단계는 8K 기준선 · 16K 중간 · 32K 운영 목표다 (`docs/plan-v2.1-amendment-20261118.md`). 클라이언트 예산(출력+reasoning 8,192, 요약 기준 20,000)은 서버 `--context` 와 같은 커밋에서 맞춘다.

### 3. 노트북

API 키는 노트북 사용자 환경 변수 `STRATA_API_KEY` 에 있다(11-18 설정, 본체 `.secrets\strata-api-key.txt` 와 같은 값). 커밋 금지.
다시 설정할 때(키 값을 화면에 띄우지 않고 본체에서 받아 온다):

```powershell
ssh desktop-5070 "type C:\strata-lab\.secrets\strata-api-key.txt" | powershell -NoProfile -Command '$k=[Console]::In.ReadToEnd().Trim(); [Environment]::SetEnvironmentVariable("STRATA_API_KEY",$k,"User")'
```

| 스크립트 | 하는 일 |
| --- | --- |
| `scripts/client/strata-remote.ps1` | 연결 확인: TCP → `/v1/models` → 짧은 질문 |
| `scripts/client/claude-local.ps1` | Claude Code 를 STRATA 에 붙여 실행. 환경 변수는 그 프로세스에만 — 평소 `~/.claude/settings.json` 은 그대로 |
| `scripts/client/codex-local.ps1` | Codex 를 별도 `CODEX_HOME`(`~/.codex-strata`)으로 실행 — 평소 `~/.codex` 는 그대로 |

노트북에서 잰 시간에는 Tailscale 왕복이 섞이므로 원장 측정에 쓰지 않는다.
