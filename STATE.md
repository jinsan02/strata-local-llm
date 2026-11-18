# STATE.md — 지금 어디까지 왔나

사람과 에이전트(Codex, Claude Code)가 함께 고치는 진행 기록입니다. 작업을 끝낼 때마다 해당 줄을 고치고 '최근 변경' 맨 위에 한 줄 더합니다. 설계 내용 자체는 `docs/`에, 수치는 `experiments/LEDGER.tsv`에, 여기는 상태와 결정만 둡니다.

## 지금

- 마지막 갱신: 2026-11-18
- 단계: **X3 하네스 A/B 1 · 2차 완료 (11-18 21:27, 90행)** — H1(페이지 나누기) 품질 +2/15, H2a(reasoning 재전송) 품질 같음 · 시간 −31% · 재읽기 −83%, H2b · S1T3 제외. **H4(강제 마지막 턴에 edit_file 만 남김) 코드 완료 · 점검 통과(6d18918), 측정은 11-19 에 시작** (`launch_night3.ps1`, 11-18 22:04 에 시작했다가 사용자 결정으로 1분 만에 중단 — 원장 행 없음). 그다음 H3(H1 + H2a). X0 · X1 · XB · X2 · B1-1 · X3 파일럿 완료. 요약 `reports/x3-harness-summary.md`
- 계획: v2.0 + v2.1 + **v2.2** ([`docs/plan-v2.2-amendment-20261118.md`](docs/plan-v2.2-amendment-20261118.md): 1차 실행 설정 → 2차 양자화 → 3차 서버·엔진, 기존 ID 대응표, KV 독립 변수. 9절 = 3차 P0 · HR · E1 후속 전달문)
- 목표: **32K 운영** (입력 24,576 · 출력+reasoning 8,192), 8K 기준선 · 16K 중간 · 64K 선택 — [`docs/plan-v2.1-amendment-20261118.md`](docs/plan-v2.1-amendment-20261118.md)
- 사용 형태: 본체 STRATA 서버를 노트북 코딩 클라이언트(Claude Code · Codex)가 Tailscale 로 부른다. 코드 읽기·수정·테스트는 노트북에서
- 대상 PC: `desktop-5070` (Tailscale 100.121.174.83), 저장소 `C:\strata-lab`
- 실행 환경: conda `strata_local_llm` (Python 3.12, conda-forge), 빌드는 VS 2022 Build Tools + CUDA 13.2.2
- 주 실행자: Claude Code (노트북에서 SSH). Codex 로 비교할 때는 브랜치를 나눈다

## 단계 진행표

기획서 v2.0 6.1·10절 + 변경안 v2.1 6절 기준. 상태: 완료 · 진행 중 · 대기 · 미착수 · 미달

