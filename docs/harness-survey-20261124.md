# 하네스 엔지니어링 조사 · 우리 하네스와 비교 (2026-11-24)

외부 자료(논문 5편, 실무 글 4편, 공개 저장소)를 읽고 우리 하네스(H9 기준: M0 · E2 · 64K · high · card-coding · H7 lenient · H9 strip)와 비교했다.
기존 기록(LEDGER x3h9 · y9 · x3h9t · y9t 각 30회)으로 바로 재 볼 수 있는 것은 재 봤다. 수치는 출처 그대로이고, 2차 요약에서 온 것은 표시했다.

## 1. 바로 걸리는 근거 두 편

| 출처 | 내용 | 우리에게 |
|---|---|---|
| *Same Model, Different Harness* (arXiv 2608.26218, 2026-08-26) | **같은 모델 Qwen3.6-35B-A3B Q4_K_XL · llama-server.** 오래된 도구 결과를 나이에 따라 줄이고(창 절반부터, 최근 4개는 그대로, 오래된 것은 앞 · 뒤만, 나이가 두 배면 상한 절반) 멈춤 감지 · 명령 안전장치를 더함. SWE-bench Verified 20,480 창에서 F2P 28% → 49%, Pro 49,152 창에서 15% → 33%. **262,144 창에서는 −0.3pp(차이 없음).** 턴 · 시간은 늘어남 | 창이 좁을 때만 크게 듣는다. 우리 64K 에서 x3h9 최대 입력은 중앙값 27,015 · 최대 43,419, y9 는 13,502 · 50,116. 강제 마지막 턴 문턱(55,296)에 닿은 적이 없다 → **64K 에서는 이득이 작을 것으로 본다.** 32K 로 내려 속도를 얻으려 할 때(E2a 생성 속도 8K 66 · 40K 53 tok/s) 다시 볼 후보 |
| *An Empirical Study of Harness Design for Coding Agents* (arXiv 2609.20804, 2026-09-17) | Nemotron-3 30B · 120B · 550B 등, SWE-bench Verified. **30B: 도구 묶음 25.20 vs bash 만 10.20, 계획 있음 25.20 vs 없음 13.60.** 큰 모델은 bash 만이 오히려 낫다(550B 69.40 vs 65.80). 편집은 old/new 정확 치환 · 한 곳 일치 · 읽은 뒤 쓰기, 편집 뒤 ruff · pyflakes 진단, 같은 호출 5번이면 경고 · 8번이면 종료 | 작은 모델은 **타입 있는 도구**가 필수 → 우리 워커 설계가 맞다. X4 A 4/16(Read · Edit 만)과 같은 방향. **계획 단계는 우리에게 없다** |

## 2. 코드(하네스) — 적용 후보

