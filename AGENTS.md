# AGENTS.md — strata-local-llm

Codex와 Claude Code가 함께 읽는 작업 지침입니다(Claude Code는 `CLAUDE.md`가 이 파일을 불러옵니다). 사람이 채팅에서 직접 지시한 내용이 이 파일보다 우선합니다. 하위 폴더의 `AGENTS.md`는 그 폴더 안에서 이 파일보다 우선합니다.

## 프로젝트

RTX 5070 Ti 16GB · RAM 32GB 본체(`desktop-5070`) 한 대에서 [Niko1221/Strata](https://github.com/Niko1221/Strata)로 MoE 모델을 돌리고, 한국어·코딩 품질을 지키면서 실행 설정 → 레이어별 맞춤 양자화 → 엔진 코드 순으로 최적화한다. 1인 + AI 에이전트 작업이다. 설계는 기획서 `docs/plan-v2.0.md`가 기준이고, 실행 전 보완점은 `docs/prep-plan-20261118.md`에 있다. 지금은 착수 게이트(환경 준비) 단계이고 측정한 수치는 없다.

## 작업 시작 순서

1. `STATE.md`에서 지금 단계, 다음 할 일, 열린 질문을 확인한다.
2. `STRUCTURE.md`에서 고칠 폴더·파일의 역할과 기준 문서를 확인한다.
3. `docs/RULES.md`(하드룰)를 읽는다. **매 세션 읽는다.**
4. 작업할 폴더의 `README.md`와 `AGENTS.md`를 읽는다.
5. 아래 기준 문서 중 필요한 절만 읽는다.

현재 상태를 복원하는 명령:

```bash
git log --oneline -20
git status
tail -n 15 experiments/LEDGER.tsv
```

앞 세션의 대화를 기억하고 있다고 가정하지 않는다. 상태는 커밋, `STATE.md`, `experiments/`에만 있다.

## 기준 문서

| 무엇 | 기준 | 비고 |
| --- | --- | --- |
| 하드룰 | `docs/RULES.md` | 규칙은 여기에만 쓴다. 다른 파일에 복사하지 않는다 |
| 목표·범위·단계·채택 기준 | `docs/plan-v2.0.md` | 원본. 고치지 않는다 |
| 실행 전 보완점, M0 후보, 툴체인 조합 | `docs/prep-plan-20261118.md` | 기획서와 다르면 이 문서가 최신 판단 |
| 커밋·브랜치·태그 | `docs/COMMIT_CONVENTION.md`, `CONTRIBUTING.md` | 훅이 집행한다 |
| 원장 열 | `docs/LEDGER_SCHEMA.md` + `tools/validate_ledger.py` | 둘이 다르면 코드가 맞다 |
| 실험 1건의 순서 | `docs/WORKFLOW.md` | |
| 하드웨어·툴체인·conda | `docs/ENVIRONMENT.md`, `env/hw-20261118.md` | |
| STRATA 옵션·모델·양자화 지원 | `engine/` 고정 커밋의 `docs/` (`MODELS.md`, `QWEN36.md`, `QUANTS.md`, `DETAILS.md`) | main 문서가 아니라 고정 커밋 기준 |

코드와 기준 문서가 다르면 둘 중 하나를 마음대로 고치지 말고, 차이를 사람에게 알린다.

## 바꾸면 안 되는 실험 조건

규칙 본문은 `docs/RULES.md`. 여기는 무엇이 있는지만 적는다.

| RULES | 요지 |
| --- | --- |
| 1 | 엔진은 Niko1221/Strata 고정 커밋 하나. 다른 엔진으로 대체하지 않는다 |
| 2 | 최종 평가 50문항(`final_eval/`)은 후보 고정 전까지 열지 않는다 |
| 3 | 평가 정답·측정 시계·채점기·기준선을 바꿔서 수치를 올리지 않는다 |
| 4 · 5 | `record` 커밋에 코드를 섞지 않는다. 원장은 append-only, 코드가 쓴다 |
| 6 · 7 | 같은 PC 교차 측정, 8K · parallel 1 이 목표 조건 |
| 8 · 9 | 원본 모델·엔진·원시 결과 덮어쓰기 금지, 바이너리·비밀값 커밋 금지 |
| 10 · 11 | 훅 우회 금지, 탐색 예산 지키기 |

## 큰 실수를 막는 규칙

- **측정은 정리 후에:** 측정 전 `scripts/cleanup.ps1`, 전원 구성표 고성능, 워밍업. 다른 GPU 작업을 동시에 띄우지 않는다.
- **tok/s 는 엔진 보고값으로만.** SSE 조각·문자 수로 계산하지 않는다. MTP draft 토큰과 채택 토큰을 구분한다.
- **reasoning 을 끄거나 답을 짧게 만드는 변경은 처리량 개선이 아니다.** 따로 표시한다.
- **8K 를 못 채운 결과를 8K 달성으로 적지 않는다.** 축소 조건은 진단용.
- **STRATA 옵션은 고정 커밋에 실제로 있는 것만 쓴다.** llama.cpp 옵션을 그대로 대입하지 않는다.
- **정해지지 않은 것은 고르지 않는다:** `STATE.md` 열린 질문. 정해지기 전에 필요하면 묻는다.
- 새 conda 패키지는 conda-forge 에서만, 더하면 `env/strata_local_llm.yml` 도 고친다.

## 명령

대상 PC 는 `desktop-5070`(Windows 11, 저장소 `C:\strata-lab`). 노트북에서 작업하면 SSH 로 원격 실행한다. 긴 PowerShell 은 따옴표가 깨지므로 `-EncodedCommand` 나 스크립트 파일로 넘긴다.

```bash
ssh desktop-5070 "cd /d C:\strata-lab && git status"
```

Python 은 conda 환경 **`strata_local_llm`**(Python 3.12, conda-forge)을 절대경로로 부른다. `conda activate` 에 의존하지 않는다. 다른 conda 환경(`C:\Miniconda3`, `C:\llm_tokenizer\.conda` 등)은 다른 프로젝트 것이라 쓰지도 고치지도 않는다.

```
C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe
```

### 검증 (커밋 전)

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File verify.ps1
```

- 훅 단위 테스트(pytest) → 원장 무결성 → 아직 push 안 한 커밋의 메시지 규칙을 한 번에 돈다.
- 훅 연결은 클론 직후 한 번: `git config core.hooksPath .githooks`

## 긴 작업

빌드, 모델 다운로드, 양자화 변환, 벤치마크는 수십 분~수 시간이 걸린다.

- 시작 전에 예상 소요·VRAM·RAM·디스크·다운로드 크기를 사람에게 말한다.
- 백그라운드로 띄우고 로그를 파일로 떨어뜨린다. 폴링하지 않는다.
- 화면이 필요한 작업(Navigator, 프로파일러 등)은 본체 데스크톱에 띄워도 된다. 사람이 원격 데스크톱으로 본다.

## 금지

- `git commit --no-verify`, 원장 기존 행 편집·삭제, 해시 손으로 적기.
- `final_eval/` 을 읽거나 커밋하기.
- API 키·토큰·비밀번호를 파일에 쓰거나 커밋하기. 배포 키 개인키(`~/.ssh/strata_deploy`)를 옮기기.
- 사람에게 묻지 않고 대용량 다운로드(모델·원본 가중치), 시스템 설정 변경(전원 구성표·페이지 파일·드라이버), 프로그램 설치.
- 사람 승인 없이 `git push`, force push.
- 테스트를 통과시키려고 테스트·허용 오차·훅을 약하게 고치기. 허용 오차는 결과를 보기 전에 정한다.

## 쓰는 방식

- 문서·주석·커밋 메시지는 한국어, 코드 식별자는 영어.
- 새 폴더를 만들면 역할을 적은 `README.md` 를 같이 만들고 `STRUCTURE.md` 트리에 한 줄 더한다.
- 커밋 메시지는 `<type>(<scope>): <제목>` — `docs/COMMIT_CONVENTION.md`. 에이전트 커밋은 `Co-Authored-By:` 를 남긴다.
- GitHub 흐름(이슈·브랜치·PR)은 `CONTRIBUTING.md`.

## 작업을 끝낼 때

1. 돌린 테스트·측정과 결과를 그대로 보고한다. 못 돌렸으면 못 돌렸다고 쓴다.
2. `STATE.md` 의 단계 진행표, '다음 할 일', '최근 변경'을 고친다.
3. 새로 정한 것이 있으면 `STATE.md` '결정 기록'에 한 줄 쓰고, 해당 기준 문서도 고친다.
4. 측정 결과는 원장에 남기고 `record` 로 커밋한다. 커밋되지 않은 결과는 없는 결과다.
