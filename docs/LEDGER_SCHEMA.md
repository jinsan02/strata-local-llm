# 원장 스키마

`experiments/LEDGER.tsv` — 탭 구분, UTF-8, LF, **append-only**.
검사기는 [`tools/validate_ledger.py`](../tools/validate_ledger.py). 열을 바꾸려면 검사기의
`COLUMNS` 와 이 문서를 같은 커밋에서 고친다 (`chore(infra):`).

값이 없으면 `NA` 로 적는다. 빈 칸을 두지 않는다.

| 열 | 의미 |
|---|---|
| `ts_utc` | 행을 쓴 시각 (ISO 8601, `Z`) |
| `run_id` | 소문자·숫자·`_.-`. 예 `bench_b0_m0_e0_s0_ctx8k` |
| `config_id` | 구성 ID: `B0` `B1` `Q1` `E1` `C1` `F1`, 변경안의 `X0`~`X4` |
| `phase` | `env` `engine` `config` `quant` `bench` `eval` |
| `status` | `start` · `ok` · `fail` |
| `origin` | 요청을 보낸 곳: `local`(본체 로컬 API) · `laptop`(Tailscale 경유, 네트워크 포함). 섞어 비교하지 않는다 |
| `workload` | 입력 종류: `fixed-512` `fixed-2048` `fixed-4096`(X1), `code-short` `code-files` `code-session` `code-max`(X2), `quality-<세트>`(X3) |
| `model_id` | `M0`, `M1` … |
| `model_sha256` | 모델 파일(또는 팩 인덱스) sha256 |
| `engine_commit` | STRATA 커밋 해시 (E0 = 고정 커밋, E1 = 패치 브랜치 커밋) |
| `settings_id` | 실행 설정 ID (`S0` 기본, `S1` 튜닝 …) |
| `ctx` | 서버 컨텍스트 설정 (토큰): 8192 · 16384 · 32768 · 65536 |
| `parallel` | 동시 요청 슬롯 수 |
| `kv` | KV 형식: `int8`(기본) `q4_0` `k8v4` `fp16` |
| `mtp` | `on` · `off` |
| `thinking` | `on`(모델 기본) · `off` |
| `cache_state` | `cold` · `warm` (프롬프트 캐시·OS 파일 캐시) |
| `input_tokens` | 템플릿 포함 실제 입력 토큰 수 (서버 보고값) |
| `max_tokens` | 요청의 출력+reasoning 예산. `input_tokens + max_tokens <= ctx` 여야 한다 (러너가 넘으면 실행을 거부) |
| `output_tokens` | 엔진이 보고한 생성 토큰 수 (reasoning + 최종 답변 content 합) |
| `reasoning_tokens` | reasoning 토큰 수. 따로 안 나오면 `NA` 와 `note` 에 이유 |
| `finish_reason` | `stop` · `length` · `tool_calls` … (서버 보고값) |
| `answer_reached` | 최종 답변 content 를 하나라도 받았으면 `1`, 아니면 `0` |
| `tests_passed` | 코딩 과제의 고정 단위 테스트 `통과/전체` (예 `5/5`). 테스트가 없는 처리량 시험은 `NA` |
| `pp_tps` | 엔진이 보고한 입력 처리량 |
| `tg_tps` | 엔진이 보고한 생성 처리량 |
| `ttft_ms` | 첫 스트림(reasoning 또는 content 중 먼저 온 것) 지연 |
| `tt_reasoning_ms` | 첫 reasoning 조각 수신 지연 |
| `tt_answer_ms` | 첫 최종 답변 content 수신 지연. 답이 없으면 `NA` |
| `total_ms` | 요청부터 스트림 종료까지 |
| `peak_vram_mb` | 관측 Peak VRAM (500ms 간격이면 `note` 에 표시) |
| `peak_ram_mb` | 관측 엔진 프로세스 Peak RAM |
| `experts_vram` | expert 캐시 상태: 엔진이 시작할 때 VRAM 에 둔 expert 수 `N/256` (층당) |
| `ssd_read_mb` | SSD 의존도: 서버 `/metrics` 의 요청별 `file_mb` (없으면 엔진 프로세스 디스크 읽기량) |
| `drafts_offered` · `drafts_accepted` | MTP 초안 시도·수락 수. 시도가 0 이면 **`NA` (초안 시도 미기록)** — 0 은 '시도했으나 없음' 과 구분되지 않는다 |
| `git_commit` | 이 저장소 커밋 |
| `git_dirty` | 작업 트리 변경 여부 `0`/`1` |
| `config_sha256` | run config JSON 의 sha256 |
| `env_sha256` | 환경 스냅샷 sha256 |
| `note` | 반복 수·캐시 상태·완료 사유 등 |

## 스키마 이행 기록

| 날짜 | 바뀐 것 | 기존 행 처리 |
| --- | --- | --- |
| 2026-11-18 | `max_tokens` `finish_reason` `answer_reached` `tests_passed` `tt_reasoning_ms` `experts_vram` `drafts_offered` `drafts_accepted` 추가 | `tools/migrate_ledger.py` 로 열 이름 기준 이동, 새 열은 `NA`. 값을 추론해 채우지 않았다 (X0·X1 의 finish·drafts 는 `note` 에 남아 있다) |

run 별 config·env JSON 과 요약은 `experiments/runs/<run_id>/` 에 커밋하고, 원시 스트림·
로그(`raw/`, `*.log`, `*.jsonl`)는 커밋하지 않는다.

## 정정 기록

| 날짜 | 열 | 대상 행 | 원장 값 | 실제 | 근거 |
| --- | --- | --- | --- | --- | --- |
| 2026-11-18 | `kv` | X0 · X1 · XB · XB2 · X2 전 행 (`x0_*` `x1_*` `xb_*` `xb2_*` `x2_*`) | `int8` | `fp32` (+ prompt attention 용 FP16 사본) | 실행 인자에 `--kv` 없음, `q36_engine.cu` 1320~1394 · 1546~1562 행. 측정값은 유효하고 라벨만 틀렸다 (TROUBLESHOOTING T-009) |
