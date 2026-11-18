# strata-local-llm

**STRATA Inference Optimization on a Single RTX 5070 Ti 16GB**

단일 RTX 5070 Ti 16GB · RAM 32GB 본체에서 [Niko1221/Strata](https://github.com/Niko1221/Strata) 로 MoE 모델을 돌리고, 한국어·코딩 품질을 지키면서 실행 설정 · 레이어별 맞춤 양자화 · 엔진 코드를 최적화하는 실험

> **착수 준비 중 (2026-11-18).** 하드웨어 실측과 기획서 검토를 마쳤고 툴체인을 설치하고 있다.
> 기준 모델 후보는 `qwen36 UD-Q4_K_XL`(Qwen3.6-35B-A3B, 22.9GB, hybrid 모드)이다.
> 아직 측정한 수치는 없다. 현재 위치는 [`docs/HANDOFF.md`](docs/HANDOFF.md).

| 단계 | 상태 |
|---|---|
| 호환성·자원 조사 | 완료 — [`docs/prep-plan-20261118.md`](docs/prep-plan-20261118.md), [`env/hw-20261118.md`](env/hw-20261118.md) |
| 환경 및 기준선 B0 | 툴체인 설치 중 |
| 실행 설정 B1 · 맞춤 양자화 Q1 · 엔진 E1 · 결합 C1 · 최종 F1 | 미착수 |

<details>
<summary><b>목표와 범위</b></summary>

첫 답변 지연, 답변 완료 시간, 생성 처리량, VRAM·RAM 사용량을 개선한다. 개선이 검증된 변경만
운영 구성에 반영하고, 개선이 없어도 재현 가능한 기준선과 실패 기록을 남긴다.
사전학습·파인튜닝, 외부 공개 서비스, 다중 GPU, 장비 구매는 범위 밖이다.

전체 설계: [`docs/plan-v2.0.md`](docs/plan-v2.0.md)
</details>

<details>
<summary><b>지키는 규칙</b></summary>

규칙 본문은 [`docs/RULES.md`](docs/RULES.md) 한 곳에만 있다. 요점:

- 엔진은 Niko1221/Strata 고정 커밋 하나, 다른 엔진으로 대체하지 않는다
- 최종 평가 50문항은 후보를 고정하기 전까지 열지 않는다 (`final_eval/` 은 훅이 막는다)
- 측정 기준·채점기·기준선을 바꿔서 수치를 올리지 않는다
- 결과는 append-only TSV 원장에 코드가 쓰고, `record` 커밋에 코드를 섞지 않는다
- 기준선과 후보는 같은 PC 에서 번갈아 잰다
</details>

## 폴더

| 경로 | 내용 | git |
|---|---|---|
| `docs/` | 기획서 · 규칙 · 작업 흐름 · 인수인계 | 커밋 |
| `env/` | 하드웨어 실측 · conda 선언 · 설치 로그 · 시작 프로그램 백업 | 커밋 |
| `scripts/` | 정리 · 설치 · 측정 스크립트 (PowerShell) | 커밋 |
| `tools/` · `tests/` | 훅 본체와 테스트 | 커밋 |
| `configs/` | 실행 설정 · 양자화 레시피 | 커밋 |
| `experiments/` | `LEDGER.tsv` 원장, run 별 config·요약 | 커밋 (raw 제외) |
| `engine/` · `data/` · `downloads/` | STRATA 체크아웃 · 모델 · 설치 파일 | **제외** |

## 시작하기

```powershell
git clone git@github.com:jinsan02/strata-local-llm.git C:\strata-lab
cd C:\strata-lab
git config core.hooksPath .githooks
```

Python 은 conda 환경 `strata_local_llm` 을 절대경로로 쓴다 — [`docs/ENVIRONMENT.md`](docs/ENVIRONMENT.md).
커밋 형식은 [`docs/COMMIT_CONVENTION.md`](docs/COMMIT_CONVENTION.md) (kotokenlab 과 같은 형식).
에이전트 진입점은 [`CLAUDE.md`](CLAUDE.md) · [`AGENTS.md`](AGENTS.md).
