# 실행 환경

환경은 설치하고 잊는 것이 아니라 **버전이 찍히는 실험 변수**다.
툴체인이나 드라이버를 바꾸면 결과가 달라질 수 있고, 그 사실이 기록에 없으면
나중에 두 측정을 비교할 수 없다. 실측 사양은 [`../env/hw-20261118.md`](../env/hw-20261118.md).

## 하드웨어

```
호스트  DESKTOP-053T952 (Tailscale 100.121.174.83, SSH 별칭 desktop-5070, 사용자 jinsan)
GPU     NVIDIA GeForce RTX 5070 Ti 16GB (16303 MiB), sm_120 (Blackwell)
Driver  616.92 (CUDA UMD 13.4)
CPU     AMD Ryzen 9 9900X 12C/24T
RAM     DDR5 32GB (16GB×2, 6000MT/s)
SSD     WD_BLACK SN850X 2TB NVMe
```

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
노트북 (Tailscale 100.104.230.60)  ──tailnet──▶  desktop-5070 (100.121.174.83):8080  STRATA 서버
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

```bat
scripts\strata.cmd launch --family qwen36 --model ud-q4_k_xl --data-dir C:\strata-lab\data --context 32k --parallel 1 --vision off --access tailscale --port 8080 --no-tui
scripts\strata.cmd launch --show-key
```

코딩 도구는 프롬프트가 커서 **32K 창**이 필요하다 (Claude Code 전체 15.6K · 단순 모드 1.25K, Codex 8.6K 토큰). 측정 단계는 8K 기준선 · 16K 중간 · 32K 운영 목표다 (`docs/plan-v2.1-amendment-20261118.md`). 클라이언트 예산(출력+reasoning 8,192, 요약 기준 20,000)은 서버 `--context` 와 같은 커밋에서 맞춘다.

### 3. 노트북

API 키는 사용자 환경 변수에만 둔다 (파일·커밋 금지):

```powershell
[Environment]::SetEnvironmentVariable('STRATA_API_KEY', '<--show-key 로 본 키>', 'User')
```

| 스크립트 | 하는 일 |
| --- | --- |
| `scripts/client/strata-remote.ps1` | 연결 확인: TCP → `/v1/models` → 짧은 질문 |
| `scripts/client/claude-local.ps1` | Claude Code 를 STRATA 에 붙여 실행. 환경 변수는 그 프로세스에만 — 평소 `~/.claude/settings.json` 은 그대로 |
| `scripts/client/codex-local.ps1` | Codex 를 별도 `CODEX_HOME`(`~/.codex-strata`)으로 실행 — 평소 `~/.codex` 는 그대로 |

노트북에서 잰 시간에는 Tailscale 왕복이 섞이므로 원장 측정에 쓰지 않는다.
