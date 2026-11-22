# STATE.md — 지금 어디까지 왔나

사람과 에이전트(Codex, Claude Code)가 함께 고치는 진행 기록입니다. 작업을 끝낼 때마다 해당 줄을 고치고 '최근 변경' 맨 위에 한 줄 더합니다. 설계 내용 자체는 `docs/`에, 수치는 `experiments/LEDGER.tsv`에, 여기는 상태와 결정만 둡니다.

## 지금

- 마지막 갱신: 2026-11-22
- **11-22 01:56 25-4 끝**: L2 마스킹 14/30 기각, **64K 21/30 효과 → 64K 를 노력치 high 로**. 다음은 노력치 옵션(다음 할 일 26). **11-22 08시 노력치 체인 시작(medium · xhigh, 64K, 끝 예상 16~17시)**. **11-22 17:13 노력치 끝**: medium(64K) 13/30 vs 32K 17/30 기각, xhigh 20/30 vs high 21/30 → xhigh 두지 않음. **운영 권장 = 서버 64K 하나 + 노력치 high**(사용자 확인 대기, effort 문서 4절). E1 턴 체크포인트 패치 작성(로컬 브랜치, 빌드 전). 저장소 공개 준비(본체 주소 가림 · 문서 정리) 커밋 → 사용자 승인 뒤 push · 공개
- 단계: **하네스 · 샘플링 탐색 마무리 → Q1(맞춤 양자화) 착수 직전 (11-20 오후)**. 기준 조합 = **M0 · E0 · 32K · H0 + card-coding**. 하네스 후보 H1 · H2a · H2b · H3 · H4 · C1 · S1T3 · T1(출력 예산 16K) 모두 기각 또는 효과 없음, card-coding 16/30 vs card-general 9/30 로 채택. A4(재토큰화) 원인 확인 · 보류. **Q1 진행 중 (11-21 02시)**: 서버 없이 빌드 · Q8_0 · 세 imatrix · 후보 R0 · M1a~M1d · R0u 생성 완료, R0u 가 M0 와 텐서 형식 · KL 모두 같음(재현 확인). **G2: M1a(KL 1.20배 · top-1 −0.32%p) · M1b(1.24배 · −0.51%p) 통과, M1c · M1d 탈락**. imatrix 비교(I-ours · I-unsloth · I-mix) 차이 오차 안 → **I-ours 로 결정**. **Q1-0c · G3 (11-21 오전, 47cb0f3)**: M1b · M1a 적재 정상(슬롯 88 · 85 vs 63), 둘 다 5/12 vs M0 7/12 → G3 통과, 다만 긴 입력 PP −23% · −44%(IQ 텐서 때문에 fused int8 커널을 못 씀). **원인 확인(엔진 소스, [`docs/engine-kernels-20261121.md`](docs/engine-kernels-20261121.md))**: IQ4_XS down 은 fused · 우리 int8 커널 어느 쪽도 받지 않고 이 빌드엔 MMQ 가 없어 한 층이라도 걸리면 전 층이 grouped 로 떨어진다. 카드는 **RTX 5070 Ti(sm_120, 70 SM, 16GB)**. **M1e(gate/up IQ4_XS + down IQ4_NL, 11-21 10시)**: 39/41 층 fused, PP 1,692 vs M0 1,525(+11%), KL 0.0538, expert RAM −1.79 GiB → M1a · M1b 대신 이것. G3 4/12 경계 통과 → **G4 13/30 vs 16/30 탈락(11-21 12:45, 16절, import_or_syntax 6 vs 1)**. 완만한 후보 **M2(gate/up 만 IQ4_XS, 13:14)**: KL 0.0474(M0 1.05배) · PP −3.5% · RAM −0.60 GiB → **G4 11/30 탈락(15:30, 18절, 짝 2 : 7) → Q1 종료 · M0 유지**. KL 이 M0 에 가까워도 X3 는 따라오지 않았다. **25-3 H7(편집 적용을 너그럽게, 18:11): 17/30 vs 16/30 → 채택, 기준 조합에 `--edit-apply lenient` 를 더함(02b1fe6)**. 커널 추가(int8 IQ4_XS down)는 작지만 E1 후보로 기록만(engine-kernels 6절). 11-21 밤 체인 `nrg`(04b1411): **run_tests 16/30 = 대조 16/30 → 효과 없음(Q15)**, **greedy 8/12 vs 7/12(r1-2) → 크게 안 떨어짐, 30회 확인 후보(Q17)**. 상세 [`docs/q1-plan-20261120.md`](docs/q1-plan-20261120.md) 11 · 12절
- 전체 계획: [`docs/plan-20261120.md`](docs/plan-20261120.md) (9단계, 11-19 확정 · 11-20 진행 표시)
- 이전 계획 문서: v2.0 + v2.1 + **v2.2** ([`docs/plan-v2.2-amendment-20261118.md`](docs/plan-v2.2-amendment-20261118.md): 1차 실행 설정 → 2차 양자화 → 3차 서버·엔진, 기존 ID 대응표, KV 독립 변수. 9절 = 3차 P0 · HR · E1 후속 전달문)
- 목표: **32K 운영** (입력 24,576 · 출력+reasoning 8,192), 8K 기준선 · 16K 중간 · 64K 선택 — [`docs/plan-v2.1-amendment-20261118.md`](docs/plan-v2.1-amendment-20261118.md)
- 사용 형태: 본체 STRATA 서버를 노트북 코딩 클라이언트(Claude Code · Codex)가 Tailscale 로 부른다. 코드 읽기·수정·테스트는 노트북에서
- 대상 PC: `desktop-5070` (Tailscale <본체 Tailscale 주소>), 저장소 `C:\strata-lab`
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
| 긴 문맥 코딩 품질 | X3 | 32K | 파일럿 완료 · 하네스 · 샘플링 탐색 완료(11-20). 기준 H0 + card-coding = 30회 16 통과(x3s1c, Q1 · E1 의 공유 대조). preload(입력 길이): 필수 파일만 2/3 첫 답 통과, 16K · 24K 는 6건 모두 첫 답 실패. navigate v1(읽기만 도구) 0/5 → v2(edit_file, T-011) X3 2/3 · SWE 2/2 | 지시 준수·코드 찾기·수정·테스트 통과·도구 호출 | 원장 `x3q_*` `x3s_*` `x3n_*` `x3sn_*`, `reports/x3-harness-summary.md` |
| X3 하네스 | H0 · H1 · H2a · H2b · S1T3 · H3 · H4 · C1 · T1 · S1 | 32K | **완료 (11-20)**: 기준 H0 유지. 30회 확인 기각 H3(17 vs 12) · H2a+card-coding(16 vs 8) · C1(48회 19 vs 19) · H4(11 vs 11, 시간 +17%) · T1(8 vs 6/24, 시간 +11%). **S1 card-coding 채택**(16 vs 9). 아래는 11-18 1 · 2차 기록 — A/B 1 · 2차 완료 (탐색, 각 3회). 15회 통과 H0 12 · 12(두 대조) · **H1 14** · **H2a 11(시간 −31%, 재읽기 −83%)** · H2b 10 · S1T3 10, 회귀 0. 최다 실패 = 강제 마지막 턴 텍스트 편집 블록 불일치 | 채택: v2.2 최종 5쌍 + 확인 전용 과제 D · E · F | 원장 `x3h0_*` `x3h1_*` `x3h2a_*` `x3h2b_*` `x3h0t3_*` (+ `x3s…`), 커밋 0f3e845 · 4ae78a4 |
| 노트북 경유 | X4 | 32K | 착수 전 · API 왕복 확인됨: Chat · Messages(Claude Code) · Responses(Codex) x 비스트림 · 스트림 12/12 (도구 호출 → 같은 ID 결과 → 후속 답, 스트림 인자 조각 조립) | 체감 지연(별도 행), tool calling·템플릿 호환 | `experiments/probes/probe_tools_20261118.json`, 원장 `origin=laptop` |
| 실행 설정 튜닝 | B1 | 32K | B1-1 완료 (thinking 3K 가 짧은 과제 12/12 · 첫 답변 37초, TG 동일). P-diag 1 완료(11-19): 63 슬롯 넘으면 TG 기여 작음, RAM 압박은 엔진 자체(expert 사본) → 투자는 Q1(RAM 여유)로 | S1, 병목 프로파일(KV·expert 캐시·버퍼 경쟁), 후보 순위 | 원장 |
| 맞춤 양자화 | Q1 | 32K | **종료 (11-21 15:30): M0 유지** — M1e 13/30 · M2 11/30 로 G4 탈락(q1-plan 16 · 18절). 이전 기록: Q1-0a 빌드 · 0b Q8_0 · 1 보정 세트 · 2 imatrix(I-ours 400청크) · 3 후보 생성 완료. expert GiB: R0 18.7 · M1a 17.3 · M1b 16.6 · M1c 15.0 · M1d 14.2. R0u(I-unsloth) = M0 와 텐서 형식 · KL 같음. imatrix-mix 완료. **G2(11-21)**: KL M0 0.0450 · R0 0.0429 · M1a 0.0539 · M1b 0.0556 · M1c 0.1018 · M1d 0.1300 → M1a · M1b 통과. imatrix 비교 → I-ours. **0c · G3(11-21 오전)**: 슬롯 M1b 88 · M1a 85, PP −23% · −44%, X3 5/12 · 5/12 vs 7/12 → 둘 다 통과. 남은 것 G4 · G5, N0 는 Q17 뒤 | 목적 RAM 여유. G0~G5 관문, 최종은 X3 30회 −1 이내(대조 x3s1c) | `docs/q1-plan-20261120.md` |
| 엔진 최적화 | E1 | 32K | **패치 작성(11-22)**: q36 턴 체크포인트, 엔진 작업 폴더 `work/engine-e1` 로컬 브랜치 `e1-turn-ckpt`. 빌드 · V1~V4 전 | 패치·수치 검사·E1 비교 | `docs/e1-turn-ckpt-plan-20261122.md`, T-013 |
| 결합 | C1 | 32K | 미착수 | 단독 효과와 상호작용 | 원장 |
| 최종 검증 | F1 | 32K | 미착수 | 독립 50문항, 재시작 재현, 혼합 50회 · 60분 | 원장 |
| 확장 탐색 | — | 64K | **11-22 결정: 64K = 노력치 high (x3k64h7 21/30 vs 32K 17/30, 시간 약 2.2배)**. 이전: 점검 완료(11-19 k64c · ctx64): 슬롯 42, RAM 여유 0.4~0.7GB, 32K 입력 TG 40.5 · 40K 30, X3 6/9 vs 3/9 판정 불가 → 결정은 Q1 뒤 한 번만 | F1 의 32K 통과 뒤에만 | 변경안 3절, 원장 `k64_*` `x3k64h0_*` |

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
    **11-19 시작점 (11-18 밤 사용자 결정: 캐시 먼저)**: 대화 캐시 A/B(`--conversation-cache-mib` 없음 · 512 · 1024, T-013 원인 가설) → 서버 설정 결정 → 본체에서 `powershell -ExecutionPolicy Bypass -File C:\strata-lab\scripts\bench\launch_night3.ps1` (H0 대조 `x3n3h0` vs H4 `x3h4`, 번갈아 3회, 약 1시간 40분, 끝 표시 `engine\night-chain3.log` 의 `[night3] done`) → 로그와 원장 1:1 대조 · 커밋 → 판정. 그다음 **H3** = H1 + H2a (H4 가 통과하면 함께), 그 뒤 `run_tests` 도구(Q15)
