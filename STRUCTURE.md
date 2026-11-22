# STRUCTURE.md — 폴더 지도와 실험 큰 틀

2026-11-18 작성, 11-22 갱신. 사람과 AI 에이전트가 **어디에 무엇을 만들고, 무엇을 기준으로 삼는지** 적습니다. 진행 상태는 `STATE.md`, 규칙은 `docs/RULES.md`.

## 1. 읽는 순서

| 누구 | 순서 |
| --- | --- |
| 처음 받은 사람 | `README.md` → 이 파일 → `STATE.md` → `docs/plan-v2.0.md` |
| AI 에이전트 | `AGENTS.md` → `STATE.md` → `docs/RULES.md` → 이 파일 3절(단계 표) → 작업 폴더의 `AGENTS.md`·`README.md` → 기준 문서의 해당 절만 |

## 2. 폴더 트리

**(예정)**은 아직 없는 것입니다. `git 밖`은 커밋하지 않습니다.

```
strata-lab/                     C:\strata-lab (desktop-5070)
├─ AGENTS.md                    AI 작업 지침 (Codex·Claude Code 공용)
├─ CLAUDE.md                    @AGENTS.md 불러오기만
├─ CONTRIBUTING.md              GitHub 규칙: 이슈·브랜치·커밋·PR·태그
├─ README.md                    소개, 처음 받았을 때 할 일
├─ STATE.md                     진행 상태·결정 기록·열린 질문
├─ STRUCTURE.md                 이 파일
├─ verify.ps1                   커밋 전 전체 검증
├─ .gitattributes · .gitignore  줄바꿈 LF 강제(.ps1 만 CRLF), 바이너리·엔진·모델 제외
├─ .githooks/                   commit-msg · pre-commit (본체는 tools/)
├─ .github/                     CI, PR·이슈 템플릿, CODEOWNERS
│
├─ docs/                        설계·규칙 문서 (docs/README.md)
│  ├─ plan-v2.0.md               기획서 원본 (고치지 않음)
│  ├─ prep-plan-20261118.md      착수 준비 계획, 기획서 검토 결과
│  ├─ plan-v2.1-amendment-20261118.md  32K 운영 목표·실험 매트릭스 (v2.0 일부 대체)
│  ├─ RULES.md                   하드룰 — 규칙의 단일 출처
│  ├─ COMMIT_CONVENTION.md       커밋 type·scope·트레일러·브랜치·태그
│  ├─ WORKFLOW.md                실험 1건의 수명, 두 에이전트 교대
│  ├─ LEDGER_SCHEMA.md           원장 열 정의
│  ├─ ENVIRONMENT.md             하드웨어·conda·빌드 툴체인
│  └─ …                          실험 설계 · 결과 문서 (문서별 상태는 docs/README.md)
│
├─ env/                         환경 기록 (env/README.md)
│  ├─ hw-20261118.md             본체 실측 사양, 정리 효과
│  ├─ strata-plan-20261118.md    E0 빌드 기록과 --plan 결과
│  ├─ strata_local_llm.yml       conda 환경 선언
│  ├─ install-*.log              설치 기록 (해시·종료 코드)
│  ├─ cleanup.log                정리 전후 메모리
│  └─ startup-backup*.reg        시작 프로그램 해제 전 값
│
├─ scripts/                     PowerShell 실행 스크립트 (scripts/README.md, AGENTS.md)
│  ├─ cleanup.ps1                측정 전 백그라운드 정리
│  ├─ install-anaconda.ps1       Anaconda + 환경
│  ├─ install-buildtools.ps1     VS Build Tools · CUDA · CMake · Ninja
│  ├─ build-strata.ps1           고정 커밋 소스 빌드 (E0 → engine/build-e0)
│  ├─ strata.cmd                 STRATA CLI 를 conda 환경으로 실행
│  ├─ bench/                     측정 러너 · 자체 점검 · 측정 체인 (bench/README.md)
│  ├─ analysis/                  원장 분석 (x3_combo.py)
│  ├─ quant/                     Q1 양자화 보정 · 생성 · 관문 체인
│  ├─ worker/                    로컬 LLM 워커 · MCP 서버 (docs/WORKER.md)
│  ├─ serve-ctx.ps1 · launch_serve.ps1  서버 기동 (측정용 · 운영용 WMI)
│  └─ client/                    노트북에서 Tailscale 로 부르는 스크립트 (연결 확인 · Claude Code · Codex)
│
├─ configs/                     실행 설정 · 양자화 레시피 (configs/README.md)
│  ├─ eval/                      X3 과제 정의 (6과제 + 확인 전용)
│  ├─ quant/                     양자화 레시피 (M1a~M2)
│  └─ worker.json                워커 기본 설정
│
├─ experiments/                 원장과 run 기록 (experiments/README.md, AGENTS.md)
│  ├─ LEDGER.tsv                 append-only 원장
│  └─ runs/<run_id>/             config·env JSON, 요약 (raw/ 는 git 밖)
│
├─ reports/                     단계별 요약 · 진행 요약(progress-*.md) · 그림(figures/)
├─ tools/                       훅 본체 · 원장 검사 (tools/README.md)
├─ tests/                       훅 본체 단위 테스트 (tests/README.md)
│
├─ engine/                      git 밖 — STRATA 체크아웃 (고정 커밋 c775728)
├─ work/                        git 밖 — 작업 복사본, 측정 중 준비물(stage/), E1 엔진 작업 폴더(engine-e1/)
├─ data/                        git 밖 — Strata-data, 모델·팩
├─ downloads/                   git 밖 — 설치 파일
└─ final_eval/                  git 밖 — 최종 평가 50문항 (후보 고정 전 열지 않음)
```