| # | 방법 | 외부 근거 | 우리 상태 | 판단 |
|---|---|---|---|---|
| C1 | **편집 뒤 정적 진단을 되돌려 줌**(pyflakes: 정의 안 된 이름 · 안 쓰는 import · 잘못된 import, 막지 않고 알려만 줌) | 2609.20804 편집 뒤 ruff/pyflakes, Aider 문법 → 컴파일 → flake8, OpenCode 매 편집 LSP 진단 [2차 요약] | T1 은 파싱 실패만 막음(기각 · 보류), H10 b 는 lenient 적용이 파싱을 깨면 거절. 이름 · import 오류는 못 잡음. X4 실패 중 import 오류 2건, X3 · Y 의 import_or_syntax 류 | **1순위.** 싸고 일반적. 실패 기록에서 pyflakes 가 잡았을 건수를 먼저 재현으로 센다 |
| C2 | **계획 도구**(todo 최대 10개, 진행 중 1개) | 30B 계획 25.20 vs 13.60. NanoHarness 는 계획 단독 수치 없음 | 없음. 단계 상한 20 에 X3 중앙값 19 단계(거의 꽉 참), 실패는 탐색에 단계를 씀 | **2순위.** 단, AHE(2604.25850)에서 "시스템 프롬프트만 바꾸기"는 유일하게 퇴보(67.4 vs 69.7) → 문구가 아니라 **도구**로 넣는다 |
| C3 | 오래된 도구 결과 줄이기 | 위 1절 | 글자 수 자르기 12,000(H0), H1 paged 기각 | 64K 에선 보류. 32K 재검토 때 후보 |
| C4 | 같은 호출 반복 감지(5회 경고 · 8회 종료) | 2609.20804, Gemini CLI 5회, Hermes 2회 경고 · 8회 정지 [2차 요약] | C1 재읽기 가드 기각(48회 19 vs 19) | 낮음. 단계 상한 20 이라 8회 반복까지 갈 일이 드묾 |
| C5 | k번 시도 → 공개 회귀 테스트로 고르기 → 다수결 (Agentless) | Agentless 후속 연구: 회귀 · 재현 테스트를 고르기에 넣으면 위치 찾기 방법과 무관하게 좋아짐(선택 단독 효과 수치는 이번에 확인 못 함) | **기존 기록으로 재현함: 효과 0.** x3h9 · y9 60회 모두 회귀 테스트 통과, 실패는 전부 "회귀는 통과 · 숨은 테스트 실패"(x3h9 6, y9 9). k=1·2·3 → 24 · 24 · 24, 21 · 21 · 21. run_tests 켠 묶음도 21 → 21.5, 22 → 22.8 | **회귀로 고르기는 버린다.** 이득은 모델이 쓴 재현 테스트에서 나오는데, 우리 모델은 테스트 쓰기가 약하다(y3 0/5 → A안 3/5). 다수결도 과제별 통과율이 반을 넘는 과제에서만 도움 |
| C6 | 끝내기 전 확인 강제(finish 훅) | AHE 진화 결과의 finish 훅, Hermes verify-on-stop [2차 요약] | H8 게이트(20/30, 보류) | 보류 유지 |
| C7 | 클라이언트 도구 묶음 | 위 1절, X4 원인 | `CLAUDE_CODE_SIMPLE=1` 은 Bash · Read · Edit 만 남김 | 본체 X4b 는 Bash 허용으로 해결. 노트북은 SIMPLE 을 끈 조건(프롬프트 15.6K 토큰, 64K 에서 감당 가능)을 따로 잰다 |

## 3. 규칙 세팅 — 적용 후보

| # | 방법 | 외부 근거 | 우리 상태 | 제안 |
|---|---|---|---|---|
| R1 | **글 규칙을 기계 검사로**: 커밋 메시지 · 비밀값 · 금지 경로를 git 훅으로 | Marmelab: 공개 CLAUDE.md 481개의 보안 규칙 중 실제 통제가 있는 것 4.4%, deny 규칙 커밋 12/391 [2차 요약]. OpenAI · Fowler: 규칙은 린터 · 구조 테스트로 | **이미 있다**(처음 보고에서 없다고 잘못 적음, COLLAB-LOG C-038): `.githooks/commit-msg`(제목 72자 · record 트레일러를 원장과 대조 · fix 의 Invalidates) · `pre-commit`(final_eval · engine · data · 모델 바이너리 경로), `core.hooksPath` 로 켜짐. 빠진 것: 비밀값(키 값) 검사 · 한국어 .ps1 BOM 검사. 이번 push 전 키 검사는 손으로 함 | `tools/precheck.py` 에 키 값(`.secrets` 의 값과 일치하는 문자열) · .ps1 BOM 검사를 더하고 막는 경우 · 통과하는 경우를 selftest 로 |
| R2 | **실패 메시지에 고치는 방법을 넣기** | OpenAI(린트 오류에 해결 지시), Fowler "좋은 쪽의 프롬프트 주입" | 하네스 편집 실패 안내는 이미 그렇다(H6 · H9 · H10) | 훅 메시지도 "무엇이 틀렸고 어떻게 고치나"로 |
| R3 | 루트 지시 파일은 약 100줄 지도, 세부는 docs/ | OpenAI 약 100줄, 공개 저장소 중앙값 123줄 [2차 요약] | 루트 `CLAUDE.md` 7줄 · `experiments/AGENTS.md` 122줄 · `RULES.md` 129줄은 적당. **`STATE.md` 242줄 · 50KB**(한 줄이 수백 자)가 무겁다 | STATE 를 "지금 상태 · 다음 할 일"(약 80줄)과 날짜별 기록 보관 파일로 나눔 |
| R4 | 기계가 만든 맥락 파일은 피하고 사람이 쓴 것만 | ETH Zurich(138과제): 생성 파일은 성공률 하락 · 비용 20%+, 사람이 쓴 것 +4% [2차 요약] | 워커 지시문은 사람이 씀 | 유지. 워커에 저장소 요약을 자동 생성해 넣는 일은 하지 않음 |
| R5 | 실패에서 규칙 만들기 | Fowler 조종 루프, flow-next 실패 기록 98건 | `string-layer-checklist` · COLLAB-LOG 로 하고 있음 | 유지. 반복되면 R1 훅으로 승격 |

