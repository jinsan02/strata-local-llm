# 커밋 규칙

집행 코드는 [`tools/check_commit_msg.py`](../tools/check_commit_msg.py),
훅은 [`.githooks/commit-msg`](../.githooks/commit-msg). 규칙과 코드가 어긋나면 코드가 맞다.
형식은 [jinsan02/kotokenlab](https://github.com/jinsan02/kotokenlab) 의 규칙을 이 실험에 맞게 옮겼다.

```
<type>(<scope>): <제목>

<본문 — 무엇을 했는지가 아니라 왜 했는지>

<트레일러 — 기계가 읽는 계보>
```

- 제목 줄 전체 **72자 이하**, 끝에 마침표 없음. 제목은 한국어 평서문("~한다")
- 제목과 본문 사이 **빈 줄 필수**
- 트레일러는 메시지 **마지막 블록**에 `Key: value` 형태로
- 에이전트가 쓴 커밋은 마지막 줄에 `Co-Authored-By:` 를 남긴다

---

## type

| type | 언제 | 필수 트레일러 |
|---|---|---|
| `record` | **측정·평가 결과 기록**. 원장 행 + 요약 산출물 | `Run-Id`, `Ledger`, `Config-SHA256` |
| `fix` | 잘못된 동작을 고침 | `Invalidates` |
| `upgrade` | 기존 기능 개선. 동작은 그대로, 속도·정확도·구조가 나아짐 | — |
| `feat` | 새 구성요소·스크립트 추가 | — |
| `model` | 모델·양자화 산출물 등록 (M0, M1 ...) | `Model-SHA256` |
| `docs` | 문서 | — |
| `chore` | 환경·설정·의존성·훅 | — |
| `revert` | 되돌리기 | — |

`fix` 와 `upgrade` 의 경계: **결과가 틀렸었나?** 틀렸으면 `fix`, 맞았는데 더 나아졌으면
`upgrade`. `fix` 는 과거 측정을 무효화할 수 있으므로 `Invalidates` 를 요구한다.

## scope

`env` `engine` `config` `quant` `bench` `eval` `infra` `docs`

| scope | 기획서 단계 |
|---|---|
| `env` | 실행 환경 — 하드웨어 기록, 툴체인, conda, 정리 스크립트 |
| `engine` | STRATA 엔진 고정·빌드·패치 (E0, E1) |
| `config` | 실행 설정 탐색 (S1) |
| `quant` | 맞춤 양자화 (M1) |
| `bench` | 성능 측정 (PP · TG · 지연 · 메모리) |
| `eval` | 품질 평가 (탐색 세트 · 최종 50문항 절차) |
| `infra` | 훅 · CI · 공용 도구 |
| `docs` | 문서 |

---

## 트레일러

| Key | 형식 | 의미 |
|---|---|---|
| `Run-Id` | `bench_b0_m0_e0_s0_ctx8k` | **`experiments/LEDGER.tsv` 에 실재해야 한다.** 훅이 확인한다 |
| `Ledger` | 쉼표 구분 경로 | 이 커밋이 행을 추가한 원장 파일들. 존재해야 한다 |
| `Config-SHA256` | 소문자 64 hex | run 의 config 해시. 원장 값과 같아야 한다 |
| `Model-SHA256` | 소문자 64 hex | 모델 파일(또는 팩 인덱스) 해시 |
| `Engine-Commit` | 40 hex | 선택. 엔진 패치·빌드를 가리킬 때 |
| `Invalidates` | `none` 또는 run_id 목록 | 이 수정으로 **무효가 된** 과거 측정 |

---

## 강제 규칙

### 1. `record` 커밋은 코드를 건드릴 수 없다

허용되는 경로: `experiments/`, `reports/`, `docs/`

`tools/`, `scripts/`, `configs/`, `.githooks/` 가 함께 스테이지되면 훅이 거부한다.
"수치가 좋게 나오도록 코드를 조금 고치면서 같이 커밋"하는 경로를 없애기 위해서다
(기획서 5.1, [RULES.md](RULES.md) 4번). 코드를 고쳐야 한다면 먼저
`fix`/`upgrade`/`feat` 로 커밋하고, 그 뒤에 다시 측정해서 `record` 한다.

### 2. `fix` 커밋은 `Invalidates` 를 반드시 적는다

`none` 이라고 적는 것도 허용한다 — 다만 **한 번은 생각해야** 적을 수 있다.
적힌 run_id 는 `LEDGER.tsv` 에 있어야 한다.

### 3. 훅과 CI 는 같은 트리를 본다

훅은 작업 트리가 아니라 **인덱스** 를 읽는다 (`check_commit_msg.py --staged`).
원장 행을 아직 스테이지하지 않은 채로 그 run 을 `Run-Id`/`Invalidates` 에 적으면
로컬에서 먼저 막힌다. 순서는 둘 중 하나다:

- 원장 행을 **같은 커밋에** 함께 스테이지한다, 또는
- 원장 행을 **먼저** `record` 로 커밋하고, 그 다음 커밋에서 참조한다

---

## 예시

```
record(bench): B0 기본 설정 8K 단일 요청 기준선

배포 기본값(parallel 2)과 기획 조건(parallel 1)을 같은 날 교차로 쟀다.
입력 512·2,048·4,096, 출력 128·512, 반복 3회.

Run-Id: bench_b0_m0_e0_s0_ctx8k
Ledger: experiments/LEDGER.tsv
Config-SHA256: <원장에서 읽은 값>
```

```
fix(bench): 첫 답변 지연에 reasoning 조각이 섞이던 오류 수정

reasoning 을 먼저 보내는 모델에서 첫 스트림 지연을 첫 답변 지연으로 기록했다.

Invalidates: bench_b0_m0_e0_s0_ctx8k
```

```
model(quant): M1 attention Q6_K · expert Q4_K 혼합 정밀도 등록

Model-SHA256: <파일 해시>
```

```
chore(env): CUDA 13.2.2 와 VS 2022 Build Tools 를 설치한다
```

---

## 브랜치

| 패턴 | 용도 |
|---|---|
| `main` | 항상 초록. 훅을 통과한 것만 들어온다 |
| `exp/<phase>-<slug>` | 실험. 예 `exp/config-expert-cache`, `exp/quant-m1-attn-q6` |
| `fix/<slug>` | 버그 수정 |
| `docs/<slug>` | 문서 |

Codex 와 Claude Code 를 비교할 때는 도구별로 브랜치를 나눈다 (기획서 5절).

## 태그 — 되돌릴 수 없는 결정 지점

| 태그 | 의미 |
|---|---|
| `m0-e0-freeze` | 기준 모델 M0 · 엔진 E0 · 평가 조건 고정 (기획서 3.3-5) |
| `eval-freeze-v1` | 측정·채점 도구 고정. 이후 변경은 `-v2` 이고 기준선을 다시 잰다 |
| `final-eval-opened` | **최종 50문항을 처음 연 커밋** (기획서 8.1) |

`final-eval-opened` 이후에 한 튜닝은 독립 평가가 아니다. 새 보류 세트를 마련한다.

---

## 훅이 막는 것

| 훅 | 검사 |
|---|---|
| `commit-msg` | 제목 형식 · type/scope 화이트리스트 · 72자 · 마침표 · 빈 줄 · 필수 트레일러 · sha256 형식 · `Run-Id`/`Invalidates` 실재 여부(**인덱스 기준**) · `Config-SHA256` 원장 대조 · `Ledger` 경로 실재 · `record` 커밋의 코드 변경 |
| `pre-commit` | 5MB 초과 · 모델 바이너리(.gguf 등) · 금지 경로(`engine/` `data/` `downloads/`) · **`final_eval` 경로** · `.ipynb` 출력 셀 · 원장 무결성 |

훅 연결: `git config core.hooksPath .githooks` (클론 직후 한 번).
`--no-verify` 는 쓰지 않는다 ([RULES.md](RULES.md) 10번).
