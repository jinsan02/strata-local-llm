# 설정 고정 점검 (2026-11-19, STRATA v0.2.15 c775728 · M0 · 클라이언트 run_x3/run_bench)

목적: 잡음 배제. 결과에 영향을 주는 모든 설정을 찾아 (a) 지금 값, (b) 어디서 정해지는지, (c) 고정 방법을 적는다.

## 1. 샘플링 (클라이언트가 요청마다 명시 — 이미 고정)

| 키 | 값 | 출처 | 비고 |
| --- | --- | --- | --- |
| temperature | 1.0 | `run_bench.SAMPLING` | 모델 카드 '일반 thinking' 세트. 카드의 **정밀 코딩 세트는 0.6** |
| top_p | 0.95 | 같음 | |
| top_k | 20 | 같음 | 엔진 상한 64 |
| presence_penalty | 1.5 | 같음 | 카드 코딩 세트는 **0**. 서버가 창 penalty_last_n=64 를 덧붙임(요청이 안 주면) |
| seed | 42 | 같음 | 엔진은 요청마다 `mt19937_64(seed)` 새로 시작 |
| min_p · repetition · frequency | 끔 | 기본 | |

→ 샘플링은 이미 고정돼 있다. 그런데도 같은 과제가 회차마다 다르게 나온다 = **잡음의 원인은 수치 비결정성**(아래 2절)이고, temperature 1.0 이 그 작은 차이를 크게 키운다.

## 2. 수치 비결정성 후보 (seed 로 막을 수 없음)

| # | 원인 | 확인 방법 |
| --- | --- | --- |
| N1 | 하이브리드 expert: 같은 expert 가 VRAM 슬롯에 있으면 GPU 커널, 없으면 CPU 커널 → 부동소수점 결과가 다름. 슬롯 내용은 앞선 요청 이력에 따라 달라짐 | D0: 같은 요청 반복, 슬롯 상태 다르게 |
| N2 | `--expert-vram` 자동: 시작 때 빈 VRAM 으로 슬롯 수 결정(63) → 다른 앱이 VRAM 을 쓰면 슬롯 수가 달라짐 | 서버 로그 슬롯 수 기록, 명시 고정 |
| N3 | 앞부분 재사용(캐시) 대 처음부터 처리: prefill 경로와 decode 경로 수치가 다름 | D0: 같은 프롬프트 cold vs 재사용 |
| N4 | MTP 2 draft 검증: 검증 배치 크기에 따라 수치가 달라질 수 있음 | D0: --mtp 0 vs 2 출력 비교 |
| N5 | GPU 원자 연산 · 스트림 순서 | D0: 같은 상태에서 3번 반복 |

## 3. 서버 동작 (기본값으로 켜져 있는 것 — 명시 고정 대상)

| 키 | 지금 | 영향 |
| --- | --- | --- |
| answer_room | 켜짐 | max_tokens 8192 이면 thinking 을 **6,144 토큰에서 닫음** |
| reasoning_budget_tokens | 없음 | |
| reasoning_effort | 없음(주입 없음) | |
| reasoning_loop_recovery | 꺼짐 | 켜지면 반복 감지 때 temperature · penalty 를 올림 |
| reasoning_close_retry | 꺼짐 | |
| repeat_stop_tokens | 256 | 같은 내용 256 토큰 반복 시 멈춤 |
| tool_call_recovery | 켜짐 | 깨진 도구 호출 복구 |
| undeclared_tool_calls | text (env STRATA_UNDECLARED_TOOL_CALLS 로도 바뀜) | |
| fit_max_tokens | 켜짐 | max_tokens 를 남은 문맥에 맞게 줄임 |
| Chat 공유 설정 | 없음 | `engine/strata-qwen36-ctx<N>.shared-settings.json` 이 생기면 **모든 요청 기본값이 바뀜**(웹 UI POST /settings) |
| anthropic_thinking | model | Claude Code 경로(X4)에서만 |

## 4. 엔진 인자 (base config)

`--native <M0> --max-context N --prefill auto --mtp 2`, parallel 1. expert-vram · expert-slots · cpu-threads · batch · hybrid-rows 는 자동.
env: STRATA_Q36_NO_MMQ · STRATA_EXPERT_I8 · STRATA_PENALTY_PROMPT 미설정(기본). 시스템 · 사용자 env 에 STRATA_* 는 API 키뿐.

## 5. 모델 · 템플릿 · 토크나이저

M0 sha256 55983c5a…(run_x3 에 고정), chat_template.jinja(serve) sha256 12827f24…, pack 토크나이저(chat_template.jinja 8,057B · vocab · merges).
thinking 켜짐(템플릿 기본). 시스템 프롬프트 · 과제 설명은 한국어.

## 6. 그 밖

| 항목 | 지금 | 고정 |
| --- | --- | --- |
| 전원 구성표 | 고성능 | 체인 시작 때 확인 |
| GPU | 드라이버 616.92, 전력 한도 300W, 최대 SM 3090MHz | nvidia-smi 1분 기록(합의 B-5) |
| Defender 빠른 검사 | 매일 02:00 | 밤 체인 시간과 겹침 → 시간 기록 · 속도 해석 때 제외 |
| 채점 env | x3_packaging (pytest 버전) | `pip freeze` 해시를 원장 env 에 |
| 클라이언트 | run_x3 · run_bench 커밋 | 이미 git_commit · config_sha256 |

## 7. 제안

1. **명시 고정(행동 불변)**: 3절 기본값을 config 에 그대로 적고(answer_room · repeat_stop_tokens · tool_call_recovery · undeclared · fit), `--expert-slots 63` 명시, 체인 시작 전 점검(shared-settings 없음 · STRATA_* env 없음 · 전원 · 슬롯 수), 채점 env freeze. 결과는 지금과 같아야 한다.
2. **D0 결정성 탐침(GPU 20분)**: N1~N5 를 같은 요청 반복으로 확인 → 잡음이 어디서 오는지 숫자로.
3. **S1 샘플링 후보(정확도 A/B)**: 카드의 정밀 코딩 세트(temperature 0.6 · presence 0) vs 지금(1.0 · 1.5). 정확도 · 잡음 둘 다 바뀔 수 있으므로 하네스 A/B 보다 먼저 확정해야 '두 번 일' 을 피한다.

## 8. 11-19 저녁 관찰: 같은 설정 · 새 서버면 회차가 똑같다

ctx64 체인 X3 에서 같은 ctx 의 3회가 비트 단위로 같은 궤적(도구 호출 · 입력 토큰 · 점수). 수치 비결정성 후보 중
N5(원자 연산 순서)는 이 조건에서 결과를 바꿀 만큼 크지 않고, N1 · N2(슬롯 수 = 하이브리드 배치)는 결과를 바꾼다(32K 63 vs 64K 42 에서 dg 과제가 갈림).
N3(재사용 vs 처음부터)은 D0 탐침에서 확인. 대응: 반복 측정은 `--seed-per-rep` 로 회차마다 seed 를 바꾼다(decisions-20261119b D).