## 4. 환경 세팅 — 적용 후보

| # | 방법 | 외부 근거 | 우리 상태 | 제안 |
|---|---|---|---|---|
| E1 | **세션 시작 점검 스크립트** | Anthropic: init.sh + 진행 파일 + git log 를 먼저 읽고 기본 동작 확인 | STATE 를 먼저 읽는 습관만, 이번에 `strata-status.ps1` 생김 | `session-start.ps1`: git 상태 · 안 올린 커밋 · 도는 체인/일괄 · 서버 · RAM · STATE 앞부분. 한 번에 |
| E2 | 할 일 목록을 JSON 으로 | Anthropic: 모델이 Markdown 보다 JSON 을 덜 고쳐 씀(관찰, 수치 없음) | STATE 의 "다음 할 일" 번호 목록 | E1 과 같이, 상태 필드만 바꾸는 `todo.json` (선택) |
| E3 | 고정 과제로 한 번에 하나만 바꿔 평가, 과제 20~50개 | Marmelab 정리 [의견], AHE 도 한 커밋에 한 변경 | RULES 12 · Y 세트로 하고 있음. **과제 12개**(X3 6 · Y 6) | 과제를 20개 이상으로 늘리는 게 과적합 위험을 가장 직접 줄임 |
| E4 | 실행마다 격리된 작업 복사본 · 사용 기록 | OpenAI 워크트리별 실행, 사용 기록 남기는 저장소 5/391 [2차 요약] | fresh_copy · 워커 worktree · LEDGER · results.jsonl | 이미 앞서 있음. 유지 |
| E5 | 빠른 테스트 루프 | Marmelab 테스트 시작 1초 이내 [의견], Fowler 빠른 검사는 커밋 전 | version_bump 회귀 51,524개 · 21.6초 | 모델이 돌리는 테스트는 관련 파일만(이미 run_tests 는 파일 지정). 회귀 전체는 채점에서만 |

## 5. 결론 — 해 볼 순서

1. **C1 편집 뒤 pyflakes 진단**: 먼저 지난 실패 편집에 pyflakes 를 돌려 잡혔을 건수를 센다(재현, 서버 불필요) → 의미 있으면 H11 로 30회.
2. **R1 훅 보강**: 이미 있는 pre-commit 에 키 값 · BOM 검사만 더한다. 측정과 무관, 바로 가능.
3. **E1 세션 시작 스크립트**: 30분 일.
4. **C2 계획 도구**: 1 다음 측정 후보.
5. 보류: C3(32K 재검토 때), C4 · C6. 버림: C5 회귀 기반 고르기(재현 결과 0).

## 출처

- [Same Model, Different Harness (arXiv 2608.26218)](https://arxiv.org/abs/2608.26218)
- [An Empirical Study of Harness Design for Coding Agents (arXiv 2609.20804)](https://arxiv.org/abs/2609.20804)
- [Beyond the Model: Demystifying Harness Effects in SE Agents (arXiv 2609.32459)](https://arxiv.org/abs/2609.32459)
- [Harness Engineering: Anatomy ... Eleven Systems (arXiv 2609.00006)](https://arxiv.org/abs/2609.00006)
- [Agentic Harness Engineering (arXiv 2604.25850)](https://arxiv.org/abs/2604.25850)
- [OpenAI, Harness engineering (2026-02-11)](https://openai.com/index/harness-engineering/)
- [Böckeler, Harness engineering for coding agent users (martinfowler.com, 2026-04-02)](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- [Marmelab, The State of AI Harness Engineering 2026 (2026-09-24)](https://marmelab.com/blog/2026/09/24/the-state-of-ai-harness-engineering-2026.html)
- [Anthropic, Effective harnesses for long-running agents (2025-11-26)](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [SWE-agent ACI](https://princeton-nlp.github.io/SWE-agent/background/aci) · [Aider edit formats](https://aider.chat/docs/more/edit-formats.html) · [Agentless](https://arxiv.org/html/2407.01489v2) · [mini-SWE-agent](https://github.com/swe-agent/mini-swe-agent)