14. X4 기준선: 노트북에서 Claude Code CLI · Codex CLI 로 같은 과제(파일 탐색 → 수정 → 테스트 → 실패 로그 재수정), 같은 STRATA 32K. 후보 하나 더면 OpenCode. Hermes 는 64K 뒤
15. 그다음 B1(P-diag → 첫 A/B, Q11 greedy·MTP 포함)
16. ~~남은 X3 과제 3개(D · E · F) 구현~~ 완료 · 검증 (11-19): 확인 전용, `configs/eval/x3-packaging/TASKS.md`
17. ~~seed 42 반복 독립성~~ 확인 (11-18): 같은 seed 에서도 반복마다 답 · 호출 수가 달랐다(짧은 flask 일부만 같음) → 반복은 독립에 가깝다. 접두사는 체인마다 나눈다(LEDGER_SCHEMA 정정: 공유 폴더 config 덮어씀)
18. **로컬 LLM 주 에이전트 · 워커 준비** (11-18 밤, `docs/WORKER.md`): 운영 서버 `scripts/launch_serve.ps1`(WMI), 워커 `scripts/worker/`(MCP `delegate_code_task` → diff). 자체 점검 5/5 · 실제 모델 1건 통과. 남은 것: 채택 하네스를 `configs/worker.json` 에 반영(H3 뒤), Codex 0.169 쓰기 샌드박스 · 출력 예산 키(X4), X5 워커 위임 A/B(클라우드 단독 vs 클라우드 지휘 + 로컬 워커). 지휘자 쪽 MCP 등록은 사람이 한다
19. ~~T-013 원인 가설 확인~~ 기각 · 원인 확정 (11-19, record 커밋): q36 엔진이 `--conversation-cache-mib` 를 받지 않음, 재사용은 정확한 이어 붙이기만. 서버 설정은 그대로(H4 · H3 는 기본 설정)
20. ~~하네스 · 샘플링 탐색~~ 완료 (11-19 밤 ~ 11-20): 기준 **H0 + card-coding**. 앞으로 A/B 체인은 `--sampling card-coding` 을 명시하고, 대조는 S1 의 `x3s1c`(seed 42~46)를 다시 돌리지 않고 쓴다
21. ~~BF16 원본 · llama.cpp 확보~~ 완료 (11-20 11:59): `data\models\qwen36-bf16`(2샤드 sha256 일치), `work\llama.cpp`(v1.0.0, 빌드 전)
22. ~~A4 원인 확인~~ 완료 · 보류 (11-20): `docs/a4-findings-20261120.md`. X4 에서 클라이언트가 thinking 을 되돌려 보내면 A4 + 강제 턴 도구 목록 유지를 같이
23. **Q1 맞춤 양자화** (진행 중): ~~9절 결정 → Q1-0a llama.cpp 빌드 → 0b Q8_0 → 1 보정 세트 → 2 imatrix → 3 후보 생성 · R0u~~ 완료(11-20 17:58, 11절) → ~~imatrix-mix · G2 KL~~ 완료(11-21 02:06, 12절: M1a · M1b 통과) → ~~M1a · M1b 를 I-unsloth · I-mix 로~~ 완료(11-21 02:36, 차이 오차 안 → I-ours) → ~~0c 적재 점검 · G3(M1b · M1a)~~ 완료(11-21 09:04, 13절: 둘 다 5/12 통과, PP 손실) → ~~커널 원인 조사 · M1e 생성 · G2 · PP~~ 완료(11-21 10:18, 14절) → ~~M1e G3 · G4~~ 13/30 탈락(16절) → ~~M2 G2 · G4~~ 11/30 탈락(11-21 15:30, 18절) → **Q1 종료, M0 유지**
24. 그 뒤: 64K 결정(Q1 반영, 한 번만) → E1(KV int8 · 스냅샷은 reasoning 재전송을 안 쓰는 지금 우선순위 낮음) → 최종 조합 재확인 → X4 · X5 → F1
25. **워커로 쓸 만해지기 위한 순서 (11-20 저녁, Claude 제안 · 사용자가 기록 요청, 실행 순서는 아직 확정 아님)**: 목표는 감독이 붙는 보조 워커. 지금 X3 30회 16 통과(53%)에서 70% 안팎을 목표선으로 둔다(판단 기준이지 측정값이 아니다). 정확도 · 속도 · 운영 평가는 같은 날 대화 기록.
    1. Q1 마무리(RAM 안정). **N0(MTP 제거)는 Q17 결론 뒤에** 정한다.
    2. **자기 검증 루프**: `--run-tests on` 을 H0 + card-coding 6과제 x 5회로 잰다. 대조는 x3s1c 재사용(같은 seed). L1(hadd `x3a6t`, S1 이전 샘플링 · 3과제 x 4회)이 7/12 vs 기준 5/12 였는데 30회 확인을 하지 않았다(Q15). **11-21 완료(04b1411): 16/30 vs 16/30 → 효과 없음, 기본값 off 유지.** H6 `--edit-hint` 는 이미 있고 5/12 vs 5/12 였다(3번과 겹치지 않게 참고).
    3. **편집 적용을 너그럽게**: 공백 · 들여쓰기 차이 허용, 여러 곳이 맞으면 되묻기, 실패하면 그 부분을 다시 보여주기. 손실 없음. 지금까지 가장 많은 실패(강제 턴 편집 블록 불일치 · 부분 적용)를 겨냥.
       **11-21 착수 (H7, `docs/h7-edit-apply-20261121.md`)**: 원장 · 답 파일 분석 — M0 대조 x3s1c 의 edit_file 실패는 55회 중 1회뿐이고, 실패는 도구 편집 없이 강제 마지막 턴까지 간 실행(metadata_extra_dupes · specifier_bounds)에 몰려 있다. 그 답의 원인: SEARCH/REPLACE 블록 전체를 2~3칸 더 들여 씀(기존 dedent 는 공통 들여쓰기를 다 빼서 못 맞춤), 도구가 없는 턴에 edit_file 을 텍스트 호출로 씀, 빈 답. 오프라인 재현(작업 복사본이 처음 그대로인 실행 80건, 9세트): 들여쓰기 이동 허용만으로 적용 실패 15건이 적용되고 5건이 통과로 바뀜. **H7 = (1) 블록 전체 들여쓰기 ±1~16칸 이동 허용(한 가지 이동 · 한 곳만 맞을 때만) (2) 줄 끝 공백 무시 (3) 마지막 답의 텍스트 edit_file 호출(path · old_string · new_string)을 편집으로 받기 (4) 여러 곳이 맞으면 줄 번호를 알려 주기.** edit_file 도구와 강제 턴 블록 양쪽에 같은 규칙, `--edit-apply lenient`(H0 = strict). 판정: M0 · 6과제 x 5회 vs x3s1c 16/30, 손실 없는 변경이라 −1 이내면 채택(효과가 없어도 해가 없으면 유지 가능).
       **11-21 결과(`x3h7`, 02b1fe6): 17/30 vs 16/30 → 채택. 기준 조합은 H0 + `--edit-apply lenient` + card-coding.** 짝 5:4, 숨은 테스트 합 361 vs 335 / 550. apply_fail + no_edit 5 → 0, import_or_syntax 1 → 5. 다시 적용해 보니(replay) 문법 오류 가운데 H7 규칙이 만든 것은 없었다(strict 였다면 apply_fail · no_edit). 규칙이 실제로 쓰인 실행은 6회(들여쓰기 이동 4 · 텍스트 호출 2)이고 그중 2회가 통과했다. +1 은 잡음 범위라 "해가 없다"까지만 확실하다. 남은 실패는 편집이 적용된 뒤의 틀린 내용(test_fail 8 · import_or_syntax 5, metadata 0/5 · specifier 0/5)이다 → 적용 규칙으로는 더 못 올린다. 상세 h7 문서 5절.
    4. **문맥 관리 vs 64K**: 오래된 도구 출력 요약 · 제거(loop-plan L2)와 64K 를 같은 과제로 비교해 24번의 64K 결정에 같이 쓴다.
       **11-21 착수 (`docs/l2-mask-20261121.md`)**: 기록 분석 — metadata · specifier 실패 20회 모두 도구 편집 0회. 큰 파일(specifiers.py 약 1,400줄 · metadata.py 약 1,060줄)을 read_file 로 12,000자씩 처음부터 넘겨 읽다가(5~7번, 76~105K자) 편집 전에 강제 턴 문턱 22,272 에 닿는다. **두 팔로 잰다. 대조 = x3h7 17/30(다시 안 돌림)**: (A) **L2 관찰 마스킹, 32K**: 입력이 16,000 을 넘으면 그때 한 번에, 가장 최근 도구 결과 2개를 빼고 오래된 큰 도구 결과(400자 이상)를 자리표시('지웠다, 필요하면 다시 읽어라' + 경로 · 줄 범위)로 바꾼다. 입력이 10,000 아래로 내려갈 때까지만 지우고, 다시 넘으면 또 한 번. 편집 결과와 모델의 말은 지우지 않는다. 손실 가능(다시 읽으면 복구됨). (B) **64K, 마스킹 없음**: 강제 턴 문턱 55,296(ctx − 8,192 − 2,048). 둘 다 M0 · H7 · card-coding · seed 42~46, 6과제 x 5회, 한 체인으로 밤에 돈다. **판정**: 각 팔 16 이상(−1 이내)이면 해가 없음, 18 이상이면 효과. 둘 다 효과가 같으면 32K + 마스킹을 고른다(RAM · 속도 · 기존 측정 유지). 64K 는 이 결과를 24번 결정에 그대로 쓴다(한 번만).
       **A 결과(`x3l2`, 21:29): 14/30 vs 17/30 → 기각.** 짝 2 : 6, 숨은 테스트 357 vs 361, import_or_syntax 6. 입력은 8~16K 로 내려가 specifier 숨은 테스트 25/30 까지 올랐지만 통과 0/5 그대로이고, 잘 되던 dg · marker · version 이 떨어졌다(지운 조각을 기억으로 고치다 문법이 깨짐으로 보임). l2 문서 4절.
       **B 결과(`x3k64h7`, 11-21 21:31 ~ 11-22 01:56): 21/30 vs 17/30 → 효과(18 이상).** 짝 6 : 2, 숨은 테스트 510 vs 361 / 550, 실패 9회 모두 test_fail(import_or_syntax 0). specifier 0/5 → 3/5(M0 첫 통과), metadata 는 0/5 그대로(숨은 15~19/20). 마지막 입력 최대 39.3K 로 문턱 55,296 에 한 번도 안 닿았고, 어려운 과제는 호출 19번에서 강제 턴 → 이제 막는 것은 문맥이 아니라 `max_steps` 20. 대가는 시간: 회차당 약 53분(대조 약 24분), think 토큰 약 2.5배. 끝난 뒤 RAM 26.7GB 회복. l2 문서 5절. **24번 64K 결정: 64K 를 '노력치 high' 로 쓴다(기본 32K 는 그대로).**
       **조합 분석(사용자 요청, `docs/combo-analysis-20261121.md`)**: 원장 653행 · 35조합으로 과제 보정 베이즈 로지스틱 + 그리드. 확실한 요인은 card-coding(+) · H2a(−) · 양자화(−). 유망하지만 확인 안 된 것은 H1 페이지 출력(짝 +2/30, card-coding 과 같이 잰 적 없음) · greedy(12회) · 64K. 외삽 없는 최선 예측은 H7 + coding + 64K 19.3/30. 다음 순서: 64K 결과 → H1 + H7 + coding 30회 → greedy + H7(Q17) → 이긴 요인만 합쳐 한 번 확인.
    5. X4(실제 위임 흐름) · 과제 유형 넓히기(설정 · 테스트 작성 · 리팩터링). 6과제 과적합을 막는다.