| 단계 | 구성 ID | 컨텍스트 | 상태 | 완료 조건 | 근거 |
| --- | --- | --- | --- | --- | --- |
| 호환성·자원 조사 | — | — | 완료 | 엔진·모델 지원, 메모리·디스크·CPU·PCIe 정보 | `docs/prep-plan-20261118.md`, `env/hw-20261118.md` |
| 환경 준비 | — | — | 완료 | conda · 툴체인 · E0 빌드 · `--plan` · M0 다운로드(해시 일치) | `env/strata-plan-20261118.md`, `env/download-m0.log` |
| 컨텍스트 지원 확인 | X0 | 8K→16K→32K | 완료 | 세 단계 모두 로딩·응답·OOM 없음. VRAM expert 77→73→63/256, TG 약 99→100→92 tok/s (입력 526) | 원장 `x0_*` |
| 기준선 | B0 | 8K | 진행 중 | 처리량 부분 완료(X1 의 8K 행). 품질·최종 답변은 XB 이후. 태그 `m0-e0-freeze` 는 품질까지 본 뒤 | 원장 `x1_*ctx8k*` |
| 설정 효과 (입력 고정) | X1 | 8K·16K·32K | 완료 | **"8K·16K·32K 설정에서 0.5K·2K·4K 입력 성능 측정"** — 처리량 시험, 32K 실사용 검증 아님. 32K 설정은 8K 대비 TG 약 10~15% 낮음, 최종 답변 0건 | `reports/x1-summary.md` |
| 출력·reasoning 예산 단계 | XB | 32K | 완료 (탐색) | 짧은 입력(149~224) 과제 4개 × 2K·4K·8K × 3회: 전부 통과 2K 8/12 · 4K 8/12 · **8K 12/12**. 서버가 max_tokens 의 1/4 을 답변 몫으로 남기고 thinking 을 닫는다(결정 기록) | `reports/xb2-summary.md`, 원장 `xb2_*` |
| 입력 길이 효과 | X2 | 32K | 완료 (탐색) | 입력 2K · 8K · 16K · 24K x 끝/중간 x 과제 4개 x 3회(84행). 전부 통과 2K 11/12 · 8K 23/24 · 16K 21/24 · 24K 20/24, length 0. TG 77→50, 첫 토큰 1.3→17초, 첫 답변 중앙 44→69~85초, SSD 0, RAM 25~26GB | `reports/x2-summary.md`, 원장 `x2_*` |
| 긴 문맥 코딩 품질 | X3 | 32K | 파일럿 완료 · **하네스 A/B 진행 중**. preload(입력 길이): 필수 파일만 2/3 첫 답 통과, 16K · 24K 는 6건 모두 첫 답 실패. navigate v1(읽기만 도구) 0/5 → v2(edit_file, T-011) X3 2/3 · SWE 2/2 | 지시 준수·코드 찾기·수정·테스트 통과·도구 호출 | 원장 `x3q_*` `x3s_*` `x3n_*` `x3sn_*`, `reports/x3-harness-summary.md` |
| X3 하네스 | H0 · H1 · H2a · H2b · S1T3 | 32K | A/B 1 · 2차 완료 (탐색, 각 3회). 15회 통과 H0 12 · 12(두 대조) · **H1 14** · **H2a 11(시간 −31%, 재읽기 −83%)** · H2b 10 · S1T3 10, 회귀 0. 최다 실패 = 강제 마지막 턴 텍스트 편집 블록 불일치 | 채택: v2.2 최종 5쌍 + 확인 전용 과제 D · E · F | 원장 `x3h0_*` `x3h1_*` `x3h2a_*` `x3h2b_*` `x3h0t3_*` (+ `x3s…`), 커밋 0f3e845 · 4ae78a4 |
| 노트북 경유 | X4 | 32K | 착수 전 · API 왕복 확인됨: Chat · Messages(Claude Code) · Responses(Codex) x 비스트림 · 스트림 12/12 (도구 호출 → 같은 ID 결과 → 후속 답, 스트림 인자 조각 조립) | 체감 지연(별도 행), tool calling·템플릿 호환 | `experiments/probes/probe_tools_20261118.json`, 원장 `origin=laptop` |
| 실행 설정 튜닝 | B1 | 32K | B1-1 완료 (thinking 3K 가 짧은 과제 12/12 · 첫 답변 37초, TG 동일). 다음: P-diag 병목 진단 → v2.2 10.3 표로 첫 A/B | S1, 병목 프로파일(KV·expert 캐시·버퍼 경쟁), 후보 순위 | 원장 |
| 맞춤 양자화 | Q1 | 32K | 미착수 | M1 레시피·형식 표·호환성·품질 | 원장 |
| 엔진 최적화 | E1 | 32K | 미착수 | 패치·수치 검사·E1 비교 | 원장 |
| 결합 | C1 | 32K | 미착수 | 단독 효과와 상호작용 | 원장 |
| 최종 검증 | F1 | 32K | 미착수 | 독립 50문항, 재시작 재현, 혼합 50회 · 60분 | 원장 |
| 확장 탐색 | — | 64K | 미착수 | F1 의 32K 통과 뒤에만 | 변경안 3절 |

## 다음 할 일

1. ~~툴체인 검증~~ 완료 (11-18): `cl` 19.44.35230, `nvcc` 13.2.86, CMake 4.1.2, Ninja 1.13.1
2. ~~STRATA E0 빌드~~ 완료 (11-18): v0.2.15 `c775728`, sm_120, `strata.exe` sha256 `907008da…` — `env/strata-plan-20261118.md`
3. ~~`--plan` 결과 저장~~ 완료 (11-18): qwen36 계획기는 다운로드 크기를 모름(실제 22.9GB), coder IQ1_M 은 64.5GB
4. ~~소스 빌드 연결 경로 확인~~ (11-18): `strata launch`(터미널)는 서명된 설치 엔진만 쓴다. 소스 경로는 `setup.py --build`(엔진을 `engine\build` 에 빌드하고 `strata-<model>.json` · `run-<model>.bat` 을 쓴다) → `serve/server.py`
5. ~~M0 다운로드~~ 완료 (11-18): `Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf` 22,853,663,008 B, sha256 일치, HF 리비전 `5bc3e23`
6. ~~X0~~ 완료 (11-18): setup 빌드 → `scripts/serve-ctx.ps1` 로 8K·16K·32K 기동, `scripts/bench/run_bench.py` 로 기록
7. **B0 + X1** (같은 실행으로 겸한다): 고정 문항 입력 512·2,048·4,096 × 출력 128·512 × 컨텍스트 8K·16K·32K, 반복 3회, 같은 샘플링. thinking 이 출력 예산을 다 쓰면 첫 답변 지연이 NA 가 되므로 출력 512 행으로 첫 답변 지연을 본다
8. ~~XB 2차~~ 완료 (11-18 11:09~11:32): 36행. 출력 예산 8K(= thinking 상한 6,144 + 답변 2,048)만 12/12 통과 → X2 는 `--budgets 8192`. 4K 의 parse_duration 실패(10~13/16)는 thinking 이 3,072 에서 강제로 닫힌 탓으로 본다(Q12 에서 확인)
9. ~~X2~~ 완료 (11:44~13:39, 84행): `scripts/bench/matrix-x2.ps1` (입력 2K · 8K · 16K · 24,320 × 끝/중간, 예산 8,192, 3회, 로그 `engine\matrix-x2.log`). 러너: `run_coding.py --ctx 32768 --input-tokens <N> [--position middle] --budgets <XB 결과> --prefix x2` — 저장소 파일(`engine/strata_cli`, `strata_control`)을 붙여 입력 약 2K·8K·16K·한도 근처(32,768 − 예산 − 256)로, 같은 과제·테스트. 러너가 입력+예산 > ctx 를 거부
10. ~~X3 파일럿~~ 완료 (11-18): preload 9 + navigate, SWE 2건 로컬 conda 검증(flask 는 Werkzeug 2.3.7 고정)
11. push: 사용자가 커밋·push 를 맡김(11-18). 단계 커밋 묶음마다 `git push`
12. ~~밤 체인 1차 결과~~ 완료 (0f3e845): H0 · H1 30행, 1차 원장은 인덱스로만 커밋(2차가 쓰는 중)
13. ~~밤 체인 2차~~ 완료 (4ae78a4): H0 r4~6 · H2a · H2b · S1T3 60행.
    **11-19 시작점**: 본체에서 `powershell -File C:\strata-lab\scripts\bench\launch_night3.ps1` (H0 대조 `x3n3h0` vs H4 `x3h4`, 번갈아 3회, 약 1시간 40분, 끝 표시 `engine\night-chain3.log` 의 `[night3] done`) → 로그와 원장 1:1 대조 · 커밋 → 판정. 그다음 **H3** = H1 + H2a (H4 가 통과하면 함께), 그 뒤 `run_tests` 도구(Q15)
