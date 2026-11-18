# 작업 흐름

## 실험 1건의 수명 (기획서 5.1)

```
   1. 병목 하나 지정           기준선·프로파일을 읽고 가설을 적는다
            ↓
   2. config 작성             configs/<phase>/<name>.json
            ↓
   3. 사전 검사               파일 호환성 · 빌드 · 수치 정확성 · 최소 추론
            ↓
   4. 교차 측정               같은 PC 에서 기준선과 후보를 번갈아 → 원장 start/ok/fail
            ↓
   5. 요약 정리               experiments/runs/<run_id>/ , reports/
            ↓
   6. record 커밋             git add experiments/ reports/
```

`record` 커밋에 코드를 섞으면 훅이 거부한다. 자세한 것은
[COMMIT_CONVENTION.md](COMMIT_CONVENTION.md).

---

## 두 에이전트가 교대로 일하는 법

이 저장소는 **Claude Code** 와 **Codex** 가 번갈아 작업할 수 있다.
서로의 대화 맥락은 볼 수 없다. 그래서:

> **상태 공유 채널은 커밋과 `experiments/` 뿐이다.**

### 세션을 시작할 때 (양쪽 공통)

```bash
git log --oneline -20
git status
tail -n 15 experiments/LEDGER.tsv
nvidia-smi --query-gpu=memory.used --format=csv
```

### 세션을 끝낼 때

- 돌린 측정은 원장에 남기고 커밋한다. **커밋되지 않은 결과는 없는 결과다**
- 작업이 중간이면 그 사실을 커밋 메시지 본문과 [`HANDOFF.md`](HANDOFF.md) 에 적는다
- `git status` 를 깨끗하게 두거나, 남긴 이유를 커밋에 적는다

### 규칙을 고칠 때

[`docs/RULES.md`](RULES.md) **한 곳만** 고친다.

---

## 자주 쓰는 명령

```powershell
# 측정 전: 백그라운드 정리 + 메모리 기록
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\cleanup.ps1

# 테스트 (훅 본체)
C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe -m pytest tests -q

# 원장 검사 (pre-commit 이 자동으로 돌리지만 수동으로도)
C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe tools\validate_ledger.py

# 훅 연결 (클론 직후 한 번)
git config core.hooksPath .githooks
```
