# STATE.md — 지금 어디까지 왔나

사람과 에이전트(Codex, Claude Code)가 함께 고치는 진행 기록입니다. 작업을 끝낼 때마다 해당 줄을 고치고 '최근 변경' 맨 위에 한 줄 더합니다. 설계 내용 자체는 `docs/`에, 수치는 `experiments/LEDGER.tsv`에, 여기는 상태와 결정만 둡니다.

## 지금

- 마지막 갱신: 2026-11-18
- 단계: **착수 게이트 1~3 (호환성·자원 조사, 환경 준비)**. 모델 다운로드·측정 없음
- 대상 PC: `desktop-5070` (Tailscale 100.121.174.83), 저장소 `C:\strata-lab`
- 실행 환경: conda `strata_local_llm` (Python 3.12, conda-forge), 빌드는 VS 2022 Build Tools + CUDA 13.2.2
- 주 실행자: Claude Code (노트북에서 SSH). Codex 로 비교할 때는 브랜치를 나눈다

## 단계 진행표

기획서 10절·6.1절 기준. 상태: 완료 · 진행 중 · 대기 · 미착수 · 미달

| 단계 | 구성 ID | 상태 | 완료 조건 | 근거 |
| --- | --- | --- | --- | --- |
| 호환성·자원 조사 | — | 완료 | 엔진·모델 지원, 메모리·디스크·CPU·PCIe 정보 | `docs/prep-plan-20261118.md`, `env/hw-20261118.md` |
| 환경 준비 | — | 진행 중 | conda · 툴체인 · STRATA 빌드 · `--plan` 결과 | 이 파일 '다음 할 일' |
| 기준선 | B0 | 미착수 | M0 · E0 고정(태그 `m0-e0-freeze`), 성능·품질·자원 로그 | 원장 |
| 실행 설정 튜닝 | B1 | 미착수 | S1, 병목 프로파일, 후보 순위 | 원장 |
| 맞춤 양자화 | Q1 | 미착수 | M1 레시피·형식 표·호환성·품질 | 원장 |
| 엔진 최적화 | E1 | 미착수 | 패치·수치 검사·E1 비교 | 원장 |
| 결합 | C1 | 미착수 | 단독 효과와 상호작용 | 원장 |
| 최종 검증 | F1 | 미착수 | 독립 50문항, 재시작 재현, 혼합 50회 · 60분 | 원장 |

## 다음 할 일

1. ~~툴체인 검증~~ 완료 (11-18): `cl` 19.44.35230, `nvcc` 13.2.86, CMake 4.1.2, Ninja 1.13.1
2. ~~STRATA E0 빌드~~ 완료 (11-18): v0.2.15 `c775728`, sm_120, `strata.exe` sha256 `907008da…` — `env/strata-plan-20261118.md`
3. ~~`--plan` 결과 저장~~ 완료 (11-18): qwen36 계획기는 다운로드 크기를 모름(실제 22.9GB), coder IQ1_M 은 64.5GB
4. launcher 가 릴리스 엔진 대신 소스 빌드 `engine\build-e0\strata.exe` 를 쓰게 하는 방법 확인 (`docs/SETTINGS.md`·`DETAILS.md`, `strata_cli/launch`)
5. 사람 확인 후 M0 다운로드(약 23GB) → 8K · parallel 1 로딩·API 응답 확인 → 태그 `m0-e0-freeze`

## 사람에게 요청한 것

| 날짜 | 요청 | 상태 |
| --- | --- | --- |
| 11-18 | 전원 구성표를 고성능으로 변경 (측정 위생) | 대기 |
| 11-18 | 양자화 단계 전 페이지 파일 확대 (예: 64GB) | 대기 |
| 11-18 | 커밋 작성자 이메일을 kotokenlab 과 같게 할지 결정 (지금은 noreply) | 대기 |

## 결정 기록

| 날짜 | 결정 | 근거 |
| --- | --- | --- |
| 11-18 | E0 = Niko1221/Strata v0.2.15 `c77572806996349b49995e4f98d41b5294d36a21` 소스 빌드(`build-e0`, sm_120, Ninja). 엔진의 Python 런타임은 `.venv` 대신 conda `strata_local_llm` 에 pip 고정 버전으로 설치하고 `scripts/strata.cmd` 로 부른다 | RULES 1번, 사용자 conda 관리 요청 |
| 11-18 | AI 작업 문서는 team4 형식(AGENTS · STATE · STRUCTURE · 폴더별 README/AGENTS · PR/이슈 템플릿)으로 둔다. `CLAUDE.md` 는 `@AGENTS.md` 한 줄로 불러오기만 한다 | 사용자 요청, encore-ai-campus/mlo-03-p1-team4 |
| 11-18 | 커밋·훅·CI·규칙 단일 출처(`docs/RULES.md`)는 kotokenlab 형식을 따른다. scope 는 기획서 단계(env · engine · config · quant · bench · eval · infra · docs) | 사용자 요청, jinsan02/kotokenlab |
| 11-18 | 저장소는 비공개 `jinsan02/strata-local-llm`. 본체는 이 저장소 전용 쓰기 deploy key 로 push 한다 | 사용자 선택 |
| 11-18 | conda 는 Anaconda(Navigator 포함) + 환경 `strata_local_llm`, 채널은 conda-forge 만 (기본 채널 이용약관 미동의) | 사용자 선택 |
| 11-18 | 빌드 툴체인은 VS 2022 Build Tools + CUDA 13.2.2(드라이버 제외), sm_120 | STRATA `SOURCE_INSTALL.md`: CUDA 13.0~13.2 ↔ VS2022 |
| 11-18 | M0 1순위 후보는 `qwen36 UD-Q4_K_XL`, Coder IQ1_M 은 SSD 의존 진단용. Flash-Next Q2/IQ2 는 RAM 기준 미달로 제외 | `docs/prep-plan-20261118.md` 2절 |
| 11-18 | E0 는 설치형이 아니라 고정 커밋의 **소스 빌드**. 설치형 바이너리는 참고용 | E1 패치와 같은 빌드 경로여야 비교 가능 |
| 11-18 | 측정 전 백그라운드 정리를 스크립트로 고정, 시작 프로그램 7개 해제(백업 `env/startup-backup*.reg`) | 사용자 요청, 가용 RAM 18.3 → 23.3GB |

