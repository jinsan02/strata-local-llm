# AGENTS.md — Codex 진입점

> **규칙 본문은 여기에 없다.** 이 저장소의 규칙은 [`docs/RULES.md`](docs/RULES.md)
> 한 곳에만 있다. 규칙을 바꾸려면 그 파일을 고친다. 여기에 복사하지 마라 —
> 갈라진 규칙은 규칙이 아니다. 이 파일은 Codex 로 이 저장소를 다룰 때의
> 운영 메모다. Claude Code 쪽 대응 파일은 [`CLAUDE.md`](CLAUDE.md).

## 세션 시작할 때 이 순서로 읽는다

1. [`docs/RULES.md`](docs/RULES.md) — 하드룰. **매 세션 읽는다**
2. [`docs/WORKFLOW.md`](docs/WORKFLOW.md) — 실험 수명주기, 두 에이전트 교대
3. [`docs/COMMIT_CONVENTION.md`](docs/COMMIT_CONVENTION.md) — 커밋할 일이 있으면
4. [`docs/LEDGER_SCHEMA.md`](docs/LEDGER_SCHEMA.md) — 결과를 기록할 일이 있으면
5. [`docs/HANDOFF.md`](docs/HANDOFF.md) — 지금까지 된 것과 다음 할 일
6. [`docs/prep-plan-20261118.md`](docs/prep-plan-20261118.md) — 기획서 검토 결과와 보완점
7. [`docs/plan-v2.0.md`](docs/plan-v2.0.md) — 기획서 원본. 필요한 절만

그리고 현재 상태를 복원한다:

```bash
git log --oneline -20
git status
tail -n 15 experiments/LEDGER.tsv
```

Claude Code 가 직전 세션을 돌렸을 수도 있다. **앞선 대화를 알고 있다고 가정하지
않는다.** 상태는 커밋과 `experiments/` 에만 있다.

## 이 환경에서의 실행

- OS 는 Windows 11, 저장소 루트는 `C:\strata-lab`
- python 은 **항상 절대경로**로 부른다. `conda activate` 에 의존하지 않는다:

  ```
  C:\ProgramData\anaconda3\envs\strata_local_llm\python.exe
  ```

- GPU 는 RTX 5070 Ti 16GB 하나뿐이다. 측정·변환을 두 개 동시에 띄우지 않는다

### 샌드박스·승인

- 네트워크가 필요한 작업은 엔진 clone, 모델 다운로드(HuggingFace), conda-forge 뿐이다
- 파일 쓰기는 `C:\strata-lab` 안으로 제한한다. 다른 프로젝트 폴더는 **읽기 전용**
- `git push` 는 사용자 승인 후에만

## 긴 작업

빌드, 모델 다운로드, 양자화 변환, 벤치마크는 수십 분~수 시간이 걸린다.
타임아웃이 있는 실행 도구로 감싸지 말고, 로그를 파일로 떨어뜨린 뒤
`experiments/runs/<run_id>/` 를 확인하는 방식으로 진행한다.
시작 전에 예상 소요·VRAM·디스크를 사용자에게 말한다.

## 절대 하지 않는 것

- `git commit --no-verify` — 훅 우회. 훅이 막으면 커밋에 문제가 있는 것이다
- 원장 TSV 의 **기존 행 편집·삭제** — append-only다. 정정도 새 행
- `final_eval/` 을 읽거나 커밋 — 최종 평가를 오염시키는, 되돌릴 수 없는 실수
- 다른 프로젝트의 conda 환경 변경
- 실험 결과를 마크다운 일지로 손으로 적기 — 원장에 코드가 적는다
- **해시를 손으로 적기** — 원장에서 읽어온다. 훅이 대조해서 거부한다

## 막혔을 때

규칙과 코드가 어긋나 보이면 코드가 맞다. 훅과 검사기가 실제 집행자다:
[`tools/check_commit_msg.py`](tools/check_commit_msg.py),
[`tools/precheck.py`](tools/precheck.py),
[`tools/validate_ledger.py`](tools/validate_ledger.py).
