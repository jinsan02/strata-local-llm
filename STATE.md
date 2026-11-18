# STATE.md — 지금 어디까지 왔나

사람과 에이전트(Codex, Claude Code)가 함께 고치는 진행 기록입니다. 작업을 끝낼 때마다 해당 줄을 고치고 '최근 변경' 맨 위에 한 줄 더합니다. 설계 내용 자체는 `docs/`에, 수치는 `experiments/LEDGER.tsv`에, 여기는 상태와 결정만 둡니다.

## 지금

- 마지막 갱신: 2026-11-18
- 단계: **X3 준비** (X0 · X1 · XB · X2 완료). 32K 설정에서 실제 입력 24K 까지 코딩 과제 답변 · 테스트 통과 확인 (탐색 세트, 24K 전부 통과 20/24)
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
| 긴 문맥 코딩 품질 | X3 | 32K | 미착수 | 지시 준수·코드 찾기·수정·테스트 통과·도구 호출 | 원장 |
| 노트북 경유 | X4 | 32K | 미착수 | 체감 지연(별도 행), tool calling·템플릿 호환 | 원장 `origin=laptop` |
| 실행 설정 튜닝 | B1 | 32K | 미착수 | S1, 병목 프로파일(KV·expert 캐시·버퍼 경쟁), 후보 순위 | 원장 |
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
10. 그다음 X3(긴 문맥 품질, Q8) → X4(노트북 경유, `origin=laptop`) → B1(Q11 greedy·MTP 포함)
11. push: 사용자가 커밋·push 를 맡김(11-18). 단계 커밋 묶음마다 `git push`

## 사람에게 요청한 것

| 날짜 | 요청 | 상태 |
| --- | --- | --- |
| 11-18 | 전원 구성표를 고성능으로 변경 (측정 위생) | 완료 (11-18 11:41): 고성능 + `scripts/power-max.ps1`(최소 CPU 100% · 코어 파킹 끔 · 부스트 적극 · 디스크·USB 절전 끔 · 최대 절전 끔), 기록 `env/power-*`. **X0 · X1 · XB 는 '균형 조정'에서, X2 부터 고성능에서 쟀다** |
| 11-18 | 양자화 단계 전 페이지 파일 확대 (예: 64GB) | 대기 |
| 11-18 | 커밋 작성자 이메일을 kotokenlab 과 같게 할지 결정 (지금은 noreply) | 완료: 사용자 계정 이메일로 (저장소 로컬 `user.email`, d818a2b 이후 커밋부터). 이전 커밋은 noreply 그대로 |
| 11-18 | 본체 방화벽에 Tailscale 대역만 허용하는 8080 규칙 추가 (명령은 `docs/ENVIRONMENT.md` '노트북에서 호출' 1) | 완료 (본체 규칙 1개, 100.64.0.0/10 · TCP 8080 확인. 노트북에 잘못 만든 규칙은 삭제됨) |

## 결정 기록

| 날짜 | 결정 | 근거 |
| --- | --- | --- |
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
| Q2 | 탐색·최종 평가 데이터 출처(공개·합성) | 공개 벤치 일부 + 합성, 출처·버전 기록 | B0 품질 측정 | 기획서 8절 |
| Q3 | qwen36 경로에서 `--kv int8\|q4_0\|k8v4\|fp16` 이 실제로 적용되는지 (launcher 에는 옵션이 있고 기본 int8, QWEN36.md 는 fp32 라고 적음) | M0 로딩 뒤 KV 메모리로 확인, 적용되면 B1 후보 | B1 탐색 목록 | `env/strata-plan-20261118.md` |
| Q9 | RAM 여유가 약 0.7GB 뿐이다 (엔진 private 35.6GB, 페이지 파일 자동 증가 최대 8GB). 32K 긴 입력에서 페이징이 늘면 `--resident-budget-gib` · `--low-ram` 조정이 필요할 수 있다 | X1·X2 에서 페이지 파일·`file_mb`·지연을 같이 보고 판단 | X2, B1 | X0 관측 |
| Q11 | MTP 를 쓰려면 greedy 가 필요한데, thinking 모델은 greedy 에서 반복 위험이 있다. 운영 샘플링을 greedy 로 바꿀지, `STRATA_SPEC_PROB` 가 qwen36 경로에서 통하는지 | B1 에서 같은 코딩 과제로 greedy vs 권장 샘플링 품질·속도 비교 | B1 | Q10 진단 |
| Q8 | X3 코딩 품질 탐색 세트의 출처 (긴 문맥 코드 수정·테스트) | 공개 저장소 일부로 합성한 과제 + 고정 단위 테스트, 최종 50문항과 분리 | X3 | 변경안 6절 |
| Q4 | 맞춤 양자화 원본(BF16 약 70GB) 확보·변환 방식 | 샤드 스트리밍 변환 가능성 먼저 소형 검사 | Q1 단계 | 기획서 6.3 |
| Q12 | thinking 상한을 서버 `reasoning_budget_tokens` 로 명시(b)할 때 값 — 11-18 토의로 (b) 방향, (c) 제외. 상세 `docs/TROUBLESHOOTING.md` T-007 | B1: max_tokens 8,192 고정, 상한 3K · 4.5K · 6K, 긴 답변 과제 추가 | B1, 클라이언트 설정 | XB 2차 |
| Q5 | API 사용량·비용 예산 상한 | 착수 시 사람이 정함 | 탐색 예산 | 기획서 5.2, 11절 |

## 에이전트 사용

- 지침은 루트와 폴더의 `AGENTS.md`. Codex 는 루트부터 지금 폴더까지 합쳐 읽는다.
- Claude Code 는 `CLAUDE.md` 가 있으면 `AGENTS.md` 를 자동으로 읽지 않는다. 그래서 `CLAUDE.md` 는 `@AGENTS.md` 한 줄로 불러온다. 지침을 `CLAUDE.md` 에 쓰지 않는다.
- 개인 기억(Claude 자동 메모리 등)은 저장소에 공유되지 않는다. 다음 세션이 알아야 할 것은 이 파일과 `docs/` 에 쓴다.

## 최근 변경

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