26. **노력치 옵션 → 도구 (11-22 사용자 결정 순서)**:
    1. 노력치: 서버는 64K 하나, 요청마다 `effort` 로 강제 턴 문턱 · 호출 상한을 고른다. low 22K/12 · medium 22K/20(지금 기준과 같음) · high 55K/20(= x3k64h7) · xhigh 55K/30. 테스트가 실패하면 한 단계 올려 **처음부터 새로** 다시 돈다(자동 올리기). 측정: xhigh 6과제 x 5회(대조 x3k64h7 21/30), 그리고 64K 서버에서 medium 이 32K 의 x3h7 과 같은지 확인.
    2. 도구: 편집 직후 문법 검사(ast.parse, 깨지면 되돌리고 줄 번호를 알려 줌) → 파일 개요 · 심볼 읽기(outline / read_symbol). 하나씩 30회로 재고 −1 규칙으로 채택.
    3. 그 뒤 후보: H1 + H7 + coding, greedy(Q17), `configs/worker.json` 갱신.
    **11-22 착수 (`docs/effort-20261122.md`)**: `run_x3.py --effort` · `g3-chain.ps1 -Effort` · 자체 점검 10/10. 오늘 체인 `scripts/bench/effort-chain.ps1`(64K 서버): 팔 M medium `x3e64m`(대조 x3h7 17/30, 약 2시간) → 팔 X xhigh `x3exh`(대조 x3k64h7 21/30, 약 5~6시간), 끝 표시 `engine\effort-chain.log` 의 `[effort] done`. 판정: M 16 이상이면 서버 하나(64K) + medium 운영, X 22 이상이면 xhigh 유지. 자동 올리기 효과는 세 세트로 서버 없이 추정.
    - 속도 쪽 MTP 는 Q17.
    **11-22 17:13 결과 (4351119 · 6b92845)**: 팔 M medium 13/30(짝 2:6) → 기각, 팔 X xhigh 20/30(짝 3:4, 회차 약 89분) → 두지 않음. 자동 올리기 추정(엄격 통과): 64K high 한 번 21/30 · 8.8분, medium → high 22/30 · 10.3분, 32K → 64K high 23/30 · 9.9분 + 재기동. → 서버 64K + high 권장, 워커 기본값 high.
