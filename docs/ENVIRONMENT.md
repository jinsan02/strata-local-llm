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