## 열린 질문

정해지기 전에는 고르지 않는다. 필요해지면 사람에게 묻는다.

| # | 정할 것 | 권장 | 막는 것 | 근거 |
| --- | --- | --- | --- | --- |
| Q1 | 주 실행자 Codex/Claude Code 중 하나로 고정할지, 비교 실험을 할지 | Claude Code 고정, 비교는 B1 이후 별도 브랜치 | 5절 예산 | 기획서 5절 |
| Q2 | 탐색·최종 평가 데이터 출처(공개·합성) | 공개 벤치 일부 + 합성, 출처·버전 기록 | B0 품질 측정 | 기획서 8절 |
| Q3 | qwen36 경로에서 `--kv int8\|q4_0\|k8v4\|fp16` 이 실제로 적용되는지 (launcher 에는 옵션이 있고 기본 int8, QWEN36.md 는 fp32 라고 적음) | M0 로딩 뒤 KV 메모리로 확인, 적용되면 B1 후보 | B1 탐색 목록 | `env/strata-plan-20261118.md` |
| Q6 | launcher 가 소스 빌드 E0 를 쓰게 할지, 엔진을 직접 실행할지 | 소스 빌드 연결 방법을 먼저 찾고, 없으면 직접 실행 | B0 | RULES 1번 |
| Q4 | 맞춤 양자화 원본(BF16 약 70GB) 확보·변환 방식 | 샤드 스트리밍 변환 가능성 먼저 소형 검사 | Q1 단계 | 기획서 6.3 |
| Q5 | API 사용량·비용 예산 상한 | 착수 시 사람이 정함 | 탐색 예산 | 기획서 5.2, 11절 |

## 에이전트 사용

- 지침은 루트와 폴더의 `AGENTS.md`. Codex 는 루트부터 지금 폴더까지 합쳐 읽는다.
- Claude Code 는 `CLAUDE.md` 가 있으면 `AGENTS.md` 를 자동으로 읽지 않는다. 그래서 `CLAUDE.md` 는 `@AGENTS.md` 한 줄로 불러온다. 지침을 `CLAUDE.md` 에 쓰지 않는다.
- 개인 기억(Claude 자동 메모리 등)은 저장소에 공유되지 않는다. 다음 세션이 알아야 할 것은 이 파일과 `docs/` 에 쓴다.

## 최근 변경

- 2026-11-18 · Claude Code · STRATA v0.2.15 clone·고정, E0 소스 빌드 성공(2.8분), 엔진 Python 런타임을 conda 환경에 설치, `--plan` 2건 기록. 모델 다운로드 없음. 엔진 실행(GPU 인식) 검증은 모델이 없어 미실행.
- 2026-11-18 · Claude Code · 빌드 툴체인 설치·검증 완료. VS Build Tools 1차 설치가 `--installPath` 공백 분리로 `C:\Program` 에 들어가 제거 후 기본 경로로 재설치(`scripts/fix-vs-buildtools.ps1`), `install-buildtools.ps1` 도 고침. `verify.ps1` 통과.
- 2026-11-18 · Claude Code · team4 형식의 AI 작업 문서 추가: `AGENTS.md` 재작성, `STATE.md`·`STRUCTURE.md`·`CONTRIBUTING.md`, 폴더별 README/AGENTS, PR·이슈 템플릿, `verify.ps1`. `docs/HANDOFF.md` 는 이 파일로 합침.
- 2026-11-18 · Claude Code · 빌드 툴체인 설치 시작(VS 2022 Build Tools 종료 코드 0, CUDA 13.2.2 진행 중). 검증 전.
- 2026-11-18 · Claude Code · kotokenlab 형식의 커밋 규칙·훅·CI 도입, 첫 커밋을 형식에 맞는 4개로 다시 써서 force-push. 훅 테스트 11개 통과.
- 2026-11-18 · Claude Code · Anaconda 2026.07-1 설치(SHA256 확인), conda-forge 환경 `strata_local_llm` 생성.
- 2026-11-18 · Claude Code · 본체 실측, 기획서 검토, 백그라운드 정리·시작 프로그램 해제.