27. **다음 순서 (11-22 저녁)**: (1) 문서 정리 · 공개 준비 커밋 → 사용자 승인 뒤 push · 저장소 공개 (2) E1 빌드 → V1 → V2 → V3 → V4(64K · high 로 30회, 대조 x3k64h7) (3) 도구 T1 · T2 30회(`docs/tools-20261122.md`) (4) 새 과제 세트 Y(`docs/new-tasks-plan-20261122.md`) (5) X4.

## 사람에게 요청한 것

| 날짜 | 요청 | 상태 |
| --- | --- | --- |
| 11-18 | 전원 구성표를 고성능으로 변경 (측정 위생) | 완료 (11-18 11:41): 고성능 + `scripts/power-max.ps1`(최소 CPU 100% · 코어 파킹 끔 · 부스트 적극 · 디스크·USB 절전 끔 · 최대 절전 끔), 기록 `env/power-*`. **X0 · X1 · XB 는 '균형 조정'에서, X2 부터 고성능에서 쟀다** |
| 11-18 | 양자화 단계 전 페이지 파일 확대 (예: 64GB) | 완료 (11-19 12:08): C:\ 고정 64GB(커밋 한도 95GB) · 재부팅 |
| 11-20 | Q1 결정 4건 (`docs/q1-plan-20261120.md` 9절: 보정 데이터 · N0 · 메모리 목표 · G2 기준) | 완료 (11-20 15시대): 권장안대로 — 결정 기록 참고 |
| 11-18 | STRATA API 키 설정 | 완료 (Claude 가 생성 · 설정, 값은 `.secrets\` 에만) |
| 11-18 | 커밋 작성자 이메일을 kotokenlab 과 같게 할지 결정 (지금은 noreply) | 완료: 사용자 계정 이메일로 (저장소 로컬 `user.email`, d818a2b 이후 커밋부터). 이전 커밋은 noreply 그대로 |
| 11-18 | 본체 방화벽에 Tailscale 대역만 허용하는 8080 규칙 추가 (명령은 `docs/ENVIRONMENT.md` '노트북에서 호출' 1) | 완료 (본체 규칙 1개, 100.64.0.0/10 · TCP 8080 확인. 노트북에 잘못 만든 규칙은 삭제됨) |

## 결정 기록

| 날짜 | 결정 | 근거 |
| --- | --- | --- |
| 11-22 | **노력치 판정**: medium(64K) · xhigh 둘 다 기준 미달 → 서버 64K 하나 + 노력치 high 를 워커 기본으로(권장, 사용자 확인 대기). 32K 서버를 따로 두는 안은 +2회(우연 범위) 대비 재기동 비용으로 채택 안 함 | x3e64m 13 vs 17, x3exh 20 vs 21, `docs/effort-20261122.md` 4절 |
| 11-22 | 저장소 공개 준비: 지금 파일에서만 본체 주소를 가리고 이력은 다시 쓰지 않는다. 노트북 스크립트는 `STRATA_BASE_URL` 을 읽는다 | 사용자 결정, C-027 |
| 11-20 | **Q1 착수 결정 4건 권장안대로 (사용자)**: (1) 보정 데이터 = conda 환경의 Python 소스(표준 라이브러리 · 일부 site-packages) + 그 코드를 감싼 도구 호출 형식 대화 + 한국어 기술 문서 소량. X3 · SWE 과제 저장소(packaging · flask · pytest · werkzeug), `final_eval/`, 실험 로그 제외, 다운로드 없음, 파일 목록을 남겨 F1 출처에서 뺀다 (2) **N0(MTP 블록 제거)** 후보에 넣음(card-coding 은 MTP 초안을 안 써 손실 없음, 엔진 수용은 Q1-0c 에서 확인) (3) 메모리 목표 = 64K 기동 뒤 남은 RAM ≥ 2GB · 페이지 파일 증가 없음 (4) G2 잠정 = KL ≤ M0 의 2배 · top-1 하락 ≤ 2%p 일 때만 G3, 최종 판정은 X3 30회 −1 이내 | `docs/q1-plan-20261120.md` 9절 |
| 11-20 | **H2a 기각 (사용자)**: H2a(reasoning 재전송) + card-coding vs 대조 x3s1c(H0 + card-coding, 같은 seed 42~46), 6과제 x 5회 = 짝 30. 통과 8/30 vs 16/30, 한쪽만 통과 2 : 11(부호 검정 p≈0.02), 일부 적용 5 vs 0. 과제당 시간 −24%, 새로 읽은 입력 약 −75% 이지만 정확도 우선 기준(−1 이내)에 크게 못 미침. 11-19 H3 기각(17 vs 12)과 같은 방향 — 이전 턴 reasoning 이 쌓이면 편집이 틀어진다 | 원장 `x3h2k_*`, 엔진 로그 `-h2k` · `-s1` |
| 11-20 | **기준 샘플링 = card-coding (사용자)**: S1 에서 card-coding 16/30 vs card-general 9/30(짝 9:2). 기준 조합은 **H0 + card-coding**. 이후 A/B 체인은 `--sampling card-coding` 을 명시한다(러너 기본값은 옛 체인 재현을 위해 그대로 card-general) | 원장 `x3s1c_*` `x3s1g_*` |
| 11-20 | **A4 보류 (사용자)**: STRATA_DEBUG 로 생성 id 를 확인(응답 67개). 후속 턴 61개 중 57개 완전 재사용, 실패 4 = 재토큰화 1(약 1.5%) + 강제 마지막 턴이 도구 목록을 빼서 앞부분이 바뀜 3. 둘 다 reasoning 재전송일 때만 문제라 H2a 기각으로 지금은 이득 없음 → X4 에서 실제 클라이언트가 thinking 을 되돌려 보내면 A4 + 강제 턴 도구 목록 유지를 같이 넣는다 | `docs/a4-findings-20261120.md`, 원장 `x3a4d_*` |
| 11-20 | **하네스 후보 C1 기각 (사용자)**: H0 vs H0+C1, card-general, seed 회차 1~8(42~49) x 6과제 = 짝 48. 통과 19/48 vs 19/48, 한쪽만 통과 5 : 5. 1~4회차 8 vs 10 은 5~8회차 11 vs 9 로 상쇄. 과제당 시간 234 → 219초(-6%)뿐이라 기본 하네스에 넣지 않는다. 체인 `c1conf-chain.ps1`(-RepStart, 793f667) 은 기록용으로 남김 | 원장 `x3c1b_*` `x3c1r_*`, 엔진 로그 `-c1` · `-c1r5` |
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
| Q9 | RAM 여유가 약 0.7GB 뿐이다 (엔진 private 35.6GB, 페이지 파일 자동 증가 최대 8GB). 32K 긴 입력에서 페이징이 늘면 `--resident-budget-gib` · `--low-ram` 조정이 필요할 수 있다 | X1·X2 에서 페이지 파일·`file_mb`·지연을 같이 보고 판단. **11-19 갱신**: 원인은 엔진의 expert 사본(18.75GiB), 정리할 백그라운드 없음 → Q1 목적을 RAM 여유로 | X2, B1, Q1 | X0 관측, `docs/plan-20261120.md` |
| ~~Q11~~ | **종결 (11-20)**: 운영 샘플링은 card-coding(temperature 0.6, 샘플링) — S1 에서 card-general 보다 정확(16 vs 9). 샘플링이라 MTP 초안은 쓰지 않는다(Q10). greedy 는 품질 근거가 없어 보류. 결과적으로 MTP 블록은 메모리만 차지 → Q1 후보 N0(MTP 제거) | — | — | S1 · D0 |
| ~~Q8~~ | **종결 (11-18 사용자 결정)**: pypa/packaging `6a69a83` 고정 신규 과제 6개(3개 구현 · 검증) + SWE-bench Verified 2건(`pallets__flask-5014`, `pytest-dev__pytest-8399`, 리비전 `78f471bf`, 로컬 conda 채점 — Docker 없음). `configs/eval/x3-packaging/TASKS.md`. 원 질문: X3 코딩 품질 탐색 세트의 출처 (긴 문맥 코드 수정·테스트) | 공개 저장소 일부로 합성한 과제 + 고정 단위 테스트, 최종 50문항과 분리 | X3 | 변경안 6절 |
| ~~Q4~~ | **종결 (11-20)**: BF16 원본 확보(2샤드 71.07GB, sha256 일치) · llama.cpp v1.0.0 clone. 변환 방식은 `docs/q1-plan-20261120.md`(Q8_0 기준 → imatrix → `--tensor-type` 후보, 서버 내린 시간에만) | — | Q1 | 11-20 다운로드 로그 `engine\after-ext.log` |
| Q12 | thinking 상한을 서버 `reasoning_budget_tokens` 로 명시(b)할 때 값 — 11-18 토의로 (b) 방향, (c) 제외. 상세 `docs/TROUBLESHOOTING.md` T-007 | B1: max_tokens 8,192 고정, 상한 3K · 4.5K · 6K, 긴 답변 과제 추가 | B1, 클라이언트 설정 | XB 2차 |
| Q13 | 출력+reasoning 예산 8K 가 긴 답변(모듈 전체 · 긴 diff)에 충분한가 — 짧은 과제 96회 최대 6.6K · 잘림 0, kv_store 는 상한 6,144 에서 7.7~8.2K · 잘림 1 (11-18). 사용자: 32K 검증 뒤 예정대로 64K 까지 본다 | 32K: 8K+thinking 4.5K vs 10~12K(입력 20~22K)를 B1 · X3 결과로 결정. 64K 는 F1 32K 통과 뒤 — 출력 예산 확대 여지와 KV(FP32 약 2.5GiB) · expert 감소를 같이 잰다 | 클라이언트 설정, 64K 탐색 | B1-1 · XB · X2 |
| Q5 | API 사용량·비용 예산 상한 | 착수 시 사람이 정함 | 탐색 예산 | 기획서 5.2, 11절 |
| Q14 | 후속 턴 캐시 재사용이 0 이다(같은 세션 4요청 모두 cached 0, 2회 재현). 이전 답을 reasoning_content 와 함께 보낼 때만 재사용(직전 프롬프트 + 생성분 일부, 451 · 479). 도구 목록 빼기 · 작업 폴더 정보 변경은 차이 없음 | **11-18 A/B: H2a(전 턴 재전송)로 재읽기 −83% · 시간 −31%, 품질 같음 → 하네스 우회 확인.** H2b(직전 턴만)는 재사용 안 됨. X4 클라이언트가 thinking 을 전부 되돌려 보내는지 확인. **엔진 원인 확정(11-19)**: q36 경로는 대화 캐시 옵션이 없고(`--conversation-cache-mib` 무시), 든 토큰 전체가 새 프롬프트의 앞부분일 때만 이어 쓴다(되감기 · 체크포인트 없음). 설정으로 못 고침 → 하네스 · 클라이언트의 정확한 재전송, E1 후보 '프롬프트 끝 순환 상태 스냅샷' (T-013). **11-20 갱신**: H2a 를 card-coding 30회로 다시 재니 16 vs 8 → **기각**(재전송이 정확도를 떨어뜨림). 재사용 실패 원인(A4) = 재토큰화 1/67 · 강제 턴 도구 목록 제거 → 보류, X4 에서 재검토(`docs/a4-findings-20261120.md`) | navigate 턴마다 전체 재읽기(1만~2만 토큰), X4 체감 지연 | `experiments/probes/probe_cache_20261118.json`, T-013 |
| Q16 | 64K 가 메모리에 들어가는가 — 11-18 로그로 추정: 로딩 시 VRAM 여유 8K 7.67 · 16K 7.25 · 32K 6.50GiB(1K 칸당 약 0.047GiB), VRAM 상주 expert 79 · 74 · 63/256 → 64K 는 여유 약 5.0GiB · 상주 약 42/256 로 추정. KV 는 VRAM 에 있어 RAM 은 크게 늘지 않을 것으로 보이나 미확인. 엔진에 `--kv int8|q4_0|k8v4` · `--kv-grow` · `--kv-resident N` 이 있다(q36 경로 적용 여부 미확인, v2.2 는 q36 KV FP32 로 기록) | 64K 단계에서: 64K 기동 로그(VRAM 여유 · 상주 expert · RAM) → 같은 과제로 32K 대비 속도 · 품질, KV 옵션 A/B. 먼저 q36 경로가 `--kv` 를 받는지 소스 확인. **11-19 측정(k64c)**: 64K 슬롯 42, 기동 뒤 RAM 여유 0.44~0.68GB, 32K 입력 pp 1500 · tg 40.5, 40K 입력 tg 30, X3 6/9 vs 3/9 판정 불가, q36 KV 옵션 없음 확인 → 결정은 Q1 뒤 | 64K 탐색, 클라이언트 예산 | 엔진 로그 `strata-qwen36-ctx*.log`, `strata.exe --help` |
| Q15 | navigate 에 테스트 도구(`run_tests`, 기존 회귀 테스트만 · 숨은 테스트 제외)를 둘지. 지금 '실패 로그 보고 재수정' 은 preload 보완 턴에만 있다 | H1 · H2 다음 별도 후보. **11-20 정리**: 도구는 구현됨(`--run-tests on`). L1(hadd `x3a6t`, S1 이전 샘플링 · 3과제 x 4회) 통과 7/12 vs 기준 `x3a6b` 5/12, 평균 시간 3.8 vs 3.9분. 같은 체인의 C1 은 9/12 였다가 48회 확인에서 같음(19 vs 19)으로 기각됐으니 12회 차이는 믿기 어렵다 → H0 + card-coding 30회로 확인(다음 할 일 25-2). **11-21 결과(`x3rt`, 04b1411)**: 16/30 vs x3s1c 16/30(과제별 dg 4 vs 3 · marker 1 vs 2 · metadata 0 vs 2 · specifier 1 vs 0 · tags 5 vs 5 · version 5 vs 4), 실행당 모델 시간 3.56 vs 3.88분 → **효과 없음, 기각(C1 과 같은 기준)** | 재수정 흐름 A/B | 하네스 지시 4절, 원장 `x3a6*` |
| Q17 | **MTP 를 쓸 가치가 있나** (N0 결정과 묶임) | [기록 · 소스 정리 11-20] q36 경로는 greedy(temperature 0 · penalty 0) 요청만 초안을 쓴다(`q36_engine.cu:3730`). 범용 경로의 `STRATA_SPEC_PROB`(샘플링 요청도 초안, 기각 표집으로 분포 보존, `mtp.cpp:724`)는 q36 경로에 없다. 속도: 순수 greedy 158/198 수락 · TG 154~162 vs 샘플링 83~108(짧은 입력, 11-18). D0: MTP 2 vs 0 greedy 출력 같음(무손실). 품질: greedy 의 X3 측정 없음. Qwen3 계열 모델 카드는 thinking 모드에서 greedy 를 권하지 않는다(성능 저하 · 끝없는 반복). 샘플링 설정에 민감하다(card-coding 16 vs card-general 9). 긴 입력에서 수락률 · 속도는 미측정 → **지금 운영(card-coding)에서는 MTP 이득 0**. 길: (a) greedy H0 X3 6과제 x 2 짧은 확인, 크게 떨어지지 않으면 30회 (b) 턴 종류별 혼합(편집 · 최종 턴만 greedy) (c) E1 후보: q36 경로에 SPEC_PROB 이식(엔진 작업, 분포 보존이라 품질 손실 없음, 가장 확실하지만 가장 비쌈). N0 절감은 0.45GiB 뿐이라 서두를 이유 없음. **11-21 (a) 결과(`x3gr`, 04b1411)**: greedy 8/12 vs x3s1c r1-2 7/12(tags 2 vs 2 · version 2 vs 2 · dg 2 vs 1 · marker 2 vs 1, metadata 0 vs 1, specifier 0 vs 0), 엔진 초안 62473/74046 채택(84%). 실행당 모델 시간 3.81 vs 4.48분(−15%)이지만 출력 토큰도 적어 출력 기준 36.3 vs 38.7 tok/s 로 오르지 않았다(입력 처리 몫과 분리 안 함). → 크게 안 떨어짐, 다음 = greedy 30회(r3~5 18회 추가로 x3s1c 와 짝) 후 판정 | N0, 속도, E1 | T-004, `experiments/probes/d0_determinism_20261119.json`, 11-20 대화 |

## 에이전트 사용

- 지침은 루트와 폴더의 `AGENTS.md`. Codex 는 루트부터 지금 폴더까지 합쳐 읽는다.
- Claude Code 는 `CLAUDE.md` 가 있으면 `AGENTS.md` 를 자동으로 읽지 않는다. 그래서 `CLAUDE.md` 는 `@AGENTS.md` 한 줄로 불러온다. 지침을 `CLAUDE.md` 에 쓰지 않는다.
- 개인 기억(Claude 자동 메모리 등)은 저장소에 공유되지 않는다. 다음 세션이 알아야 할 것은 이 파일과 `docs/` 에 쓴다.

## 최근 변경

- 2026-11-22 · Claude Code · 노력치 체인 끝(17:13): medium(64K) 13/30 기각 · xhigh 20/30 두지 않음 → 64K + high 권장, 워커 기본값 high. 기록 커밋 4351119 · 6b92845. 문서 정리(README · docs 색인 · 진행 요약 · 그림 5장 · COLLAB-LOG C-024~027 · T-013 E1) · 공개 준비.
- 2026-11-22 · Claude Code · 노력치 옵션(`--effort low/medium/high/xhigh` = 문턱 · 호출 상한 묶음) · 측정 체인 `effort-chain.ps1` · `docs/effort-20261122.md`(정의 · 판정 · 오늘 시간표). 자체 점검 10/10, 기존 자체 점검 전부 통과.
- 2026-11-22 · Claude Code · 25-4 끝: A 32K + L2 마스킹 14/30(짝 2:6) 기각, B 64K 21/30(짝 6:2, 숨은 510 vs 361, 회차 약 53분) 효과 → 24번 결정 = 64K 를 노력치 high 로. 조합 분석 문서 · `scripts/analysis/x3_combo.py` 추가. 다음 할 일 26(노력치 → 도구) 기록.
- 2026-11-21 · Claude Code · 25-3 H7(`--edit-apply lenient`, 1be6e1f): M0 30회 17/30 vs H0 16/30(짝 5:4, 숨은 테스트 361 vs 335) → 채택(02b1fe6). apply_fail · no_edit 5 → 0, 늘어난 import_or_syntax 는 H7 규칙과 무관(재적용 확인). 남은 실패는 내용 오류. h7 문서 5절.

- 2026-11-21 · Claude Code · Q1 G3 · G4(M1e): G3 4/12 vs 7/12 경계 통과, G4 30회 13 vs 16(짝 3:6, import_or_syntax 6 vs 1) → 탈락(bcd5c15). q1-plan 15 · 16절. 다음 방향은 사용자 결정 대기.
- 2026-11-21 · Claude Code · M1e(`q1-m1e.ps1`, 02ef084): down IQ4_NL → 39/41 fused, PP +11% vs M0, KL 0.0538, 슬롯 70. 회고(왜 못 잡았나) · 커널 추가 검토 · '레시피 전에 엔진 짝 확인' 규칙을 engine-kernels 6절에.
- 2026-11-21 · Claude Code · 엔진 커널 조사(사용자 요청): q36 프롬프트 expert 경로 = fused → int8 → (MMQ, 빌드에 없음) → grouped, 한 층 grouped 면 전부 grouped. fused down 은 IQ4_NL · Q2_0 · K-quant 짝만, int8 down 에 IQ4_XS 없음 → M1a · M1b PP 하락 설명. 카드 실물 RTX 5070 Ti(70 SM). `docs/engine-kernels-20261121.md`.
- 2026-11-21 · Claude Code · Q1-0c · G3(`g3-chain.ps1`, 07:24~09:04, 원장 47cb0f3 24행): 러너 `--model-id` · 서버 `-Model` 추가(c99d68d), 첫 실행은 `$r`/`$R` 버그로 중단 · 행 없음(903ce28 수정). M1b · M1a 5/12 vs M0 7/12 → 통과, 슬롯 88 · 85, PP −23% · −44%. q1-plan 13절.
- 2026-11-21 · Claude Code · 밤 체인 `nrg`(02:52~05:32, 04b1411, 원장 42행): run_tests 16/30 = 대조 16/30 → Q15 기각. greedy 8/12 vs 7/12, 초안 채택 84%, 출력 tok/s 이득 없음 → Q17 greedy 30회 후보. 끝나고 밤 모드(39a7d50).
- 2026-11-21 · Claude Code · Q1 imatrix 비교(`q1-var.ps1`, 02:10~02:36): M1a · M1b 를 I-unsloth · I-mix 로 다시 만들어 KL — 세 imatrix 차이는 오차 안(M1a 0.0538~0.0559, M1b 0.0556~0.0574) → **I-ours 로 결정**(사용자 위임). 11-21 밤 체인 `scripts/bench/nrg-chain.ps1`(be630f6): run_tests 30회 · greedy 6x2, 끝나면 밤 모드.

- 2026-11-21 · Claude Code · Q1 imatrix-mix 완료(11-20 22:43, 285.9분) · **G2 KL**(`scripts/quant/q1-g2.ps1`, 01:13~02:06, 기준 Q8_0 · kl.txt · ctx 2048 · 34청크): M0 0.0450 · R0 0.0429 · R0u 0.0449 · M1a 0.0539 · M1b 0.0556 · M1c 0.1018 · M1d 0.1300, top-1 96.03 → M1a 95.71 · M1b 95.52 · M1c 93.85 · M1d 93.01. 잠정 관문으로 M1a · M1b 통과, M1c · M1d 탈락. imatrix 비교 체인 `scripts/quant/q1-var.ps1`(M1a · M1b x I-unsloth · I-mix) 추가.

- 2026-11-20 · Claude Code · 워커 평가(사용자 요청: 시킬 워커로서 평가)를 다음 할 일 25(순서 제안 5단계)로 기록. MTP 기록 · 소스 정리 → 열린 질문 Q17 신설(q36 은 greedy 만 초안, SPEC_PROB 없음, 지금 이득 0). Q15 갱신: L1(`x3a6t`) 7/12 vs 5/12 가 30회 확인 없이 남아 있던 것을 찾음.

- 2026-11-20 · Claude Code · Q1 밤 체인 1부(`q1-night.ps1`, 14:32~17:51) · 2부 앞부분(`q1-after.ps1`, ~17:58): llama.cpp 빌드 3.5분, BF16 → Q8_0 1.6분(35.21GB, MTP 텐서 보존), 보정 세트 162파일, imatrix I-ours 400청크 162.6분(PPL 2.03), 후보 5개 3.2~9.9분씩(expert 18.7 · 17.3 · 16.6 · 15.0 · 14.2GiB), R0u = M0 와 텐서 753개 형식 같음. 메모리 최대 커밋 16.4GB · 페이지 파일 1.78GB(양자화 중). 결과 표 `docs/q1-plan-20261120.md` 11절. 모델 파일 등록(`model(quant)`)은 G2 뒤 고른 후보만.

- 2026-11-20 · Claude Code · 관리 문서 최신화: STATE '지금' · 단계 진행표 · 다음 할 일(20~24) · 열린 질문(Q4 · Q11 종결, Q9 · Q14 · Q16 갱신) · 사람 요청(페이지 파일 완료, Q1 결정 대기), `docs/plan-20261120.md` 진행 표시, Q1 상세 계획 `docs/q1-plan-20261120.md`(엔진 expert 형식 · M0 텐서 표 확인 반영), COLLAB-LOG C-019~021.
- 2026-11-20 · Claude Code · H2a + card-coding 6과제 x 5회(12:02~13:33): 8/30 vs 대조 16/30 → **H2a 기각**, **기준 샘플링 card-coding 확정**(기준 조합 H0 + card-coding). A4 원인 확인(x3a4d, STRATA_DEBUG): 재토큰화 1/67, 나머지 실패는 강제 턴의 도구 목록 제거 → **A4 보류**(X4 에서 재검토). BF16 원본 2개(71.07GB, sha256 일치) · llama.cpp v1.0.0(b1b770d) 다운로드 완료 — Q1-0 준비됨.
- 2026-11-20 · Claude Code · 하네스 후보 **C1 기각**(1~8회차 짝 48: 19 vs 19, 5:5, 시간 -6%). 밤 체인 결과: S1 card-coding 16/30 vs card-general 9/30(짝 9:2) · T1 출력 예산 16384 는 8/24 vs 6/24(짝 3:1, thinking +30% · 시간 +11%, 상한 도달 같음) → 상한 6,144 유지 · 64K X3 6/9 vs 3/9(판정 불가). 다음: BF16 원본 · llama.cpp v1.0.0 다운로드(서버 내린 상태) → H2a + card-coding 6과제 x 5회(`h2k-chain.ps1`, 대조 S1 의 `x3s1c`).
- 2026-11-19 · Claude Code · 사용자 결정: **정확도 우선**(속도는 정확도가 같을 때만), 하네스 채택 기준 30회 **-1 이내**로 강화, 손실 없는 개선 먼저, 바탕(ctx · 모델 · 엔진)이 바뀌면 확정 조합으로 한 번만 재확인, 밤에도 연속 체인. Claude Code CLI 설치(노트북 2.1.328). **채택 확인: H3 기각**(30회 H0 17 · H3 12, D · E · F 7 · 4), 기준 하네스 H0 유지. Codex 참고 상한 D · E · F 3/3. 하네스 후보 H6 · C1 · --force-at, 연속 체인(P-diag 1 → 64K → 하네스 추가 A/B(기준 H0) → H1 재확인), `docs/cache-ideas.md`(캐시 · 압축 · KV · expert 후보), 루프 · 멀티 턴 · 캐시 계획 `docs/loop-plan.md`(L0~L8, 오픈소스 에이전트 조사 포함), 전체 계획 `docs/plan-20261120.md`.
- 2026-11-19 · Claude Code · H3 A/B(30행, 4317f90): H0 10 · H3 9, 시간 −32% · 새로 읽은 입력 −79% → H3 채택 후보. run_tests 도구(Q15, --run-tests on 일 때만) · selftest, E1 · 64K 메모(`docs/E1-candidates.md`: q36 KV fp32 고정 · KV 옵션 없음, 프롬프트 끝 순환 상태 스냅샷 안). 사람: 페이지 파일 64GB 고정(커밋 한도 95GB) · Tailscale 무인 실행 · 업데이트 12-10 까지 중지 · 재부팅. RDP 는 암호 없는 로그인이라 불가, ssh 로 운영. `claude-local.ps1` 에 --strict-mcp-config.
- 2026-11-19 · Claude Code · H4 A/B(30행, bedf6b1): H0 11 · H4 11, H4 는 텍스트 블록 불일치를 없앴지만 강제 턴 문법 오류 2건 · 시간 +17% · 입력 +35% → 채택하지 않음. 다음 H3 = H1 + H2a. X3 확인 전용 과제 D · E · F 구현 · 검증(기준 실패 · 참조 통과 · 회귀 통과). 측정 중 `configs/` 에 새 파일을 만들어 git_dirty 위험 → 2분 만에 git 밖으로 옮김(영향 행 0, 원장 git_dirty 전부 0).
- 2026-11-19 · Claude Code · 대화 캐시 A/B(없음 · 512 · 1024, 원장 3행): q36 엔진이 옵션을 무시해 세 조건 같음, 후속 턴 재사용 0 재현. 엔진 소스로 원인 확정(T-013) — 든 토큰 전체가 앞부분일 때만 재사용, 체크포인트 없음. 서버 설정 변경 없이 H4 로. `serve-ctx.ps1 -CacheMib` 는 다른 엔진 경로용으로 남김.
- 2026-11-18 · Claude Code · 로컬 LLM 을 주 에이전트 · 워커로 쓰는 준비(`docs/WORKER.md`): `launch_serve.ps1`(WMI 운영 서버, 63초 준비), `scripts/worker/`(X3 탐색 루프 재사용, 별도 작업 트리 · 테스트 · 1회 보완 · 측정 체인 감지 · 잠금, 표준 라이브러리 MCP 서버), 자체 점검 5/5, 노트북 → ssh → MCP → STRATA 실제 1건 `done` 43초. `run_x3.navigate_loop` 강제 턴 기준을 인자로(`force_at`, 32K 값 불변). Codex 0.169 연결 확인 · 쓰기 샌드박스 문제는 X4 로. T-015(실행 정책) · T-016(옛 .pyc), T-013 원인 가설(대화 캐시 자동 꺼짐), Q16(64K 메모리 추정).
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
