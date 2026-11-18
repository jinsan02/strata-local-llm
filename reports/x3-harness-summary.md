# X3 파일럿 · 하네스 요약 (2026-11-18, 진행 중)

고정: M0(Qwen3.6-35B-A3B UD-Q4_K_XL) · E0(STRATA v0.2.15 `c775728`) · S0 샘플링 · 32,768 · 출력+thinking 8,192 · 단일 슬롯 ·
pypa/packaging `6a69a83` · SWE-bench Verified 리비전 `78f471bf`(로컬 conda 채점, 공식 Docker 하니스 아님). 모든 수치는 1회 파일럿(탐색)이다.

## 1. preload — 입력 길이 효과 (원장 `x3q_*`)

필수 파일 + 무관한 패딩 파일, 첫 답 실패 시 테스트 로그로 1회 보완.

| 과제 | 필수 파일만 (6.8K~11K) | 16K | 24K |
| --- | --- | --- | --- |
| dg_group_names | **통과** 14/14 (111초) | 실패 5→6/14 | 실패 4→4/14 |
| marker_extras | import · 문법 오류 0/11 | 새 테스트 11/11, 회귀 깨짐 | 1차 오류 → 보완 후 11/11 (`pass_partial_apply`) |
| version_bump | **통과** 16/16 (125초) | 새 테스트 16/16, 회귀 깨짐 | import · 문법 오류 0/16 |

입력이 16K 를 넘으면 첫 답 6건이 모두 실패했다(새 테스트는 통과하고 회귀 깨짐 2, import · 문법 오류 2, 새 테스트 실패 2). 보완 턴으로 바뀐 것은 1건.

## 2. navigate — 하네스 문제와 수정

| 버전 | 바꾼 것 | X3 (3) | SWE (2) | 병목 |
| --- | --- | --- | --- | --- |
| v1 | 읽기 도구 3개, 편집은 마지막 답의 텍스트 블록 | 0/3 | 0/2 | 모델이 없는 `SEARCH` 도구를 텍스트로 호출(4/5) → 서버가 미선언 호출을 거부 → `no_edit` (T-011) |
| v2 | `edit_file` 도구 + 텍스트 호출 1회 재요청 | **2/3** | **2/2** | dg 는 22회 호출 뒤 강제 종료 턴, 마지막 입력 19~22K (강제 기준 22,272 근처) |
| v3 = **H0** | 깨진 JSON 인자 거부 · 오류 난 읽기 제외 · `count_tokens` 로 요청 전체 입력 계산 · 턴별 캐시 · wall_ms | 측정 중 | 측정 중 | — |

v2 상세 (원장 `x3n_*` · `x3sn_*`): marker 11/11 (도구 10회, 242초) · version 16/16 (7회, 121초) · dg 4/14 (22회, edit_file 실패 2, 446초) ·
flask F2P 1/1 · P2P 59/59 (3회, 16초) · pytest 1/1 · 59/59 (20회, 183초). 텍스트 도구 호출 0.

## 3. 점검 결과

**도구 왕복** (`experiments/probes/probe_tools_20261118.json`): Chat Completions · Anthropic Messages(Claude Code) · OpenAI Responses(Codex) x
비스트림 · 스트림 x 2회 = **12/12 통과**. 텍스트 → 도구 호출 → 같은 ID 결과 → 후속 답에 결과 값. 스트림 인자 8조각 조립 정상. API 변환 단계 문제 없음.

**후속 턴 재사용** (`probe_cache_20261118.json`, 2회 재현, T-013):

| 변형 (요인 하나) | 요청 2~4 cached | 비고 |
| --- | --- | --- |
| 도구 목록 유지 (기준) | 0 · 0 · 0 | 앞부분이 같아도 재사용 없음, 8.8K 프롬프트 첫 스트림 약 6초 |
| 마지막 턴 도구 목록 뺌 | 0 · 0 · 0 | 차이 없음 |
| 작업 폴더 정보 · 시각 변경 | 0 · 0 · 0 | 차이 없음 |
| 이전 답 reasoning 없이 | 0 | — |
| **이전 답 + reasoning_content** | **451 · 479** | 직전 프롬프트 + 생성분까지 재사용 |

서버 측정값: `prompt_tokens_details.cached_tokens` · `timings.cache_n/prompt_n` (Chat), `cache_read_input_tokens` (Messages),
`input_tokens_details.cached_tokens` (Responses). 서버가 안 주는 값은 NA 로 둔다.

## 4. A/B (밤 체인, 진행 중)

H0 vs H1(도구 응답 페이지 나누기: read_file 약 2,500토큰 단위 + 이어 읽기 안내, grep 경로:줄 + 앞 줄 + 총 건수, 도구 정의는 동일) 을
번갈아 3회, 과제 5개. 판정 순서: 테스트 통과 · 회귀 → 같으면 wall_ms · 새로 읽은 입력. 결과는 연결 재개 뒤 이 절에 채운다.

## 5. 다음에 바꿀 한 가지

**H2: 이전 assistant 답에 reasoning_content 를 붙여 보낸다** — 지금은 매 턴 전체(1만~2만 토큰)를 다시 읽고, 이 하나만 재사용을 만든다.
그다음 Q15 `run_tests` 도구(실패 로그 → 재수정 흐름), X4 기준선(Claude Code CLI · Codex CLI).
