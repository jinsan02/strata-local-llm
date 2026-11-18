# strata-local-llm

**STRATA Inference Optimization on a Single RTX 5070 Ti 16GB**

단일 RTX 5070 Ti 16GB · RAM 32GB 본체에서 [Niko1221/Strata](https://github.com/Niko1221/Strata) 로 MoE 모델을 돌리고, 한국어 · 코딩 품질을 지키면서
실행 설정 · 하네스 · 레이어별 맞춤 양자화 · 엔진 코드를 최적화하는 실험. 최종 목표는 본체 STRATA(32K)를 노트북의 코딩 도구(Claude Code · Codex)가
Tailscale 로 불러 **파일 탐색 → 수정 → 테스트 → 실패 로그로 재수정** 을 안정적으로 하는 것이다.

> **1차(실행 설정 · 하네스) 진행 중 — 2026-11-18 기준.** 원장 371행. 현재 위치와 다음 할 일은 [`STATE.md`](STATE.md),
> 내일 계획은 [`docs/plan-20261119.md`](docs/plan-20261119.md), 폴더 지도는 [`STRUCTURE.md`](STRUCTURE.md).

## 고정한 것

| 항목 | 값 |
| --- | --- |
| 모델 M0 | Qwen3.6-35B-A3B `UD-Q4_K_XL` (22.9GB, sha256 일치), hybrid 모드 — 32K 에서 VRAM 에 expert 63/256 |
| 엔진 E0 | STRATA v0.2.15 `c775728` 소스 빌드(`setup.py --build`, sm_120), `serve/server.py --engine strata` + `strata.exe --serve --native` |
| 운영 목표 | 컨텍스트 32,768 · 입력 24,576 · 출력+reasoning 8,192 · 단일 슬롯 |
| 샘플링 S0 | temperature 1.0 · top_p 0.95 · top_k 20 · presence 1.5 · seed 42, thinking 상한 = 서버 answer_room(6,144) |

## 지금까지의 결과 (탐색 수치)

| 단계 | 결론 | 근거 |
| --- | --- | --- |
| X0 컨텍스트 지원 | 8K · 16K · 32K 모두 기동 · 응답, OOM 없음 | 원장 `x0_*` |
| X1 설정 효과 | 32K 설정은 8K 대비 TG 약 10~15% 낮음 (처리량 시험) | [`reports/x1-summary.md`](reports/x1-summary.md) |
| XB 출력 예산 | 8K 만 12/12 통과 — 서버가 max_tokens 의 1/4 을 답변 몫으로 두고 thinking 을 닫는다 | [`reports/xb2-summary.md`](reports/xb2-summary.md) |
| X2 입력 길이 | 입력 24K 까지 답변 100%, 테스트 통과 20/24, TG 77→50 tok/s, SSD 0 | [`reports/x2-summary.md`](reports/x2-summary.md) |
| B1-1 thinking 상한 | 짧은 과제는 3K 상한이 12/12 · 첫 답변 37초(TG 같음) — 탐색 과제에서는 품질 −2/15 라 쓰지 않음 | [`reports/b1t-summary.md`](reports/b1t-summary.md) |
| X3 긴 문맥 코딩 | 입력을 다 넣으면 16K 이상 첫 답 6/6 실패 → 필요한 파일만 찾아 읽는 navigate 하네스로 간다 | [`reports/x3-harness-summary.md`](reports/x3-harness-summary.md) |
| X3 하네스 A/B | v1 0/5 → `edit_file` 도구 4/5. **H1 페이지 나누기 품질 +2/15**, **H2a reasoning 재전송 품질 같음 · 시간 −31% · 재읽기 −83%** | 같은 보고서 |
| API 도구 왕복 | Chat · Messages(Claude Code) · Responses(Codex) x 스트림 12/12 | `experiments/probes/` |

알게 된 제약: q36 경로 KV 는 FP32 고정(`--kv` 미적용), MTP 초안은 greedy 단독 요청에서만, 같은 세션 후속 턴은 이전 답을 reasoning 없이
보내면 캐시 재사용 0(매 턴 전체 재읽기, T-013). 문제와 해결 기록은 [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md)(T-001~T-014).

| 단계 | 상태 |
|---|---|
| 호환성 · 환경 · X0 · X1 · XB · X2 | 완료 |
| B0 기준선 | 처리량만 완료 |
| B1 실행 설정 · X3 하네스 · X4 노트북 경유 | 진행 중 (X4 는 API 왕복만 확인) |
| Q1 맞춤 양자화 · E1 엔진 · C1 결합 · F1 최종 · 64K | 미착수 |

<details>
<summary><b>목표와 범위</b></summary>

첫 답변 지연, 답변 완료 시간, 생성 처리량, VRAM · RAM 사용량을 개선한다. 개선이 검증된 변경만
운영 구성에 반영하고, 개선이 없어도 재현 가능한 기준선과 실패 기록을 남긴다.
사전학습 · 파인튜닝, 외부 공개 서비스, 다중 GPU, 장비 구매는 범위 밖이다.

전체 설계: [`docs/plan-v2.0.md`](docs/plan-v2.0.md) + 변경안 [v2.1](docs/plan-v2.1-amendment-20261118.md) · [v2.2](docs/plan-v2.2-amendment-20261118.md)
</details>

<details>
<summary><b>지키는 규칙</b></summary>

규칙 본문은 [`docs/RULES.md`](docs/RULES.md) 한 곳에만 있다. 요점:

- 엔진은 Niko1221/Strata 고정 커밋 하나, 다른 엔진으로 대체하지 않는다
- 최종 평가 50문항은 후보를 고정하기 전까지 열지 않는다 (`final_eval/` 은 훅이 막는다). 참조 패치 · 비공개 테스트는 모델 입력에 넣지 않는다
- 측정 기준 · 채점기 · 기준선을 바꿔서 수치를 올리지 않는다. 하네스 후보는 요인 하나씩 새 ID 로 비교한다
- 결과는 append-only TSV 원장에 코드가 쓰고, `record` 커밋에 코드를 섞지 않는다. 정정은 [`docs/LEDGER_SCHEMA.md`](docs/LEDGER_SCHEMA.md) 정정 기록에
- 기준선과 후보는 같은 PC · 같은 세션에서 번갈아 잰다
- 비밀값(API 키)은 커밋하지 않는다 — 본체 `.secrets/`(git 제외)와 사용자 환경 변수에만
</details>

## 폴더

| 경로 | 내용 | git |
|---|---|---|
| `docs/` | 기획서 · 규칙 · 작업 흐름 · 원장 스키마 · 트러블슈팅 · 일일 계획 | 커밋 |
| `reports/` | 단계별 요약 (X1 · XB · X2 · B1-1 · X3 하네스) | 커밋 |
| `env/` | 하드웨어 실측 · conda 선언 · 설치 로그 · 낮/밤 모드 기록 | 커밋 |
| `scripts/` | 서버 기동(`serve-ctx.ps1`) · 낮/밤 모드 · 측정 러너(`bench/`) · 노트북 클라이언트(`client/`) | 커밋 |
| `configs/` | 실행 설정 · 평가 과제(`eval/`) | 커밋 |
| `experiments/` | `LEDGER.tsv` 원장, run 별 config · 답 · 도구 · 턴 기록, 점검 원자료(`probes/`) | 커밋 (raw 제외) |
| `tools/` · `tests/` | 훅 본체와 테스트 | 커밋 |
| `engine/` · `data/` · `downloads/` · `work/` · `.secrets/` | STRATA 체크아웃 · 모델 · 설치 파일 · 작업 복사본 · 비밀값 | **제외** |

## 시작하기

```powershell
git clone git@github.com:jinsan02/strata-local-llm.git C:\strata-lab
cd C:\strata-lab
git config core.hooksPath .githooks
```

- Python 은 conda 환경 `strata_local_llm` 을 절대경로로 쓴다 — [`docs/ENVIRONMENT.md`](docs/ENVIRONMENT.md)
- 서버: `scripts\serve-ctx.ps1 -Context 32768` (기본 127.0.0.1, 노트북용 Tailscale 주소는 16자 이상 `STRATA_API_KEY` 가 있어야 열린다)
- 장시간 측정은 노트북 연결과 무관하게 WMI 로 띄운다: `scripts\bench\launch_night*.ps1` (T-012)
- 커밋 형식 [`docs/COMMIT_CONVENTION.md`](docs/COMMIT_CONVENTION.md), AI 에이전트 지침 [`AGENTS.md`](AGENTS.md) (`CLAUDE.md` 는 이것을 불러온다), GitHub 흐름 [`CONTRIBUTING.md`](CONTRIBUTING.md)