## 3. 단계별 기준 문서와 산출물

| 단계 | 기준 문서 (이 순서로 이김) | 만드는 곳 | 커밋 scope |
| --- | --- | --- | --- |
| 환경 | `prep-plan` 1·3절 → `ENVIRONMENT.md` | `env/`, `scripts/` | `env` |
| 엔진 E0 · E1 | `plan` 3.1·6.4 → STRATA 고정 커밋 문서 | `engine/`(git 밖), `scripts/build-strata.ps1` | `engine` |
| 기준선 B0 · 설정 B1 | `plan` 6.1·6.2·7절 → `prep-plan` 2절 | `configs/settings/`, `experiments/` | `config`, `bench` |
| 맞춤 양자화 Q1 | `plan` 4·6.3절 → STRATA `QUANTS.md` | `configs/quant/`, `data/`(git 밖) | `quant`, `model` 커밋 |
| 품질 평가 | `plan` 8절 | 탐색 세트는 `configs/eval/`(예정), 최종은 `final_eval/`(git 밖) | `eval` |
| 결합 C1 · 최종 F1 | `plan` 6.1·9절 | `experiments/`, `reports/` | `bench`, `eval` |

## 4. 큰 실수를 막는 체크리스트

커밋 전에 내 변경이 아래를 어기지 않는지 봅니다. 하나라도 어기면 사람에게 먼저 묻습니다.

| # | 확인 | 어기면 생기는 일 |
| --- | --- | --- |
| 1 | 측정 결과와 코드·설정 변경을 다른 커밋으로 | 어느 코드가 그 수치를 냈는지 모름 |
| 2 | 원장 기존 행을 고치지 않음, 실패 run 도 기록 | 같은 실패를 반복, 기준선 조작 의심 |
| 3 | 기준선과 후보를 같은 날 같은 상태에서 교차 측정 | 온도·캐시·백그라운드 차이를 개선으로 착각 |
| 4 | 비교 묶음의 `engine_commit` · `model_sha256` · `settings_id` 가 의도한 것만 다름 | 효과 귀속이 틀림 |
| 5 | 8K · parallel 1 조건, 템플릿 포함 실제 토큰 수 기록 | 목표 조건 미달을 달성으로 보고 |
| 6 | tok/s 는 엔진 보고값, reasoning 포함 여부 명시 | 처리량 착시 |
| 7 | 허용 오차·채점 기준은 결과 보기 전에 정함 | 사후 확대로 거짓 통과 |
| 8 | `final_eval/` 을 열지 않음 | 최종 평가 오염 (되돌릴 수 없음) |
| 9 | 모델·팩·설치 파일은 해시만 커밋 | 저장소 비대, 라이선스 문제 |
| 10 | 다른 프로젝트의 conda 환경·폴더를 건드리지 않음 | 다른 실험 재현성 깨짐 |

## 5. 이름 규칙

| 대상 | 규칙 | 예 |
| --- | --- | --- |
| run_id | `<phase>_<구성ID>_<모델>_<엔진>_<설정>_<조건>`, 소문자 | `bench_b0_m0_e0_s0_ctx8k` |
| 구성 ID | 기획서 6.1 | `B0` `B1` `Q1` `E1` `C1` `F1` |
| 모델 · 엔진 · 설정 ID | `M<n>` · `E<n>` · `S<n>` | `M1`, `E1`, `S1` |
| 설정 파일 | `configs/settings/S<n>-<요지>.json` | `S1-expert-cache-12g.json` |
| 양자화 레시피 | `configs/quant/M<n>-<요지>.json` | `M1-attn-q6k.json` |
| 스크립트 | PowerShell, 동사-대상 | `install-buildtools.ps1`, `build-strata.ps1` |
| 커밋 | `<type>(<scope>): <제목>` | `record(bench): B0 기본 설정 8K 단일 요청 기준선` |
| 브랜치 | `exp/<phase>-<slug>`, `fix/<slug>`, `docs/<slug>` | `exp/config-expert-cache` |
| 문서 | 영문 대문자 또는 `이름-YYYYMMDD.md` | `prep-plan-20261118.md` |