14. X4 기준선: 노트북에서 Claude Code CLI · Codex CLI 로 같은 과제(파일 탐색 → 수정 → 테스트 → 실패 로그 재수정), 같은 STRATA 32K. 후보 하나 더면 OpenCode. Hermes 는 64K 뒤
15. 그다음 B1(P-diag → 첫 A/B, Q11 greedy·MTP 포함)
16. 남은 X3 과제 3개(D · E · F) 구현 — 채택 하네스 확인 전용
17. ~~seed 42 반복 독립성~~ 확인 (11-18): 같은 seed 에서도 반복마다 답 · 호출 수가 달랐다(짧은 flask 일부만 같음) → 반복은 독립에 가깝다. 접두사는 체인마다 나눈다(LEDGER_SCHEMA 정정: 공유 폴더 config 덮어씀)

## 사람에게 요청한 것

| 날짜 | 요청 | 상태 |
| --- | --- | --- |
| 11-18 | 전원 구성표를 고성능으로 변경 (측정 위생) | 완료 (11-18 11:41): 고성능 + `scripts/power-max.ps1`(최소 CPU 100% · 코어 파킹 끔 · 부스트 적극 · 디스크·USB 절전 끔 · 최대 절전 끔), 기록 `env/power-*`. **X0 · X1 · XB 는 '균형 조정'에서, X2 부터 고성능에서 쟀다** |
| 11-18 | 양자화 단계 전 페이지 파일 확대 (예: 64GB) | 대기 — Q1 전에. 이유 · 방법은 `docs/plan-20261119.md` 부록 |
| 11-18 | STRATA API 키 설정 | 완료 (Claude 가 생성 · 설정, 값은 `.secrets\` 에만) |
| 11-18 | 커밋 작성자 이메일을 kotokenlab 과 같게 할지 결정 (지금은 noreply) | 완료: 사용자 계정 이메일로 (저장소 로컬 `user.email`, d818a2b 이후 커밋부터). 이전 커밋은 noreply 그대로 |
| 11-18 | 본체 방화벽에 Tailscale 대역만 허용하는 8080 규칙 추가 (명령은 `docs/ENVIRONMENT.md` '노트북에서 호출' 1) | 완료 (본체 규칙 1개, 100.64.0.0/10 · TCP 8080 확인. 노트북에 잘못 만든 규칙은 삭제됨) |

## 결정 기록

| 날짜 | 결정 | 근거 |
| --- | --- | --- |
| 11-18 | **내일 안건 12건 권장대로 (사용자 22시)**: (1) H4 → H3(H1 + H2a, H4 통과 시 포함) 순서, 요인 하나씩 (2) H3 에서 강제 턴 수 · 최대 입력을 같이 본다 (3) 확인 전용 과제 D · E · F 는 GPU 측정 중 CPU 로 구현, 검증(pytest)은 GPU 쉬는 틈에 (4) 최종 채택 = 기존 3 + D · E · F 6과제 x 5회, '품질 같음' 기준은 그때 30회 기준으로 다시 정함 (5) `run_tests` 도구 = 공개 테스트만 · 시간 제한 · 출력은 종료 코드 · 첫 핵심 실패 · 재현 명령 · 전체 로그 위치, H3 다음 후보 (6) T-013 엔진 쪽: STRATA 대화 캐시 체크포인트 옵션을 소스로 확인 → 설정이면 1차 후보, 아니면 3차 (7) X4 는 하네스 확정 뒤, 클라이언트가 thinking 을 되돌려 보내는지 먼저 (8) GPU 배분: 낮 = 하네스, 밤 = B1 P-diag (9) **Q2 권장안 승인** (10) API 키 설정 완료 (11) 페이지 파일은 Q1 전에 사용자가 (12) 체인 끝 자동 밤 모드 유지 | 사용자, `docs/plan-20261119.md` |
| 11-18 | API 키: 본체 `.secrets\strata-api-key.txt`(43자, git 제외) + 본체 · 노트북 사용자 환경 변수 `STRATA_API_KEY`. 키가 걸린 뒤로는 127.0.0.1 서버도 키를 요구(키 없음 · `strata-local` 401, 실제 키 200). 문서 원칙 '파일 금지' 를 사용자 요청으로 'git 밖 파일 허용' 으로 바꿈 | 사용자 요청, `docs/ENVIRONMENT.md` |
| 11-18 | LLMFit(하드웨어 맞춤 모델 · 양자화 추천, 대역폭 기반 추정)은 도입하지 않는다. 추론 · 실험 속도에 영향 없고, STRATA hybrid(expert 일부 VRAM)를 반영하지 못해 X0~X2 실측보다 부정확. Q1(양자화) 후보 대조용으로만 나중에 검토(설치 시 사용자 확인) | 사용자 요청 검토, github.com/AlexsJones/llmfit |
| 11-19 | **토의 12건 권장대로 (사용자)**: (1) H2a · H2b reasoning 재전송 A/B (T-013) (2) 보완 요청은 공개 회귀 로그 + 비공개 통과 수만, 기존 7행 정정 기록 (T-014) (3) 하네스 튜닝은 구현된 3과제로만, 남은 X3 과제 3개(D · E · F)는 채택 하네스 **확인 전용** (4) 이번 3회 A/B 는 탐색, '품질 같음' = 15회 중 통과 수 차이 ≤ 1 이고 회귀 증가 없음, 채택은 v2.2 기준 최종 5쌍 (5) SWE 2건은 하네스 건전성 확인용, 품질 판단 제외(공개 · 유명 저장소라 기억 가능성) (6) X4 기준선은 턴별 cached 부터 기록 (7) `serve-ctx.ps1` 은 루프백 밖으로 열 때 16자 이상 실제 `STRATA_API_KEY` 없으면 거부 (8) 클라이언트 컨텍스트: Codex `model_context_window` 32,768 · 요약 61% · Claude Code `CLAUDE_CODE_MAX_CONTEXT_TOKENS` 이미 고정 — X4 첫 실행에서 실제 CLI 로 확인 (9) `git_dirty` = 코드 · 설정 경로만 (10) Q2 최종 평가 출처를 X4 전에 정한다(권장안 아래) (11) 하네스 확정 뒤 navigate 에서 S1T3(thinking 3,072) 비교 — 밤 체인 2차에 H0 · S1T3 포함 (12) 16K 이상 품질 저하는 길이 vs 방해 코드 미분리 — B1 · X3 후속에서 무관 언어 패딩으로 분리 | 사용자 11-19, 토의 안건 |
| 11-18 | **하네스 비교 원칙**: X3 = 통제된 탐색 · 편집 평가(Chat Completions), X4 = 노트북 클라이언트 실제 흐름 검증. 모델 · 엔진 · 샘플링 · 과제 커밋 · 출력 예산 8,192 · 최대 20턴 · 32K · 단일 슬롯 고정, 후보는 요인 하나씩 새 ID(H0, H1, …). B1-1 상한(Q12)은 미확정이라 양쪽 S0 | 사용자 하네스 지시 |
| 11-18 | **T-011 C안**: navigate 의 쓰기도 도구로(`edit_file`), 텍스트 도구 호출 감지 시 1회 재요청. v1 5행은 fix 커밋 Invalidates | 사용자 결정, v2 재측정 4/5 |
| 11-18 | 서버는 선언되지 않은 도구 호출을 거부하고 텍스트로 둔다(`strata_rejected_tool_calls`). 'SEARCH' 실패는 API 변환이 아니라 모델 도구 선택으로 분류 | `serve/server.py` |
| 11-18 | 본체 장시간 실행은 WMI(`launch_night.ps1`)로 띄운다. ssh 세션이 끝나면 그 세션에서 띄운 서버 · 측정도 꺼진다(T-012) | 11-18 관측 |
| 11-18 | **XB 결론 (탐색)**: 32K 운영의 출력+reasoning 예산은 **8,192** 로 둔다. 2K·4K 는 각각 4/12 실패. 단 STRATA 서버는 thinking 요청에 예산이 없으면 `max_tokens ≥ 1024` 일 때 thinking 을 `max_tokens − max(512, max_tokens/4)` 에서 닫는다(`answer_room`, `serve/server.py:6235`). 그래서 XB 는 사실상 **thinking 상한 시험**이다(2K→1,536 · 4K→3,072 · 8K→6,144). 8K 에서 실제 사용은 2,216~6,512 토큰. 클라이언트의 max_tokens 가 곧 thinking 상한이 된다 | `reports/xb2-summary.md`, 엔진 소스 |
| 11-18 | **MTP 진단 (Q10 종결)**: 활성화·초안 블록 로딩은 됨. v0.2.15 qwen36 경로는 `spec = mtp_d>0 && !smp.needs_logits() && !adm` (`q36_engine.cu:3730`) — logits 가 필요 없는 greedy 단독 요청만 초안을 쓴다. 순수 greedy(penalty 0)에서 158/198 수락(80%), TG 154~162 tok/s. 권장 샘플링(temperature 1.0 + presence 1.5)은 초안 시도 없음, TG 83~108. 서버 `/metrics` 의 drafts 는 계측 누락(엔진이 158/198 을 보고해도 0/0) → 러너는 엔진 로그에서 읽고, 시도 0 은 '초안 시도 미기록'(NA) | 엔진 로그 · 소스 · 프로브 6건 |
| 11-18 | 원장 이행: `max_tokens` `finish_reason` `answer_reached` `tests_passed` `tt_reasoning_ms` `experts_vram` `drafts_offered` `drafts_accepted` 추가. 기존 63행은 열 이동만, 새 열 NA | 사용자 지시 1·2·3·5 |
| 11-18 | 코딩 실사용 성능은 같은 프롬프트에서 최종 답변 + 테스트 통과가 확인된 행만. X1 은 처리량 시험으로만 부른다. 입력+예산 ≤ ctx 를 러너가 강제 | 사용자 지시 4·6 |
| 11-18 | **E0 확정 (Q6 종결)**: `setup.py --build` 가 같은 커밋 `c775728` 로 만든 `engine\engine\strata.exe` (sha256 `dac0229467a62eb6d18b8f54ecfc21b15421978201a8bed1388cc37af8cfc777`, llama.cpp `3cf0325` 포함). 직접 빌드 `build-e0`(`907008da…`)는 참고용. 서버는 `serve/server.py` + `strata-qwen36-ctx<N>.json`(setup 설정에서 `--max-context` 만 바꾼 사본) | setup 이 쓰는 빌드 경로가 운영 경로 |
| 11-18 | 측정 샘플링은 서버의 qwen35moe thinking 권장값(temperature 1.0, top_p 0.95, top_k 20, presence_penalty 1.5, seed 42)으로 고정. X0 8K 3행만 0.6/0.95/20 이라 비교에 쓰지 않는다 | `serve/server.py` 권장 세트 |
| 11-18 | SSD 의존도는 서버 `/metrics` 의 요청별 `file_mb`, MTP 는 `drafts_accepted/offered` 를 원장 `note` 에 남긴다. chat API 는 reasoning 토큰 수를 주지 않아 `reasoning_tokens=NA` (Responses API 로 X3·X4 에서 잰다) | `/metrics` requests 필드 |
| 11-18 | **컨텍스트 목표 변경 (Q7 종결)**: 8K 기준선 · 16K 중간 · **32K 운영 목표**(입력 24,576 · 출력+reasoning 8,192, 초기안) · 64K 는 32K 통과 뒤 선택. 설정 효과(X1)와 입력 길이 효과(X2)를 나눠 잰다. 32K 부적합 시 원인과 16K 운영안을 낸다. M0 는 학습 범위 262,144 라 RoPE 확장 불필요 | 사용자 지시, `docs/plan-v2.1-amendment-20261118.md` |
| 11-18 | 클라이언트 출력+reasoning 예산을 STRATA 권장 4,096 대신 창의 1/4(32K → 8,192)로, Codex 요약 기준은 20,000 으로 둔다 | 변경안 4절 예산. reasoning 이 예산을 자주 다 쓰면 재조정 |
| 11-18 | 측정은 본체 로컬 API(`origin=local`)가 먼저, 노트북 경유(`origin=laptop`)는 별도 행. 원장에 origin · workload · kv · mtp · thinking · cache_state · reasoning_tokens · ssd_read_mb 열 추가 | 변경안 6·7절, RULES 7 |
| 11-18 | 최종 사용 목표: 완성된 로컬 LLM 을 노트북의 코딩 도구(Claude Code · Codex · OpenCode)가 Tailscale(`--access tailscale`, 8080, API 키)로 부른다. 노트북 설정은 평소 도구 설정을 건드리지 않는 실행 스크립트(`scripts/client/`)로 한다 | 사용자 요청, `strata connect` 공식 지원 목록 |
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
| ~~Q2~~ | **종결 (11-18 사용자: 권장안 승인)** — 아래 권장안대로 만든다(구성은 F1 전, 에이전트는 `final_eval/` 을 읽지 않는다). 원 질문: 탐색·최종 평가 데이터 출처(공개·합성) | 권장: F1 50문항 = 튜닝에 쓰지 않은 저장소의 신규 합성 과제(X3 와 같은 방식: 고정 커밋 · 기준 실패 · 참조 통과 검증) 30 + 최근(모델 공개 이후) 공개 이슈 기반 20, `final_eval/` 에만 두고 에이전트는 읽지 않는다. 사람이 승인 | B0 품질 측정, F1, 64K | 기획서 8절, 토의 10 |
| ~~Q3~~ | **종결 (11-18)**: q36 경로는 `--kv` 미적용, K·V FP32(+FP16 사본) → KV 형식 변경은 3차 엔진 과제 (T-009, 계획 v2.2 5절). 원 질문: qwen36 경로에서 `--kv int8\|q4_0\|k8v4\|fp16` 이 실제로 적용되는지 (launcher 에는 옵션이 있고 기본 int8, QWEN36.md 는 fp32 라고 적음) | M0 로딩 뒤 KV 메모리로 확인, 적용되면 B1 후보 | B1 탐색 목록 | `env/strata-plan-20261118.md` |
| Q9 | RAM 여유가 약 0.7GB 뿐이다 (엔진 private 35.6GB, 페이지 파일 자동 증가 최대 8GB). 32K 긴 입력에서 페이징이 늘면 `--resident-budget-gib` · `--low-ram` 조정이 필요할 수 있다 | X1·X2 에서 페이지 파일·`file_mb`·지연을 같이 보고 판단 | X2, B1 | X0 관측 |
| Q11 | MTP 를 쓰려면 greedy 가 필요한데, thinking 모델은 greedy 에서 반복 위험이 있다. 운영 샘플링을 greedy 로 바꿀지, `STRATA_SPEC_PROB` 가 qwen36 경로에서 통하는지 | B1 에서 같은 코딩 과제로 greedy vs 권장 샘플링 품질·속도 비교 | B1 | Q10 진단 |
| ~~Q8~~ | **종결 (11-18 사용자 결정)**: pypa/packaging `6a69a83` 고정 신규 과제 6개(3개 구현 · 검증) + SWE-bench Verified 2건(`pallets__flask-5014`, `pytest-dev__pytest-8399`, 리비전 `78f471bf`, 로컬 conda 채점 — Docker 없음). `configs/eval/x3-packaging/TASKS.md`. 원 질문: X3 코딩 품질 탐색 세트의 출처 (긴 문맥 코드 수정·테스트) | 공개 저장소 일부로 합성한 과제 + 고정 단위 테스트, 최종 50문항과 분리 | X3 | 변경안 6절 |
| Q4 | 맞춤 양자화 원본(BF16 약 70GB) 확보·변환 방식 | 샤드 스트리밍 변환 가능성 먼저 소형 검사 | Q1 단계 | 기획서 6.3 |
| Q12 | thinking 상한을 서버 `reasoning_budget_tokens` 로 명시(b)할 때 값 — 11-18 토의로 (b) 방향, (c) 제외. 상세 `docs/TROUBLESHOOTING.md` T-007 | B1: max_tokens 8,192 고정, 상한 3K · 4.5K · 6K, 긴 답변 과제 추가 | B1, 클라이언트 설정 | XB 2차 |
| Q13 | 출력+reasoning 예산 8K 가 긴 답변(모듈 전체 · 긴 diff)에 충분한가 — 짧은 과제 96회 최대 6.6K · 잘림 0, kv_store 는 상한 6,144 에서 7.7~8.2K · 잘림 1 (11-18). 사용자: 32K 검증 뒤 예정대로 64K 까지 본다 | 32K: 8K+thinking 4.5K vs 10~12K(입력 20~22K)를 B1 · X3 결과로 결정. 64K 는 F1 32K 통과 뒤 — 출력 예산 확대 여지와 KV(FP32 약 2.5GiB) · expert 감소를 같이 잰다 | 클라이언트 설정, 64K 탐색 | B1-1 · XB · X2 |
| Q5 | API 사용량·비용 예산 상한 | 착수 시 사람이 정함 | 탐색 예산 | 기획서 5.2, 11절 |
| Q14 | 후속 턴 캐시 재사용이 0 이다(같은 세션 4요청 모두 cached 0, 2회 재현). 이전 답을 reasoning_content 와 함께 보낼 때만 재사용(직전 프롬프트 + 생성분 일부, 451 · 479). 도구 목록 빼기 · 작업 폴더 정보 변경은 차이 없음 | **11-18 A/B: H2a(전 턴 재전송)로 재읽기 −83% · 시간 −31%, 품질 같음 → 하네스 우회 확인.** H2b(직전 턴만)는 재사용 안 됨. X4 클라이언트가 thinking 을 전부 되돌려 보내는지 확인. 엔진 쪽(혼합 순환 레이어의 체크포인트 · 되감기) 원인 확인은 3차 | navigate 턴마다 전체 재읽기(1만~2만 토큰), X4 체감 지연 | `experiments/probes/probe_cache_20261118.json`, T-013 |
| Q15 | navigate 에 테스트 도구(`run_tests`, 기존 회귀 테스트만 · 숨은 테스트 제외)를 둘지. 지금 '실패 로그 보고 재수정' 은 preload 보완 턴에만 있다 | H1 · H2 다음 별도 후보 | 재수정 흐름 A/B | 하네스 지시 4절 |

## 에이전트 사용

- 지침은 루트와 폴더의 `AGENTS.md`. Codex 는 루트부터 지금 폴더까지 합쳐 읽는다.
- Claude Code 는 `CLAUDE.md` 가 있으면 `AGENTS.md` 를 자동으로 읽지 않는다. 그래서 `CLAUDE.md` 는 `@AGENTS.md` 한 줄로 불러온다. 지침을 `CLAUDE.md` 에 쓰지 않는다.
- 개인 기억(Claude 자동 메모리 등)은 저장소에 공유되지 않는다. 다음 세션이 알아야 할 것은 이 파일과 `docs/` 에 쓴다.

## 최근 변경

- 2026-11-18 · Claude Code · 마무리: 내일 안건 12건 권장대로 결정, Q2 종결(권장안 승인), API 키 생성 · 설정(git 제외, 401/200 확인), README · ENVIRONMENT · client README 최신화, 내일 계획 `docs/plan-20261119.md`.
- 2026-11-18 · Claude Code · H4 코드(`--final-turn edit`) · 밤 체인 3차 스크립트 커밋(6d18918), 가짜 응답 점검 통과(H0 동작 불변). 3차는 22:04 시작 직후 사용자 결정으로 중단(원장 행 없음, 빈 run 폴더 1개 삭제), 서버 종료 · 밤 모드. 11-19 에 `launch_night3.ps1` 로 시작.
- 2026-11-18 · Claude Code · 하네스 A/B 1 · 2차 완료 · 커밋(0f3e845 · 4ae78a4, 90행, 로그와 1:1 대조 · 중복 0). H1 품질 +2/15, H2a 품질 같음 · 시간 −31% · 재읽기 −83%, H2b(설계상 재사용 안 됨) · S1T3(품질 −2) 제외. 최다 실패는 강제 마지막 턴의 텍스트 편집 블록 불일치 → 다음 H4. LEDGER_SCHEMA 정정 2건(2차 커밋 혼재, 공유 폴더 config 덮어씀). Q14 하네스 우회 확인.
- 2026-11-19 · Claude Code · 토의 12건 권장대로 결정(결정 기록 11-19). 비공개 테스트 로그 노출 수정(T-014) · 7행 정정 기록, `git_dirty` 정의 변경, H2a · H2b(reasoning 재전송) · `--reasoning-budget`/`--settings-id` 러너 인자, `serve-ctx.ps1` 키 가드. 밤 체인 2차 예약.
- 2026-11-18 · Claude Code · X3 파일럿 2차 · SWE 2건 완료(T-010 · T-011, flask Werkzeug 고정). navigate v2(edit_file) 재측정 X3 2/3 · SWE 2/2. 하네스 v3 = H0(깨진 JSON 거부 · 오류 읽기 제외 · count_tokens 예산 · 턴별 캐시 · wall_ms), H1(도구 응답 페이지 나누기). 점검: 3 API x 스트림 도구 왕복 12/12, 후속 턴 캐시 재사용 0(Q14 · T-013). 서버 수명 문제(T-012) → WMI 밤 체인으로 H0 · H1 번갈아 3회 시작(17:04).
- 2026-11-18 · Claude Code · B1-1 완료 · 커밋. X3 파일럿 1차에서 채점 파서 결함(경로 줄 없는 · 들여 쓴 블록 0점)과 원장 6행 유실(T-010) → 파서 수정 · 2차 재시작. v2.2 10절: FlashAttention · GQA · KV · expert 배치의 측정 순서(P-diag 8K · 24K) · 병목별 첫 A/B · 채택 기준(10% / 5%, 3회 · 5쌍, 수치 오차 초안) · 업스트림 #3903 · #3904 · #3906 · #3909 (Open, E0 에 없음, 공개 수치만).
- 2026-11-18 · Claude Code · X3 준비: packaging 고정 커밋 과제 A·B·C 구현(기준 커밋 새 테스트 실패 · 참조 패치 통과 확인), 러너 `run_x3.py`(preload 길이 · navigate 도구 탐색 · 실패 로그 1회 보완), SWE-bench Verified 2건 선정 · `setup_swe.py` · `run_swe.py`. 실행 체인: B1-1 끝 → `matrix-x3.ps1`(preload 9 + navigate 3) → `matrix-swe.ps1`(환경 준비 → 2건). 8K 조건은 marker · version 과제의 필수 파일만으로도 약 12K 라 불가.
- 2026-11-18 · Claude Code · TurboQuant 자료 검토(v2.2 9.7: KV 양자화, STRATA 미지원 → E1 후보, 이 모델은 KV 비중이 작아 이득 상한 약 1.1GiB). 낮/밤 모드 스크립트 `scripts/llm-mode.ps1` · `user-mode.ps1` 추가(TCube · Claude Cowork 유지, 사용자 결정). X3 평가 자료는 대기.
- 2026-11-18 · Claude Code · v2.2 9절(후속 전달문: 3차 P0 · HR · E1, KV 구성 분해표, Q9 RAM 지표 분리) 반영. B1-1 thinking 상한 시험 시작(S0 · S1T3 · S1T4 · S1T6 x 과제 5개 x 3회, 새 과제 kv_store).
- 2026-11-18 · Claude Code · 계획 v2.2 반영(대응표 · 확인 상태 3분류 · KV 확인). q36 KV 는 FP32 로 확인, 원장 kv 라벨 정정(T-009), Q3 종결. 참고 링크는 도구 차단으로 미확인.
- 2026-11-18 · Claude Code · X2 완료(84행): 32K 설정 · 예산 8K 에서 입력 24K 까지 답변 도달 100%, 테스트 전부 통과 20~23/24, TG 77→50, SSD 0. 긴 입력에서 문법 오류 `List[str]]` 2건(T-008).
- 2026-11-18 · Claude Code · 측정용 전원 설정 고정(고성능 + power-max.ps1, 사용자 실행). 커밋 작성자 이메일 변경. X2 매트릭스 추가·시작.
- 2026-11-18 · Claude Code · XB 2차 완료(32K, 과제 4개 × 2K·4K·8K × 3회, 36행): 8K 만 12/12, 2K·4K 각 8/12. 서버 `answer_room` 이 max_tokens 의 1/4 을 답변 몫으로 남기고 thinking 을 닫는 것을 확인(Q12). 채점기가 문법 오류 답을 0/1 로 세던 것 고침. 커밋 16개 push.
- 2026-11-18 · Claude Code · X1 완료(54행, 처리량 시험으로 명명), MTP 진단(greedy 전용 경로, /metrics 계측 누락), 원장 열 8개 이행, 러너에 reasoning/답변 지연 분리·예산 가드·expert 상태·엔진 로그 drafts. 탐색 코딩 과제 4개(참고 해답으로 테스트 33개 검증) + XB 러너. XB 진행 중.
- 2026-11-18 · Claude Code · X0 완료: setup 빌드(E0 확정), 8K·16K·32K 기동·짧은 요청 각 3회 기록(원장 9행). 32K 에서 VRAM expert 63/256, TG 약 8% 하락. RAM 여유 약 0.7GB. 측정 러너·서버 전환 스크립트 추가.
- 2026-11-18 · Claude Code · 계획 v2.1 변경: 32K 운영 목표, X0~X4 실험 추가, RULES 7 교체, 원장 열 8개 추가(원장은 비어 있어 이행 대상 없음), 클라이언트 예산 8,192/20,000. M0 다운로드 완료(12.4분, sha256 일치). 그동안 측정값은 없어 다시 할 실험 없음.
- 2026-11-18 · Claude Code · 노트북 → Tailscale → 본체 호출 준비: `scripts/client/`(연결 확인, Claude Code·Codex 실행 스크립트), 방화벽 명령 문서화. 노트북에서 `strata-remote.ps1` 은 TCP 8080 실패까지 확인(서버 없음, 예상대로). 실제 호출은 M0 다운로드·서버 기동 뒤.
- 2026-11-18 · Claude Code · STRATA v0.2.15 clone·고정, E0 소스 빌드 성공(2.8분), 엔진 Python 런타임을 conda 환경에 설치, `--plan` 2건 기록. 모델 다운로드 없음. 엔진 실행(GPU 인식) 검증은 모델이 없어 미실행.
- 2026-11-18 · Claude Code · 빌드 툴체인 설치·검증 완료. VS Build Tools 1차 설치가 `--installPath` 공백 분리로 `C:\Program` 에 들어가 제거 후 기본 경로로 재설치(`scripts/fix-vs-buildtools.ps1`), `install-buildtools.ps1` 도 고침. `verify.ps1` 통과.
- 2026-11-18 · Claude Code · team4 형식의 AI 작업 문서 추가: `AGENTS.md` 재작성, `STATE.md`·`STRUCTURE.md`·`CONTRIBUTING.md`, 폴더별 README/AGENTS, PR·이슈 템플릿, `verify.ps1`. `docs/HANDOFF.md` 는 이 파일로 합침.
- 2026-11-18 · Claude Code · 빌드 툴체인 설치 시작(VS 2022 Build Tools 종료 코드 0, CUDA 13.2.2 진행 중). 검증 전.
- 2026-11-18 · Claude Code · kotokenlab 형식의 커밋 규칙·훅·CI 도입, 첫 커밋을 형식에 맞는 4개로 다시 써서 force-push. 훅 테스트 11개 통과.
- 2026-11-18 · Claude Code · Anaconda 2026.07-1 설치(SHA256 확인), conda-forge 환경 `strata_local_llm` 생성.
- 2026-11-18 · Claude Code · 본체 실측, 기획서 검토, 백그라운드 정리·시작 프로그램 해제.
