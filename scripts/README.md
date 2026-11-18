# scripts — PowerShell 실행 스크립트

본체(`desktop-5070`)에서 돈다. 노트북에서는 `ssh desktop-5070 "powershell -NoProfile -ExecutionPolicy Bypass -File C:\strata-lab\scripts\<이름>.ps1"`.

| 스크립트 | 하는 일 | 로그 |
| --- | --- | --- |
| `cleanup.ps1` | 측정 전 백그라운드 앱 종료, 전후 메모리 기록 (프로그램 삭제 없음) | `env/cleanup.log` |
| `install-anaconda.ps1` | Anaconda 설치(SHA256 확인) + 환경 `strata_local_llm` | `env/install-anaconda.log` |
| `install-buildtools.ps1` | VS 2022 Build Tools · CUDA 13.2.2 · CMake · Ninja | `env/install-buildtools.log` |
| `fix-vs-buildtools.ps1` | 1차 설치가 `C:\Program` 에 들어간 VS 를 지우고 기본 경로로 재설치 | `env/install-buildtools.log` |
| `build-strata.ps1` | 엔진 고정 커밋 소스 빌드 (Ninja, sm_120, `build-e0`) | `env/build-strata-e0.log` |
| `strata.cmd` | STRATA CLI 를 conda 환경으로 실행 (`STRATA_PYTHON`). ASCII 만 (cmd 코드 페이지) | — |
| `setup-m0.ps1` | STRATA 소스 setup 으로 M0 실행 구성 생성 (`--build --no-start`, conda Python) | `env/setup-m0-ctx<N>.log` |
| `serve-ctx.ps1` | `--max-context` 만 바꾼 설정 사본으로 서버 전환 (`-Stop` 은 내리기) | `engine/serve-*.log` (git 밖) |
| `bench/run_bench.py` | 측정 러너: 스트리밍 지연·엔진 보고 속도·Peak VRAM/RAM·`/metrics` 의 file_mb·drafts 를 원장에 | 원장 |
| `client/` | **노트북에서** Tailscale 로 서버를 부르는 스크립트 (`client/README.md`) | — |
