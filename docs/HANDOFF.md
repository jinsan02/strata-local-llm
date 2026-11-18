# 인수인계

> 상태는 커밋과 `experiments/` 에만 있다. 앞 세션의 대화를 기억하고 있다고 가정하지 않는다.

## 현재 위치 (2026-11-18)

기획서 3.3 착수 게이트 1~3단계(환경 조사·준비) 진행 중. 모델 다운로드·측정은 아직 없다.

### 된 것

- 하드웨어 실측 → [`../env/hw-20261118.md`](../env/hw-20261118.md)
- 기획서를 STRATA v0.2.15 공식 문서와 대조 → [`prep-plan-20261118.md`](prep-plan-20261118.md)
  - M0 1순위: `qwen36 UD-Q4_K_XL` (hybrid 모드). Coder IQ1_M 은 SSD 의존 진단용
- 백그라운드 정리 스크립트와 시작 프로그램 해제 (백업 `env/startup-backup*.reg`)
- Anaconda + conda 환경 `strata_local_llm` (conda-forge)
- 저장소 규칙: kotokenlab 형식의 커밋 규칙 · 훅 · CI

### 진행 중

- VS 2022 Build Tools · CUDA 13.2.2 · CMake · Ninja 설치 (`scripts/install-buildtools.ps1`)

### 다음 할 일

1. 툴체인 검증 (`cl`, `nvcc --version`, `cmake --version`)
2. `engine/` 에 STRATA clone → v0.2.15 checkout → 커밋 해시 기록 → sm_120 빌드
3. `strata launch --plan --family qwen36 --model UD-Q4_K_XL` (및 coder IQ1_M) 결과 저장
4. 사용자 확인 후 M0 다운로드 → 태그 `m0-e0-freeze`

### 사용자에게 요청한 것

- 전원 구성표 고성능으로 변경
- 양자화 단계 전 페이지 파일 확대 (예: 64GB)
