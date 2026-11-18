# GitHub 규칙

혼자 + AI 에이전트로 일하지만, 나중에 다시 보거나 다른 에이전트가 이어받을 수 있게 이력을 남깁니다. 커밋 형식은 [jinsan02/kotokenlab](https://github.com/jinsan02/kotokenlab) 과 같고, 자세한 것은 [`docs/COMMIT_CONVENTION.md`](docs/COMMIT_CONVENTION.md) 입니다.

## 1. 한 바퀴 = 가설 하나

1. 이슈를 연다 — 템플릿 '실험'(가설 · 바꿀 것 · 기대 지표 · 품질 위험 · 확인 방법, 기획서 5.1-2) 또는 '버그'.
2. 브랜치를 만든다 — `main` 에서 `exp/<phase>-<slug>`.
3. 코드·설정 커밋(`feat`/`fix`/`upgrade`/`chore`) → 측정 → 결과 커밋(`record`).
4. PR 을 연다 — 템플릿을 채우고 `Closes #번호`.
5. 스스로 리뷰하고 CI 초록을 확인한 뒤 머지. 실패한 가설도 `record` 로 남기고 이슈를 닫는다.

환경 준비·문서처럼 가설이 없는 작업은 이슈 없이 `main` 에 바로 커밋해도 된다. 측정 결과가 들어가는 작업은 브랜치와 PR 을 거친다.

## 2. 브랜치

| 패턴 | 용도 |
| --- | --- |
| `main` | 항상 초록. 훅·CI 를 통과한 것만 |
| `exp/<phase>-<slug>` | 실험. 예 `exp/config-expert-cache`, `exp/quant-m1-attn-q6`, `exp/engine-prefetch` |
| `fix/<slug>` | 버그 수정 |
| `docs/<slug>` | 문서 |

Codex 와 Claude Code 를 비교할 때는 도구별 브랜치(`exp/<phase>-<slug>-codex`, `-claude`)와 실험 ID 를 나누고, 모델·엔진 파일을 동시에 고치지 않는다 (기획서 5절).

## 3. 커밋 메시지

```
<type>(<scope>): <제목>

<본문 — 왜>

<트레일러>
```

type · scope · 트레일러 · 예시는 [`docs/COMMIT_CONVENTION.md`](docs/COMMIT_CONVENTION.md). 훅이 집행한다.

## 4. PR

- 템플릿의 확인 항목을 채운다. 돌린 명령과 결과를 그대로 쓴다. 못 돌렸으면 못 돌렸다고 쓴다.
- 머지는 **Merge commit** 으로 한다. `record` 커밋과 코드 커밋을 따로 남겨야 하므로 squash 하지 않는다.
- force push 는 사람 승인을 받은 경우에만.

### 4-1. CI (`.github/workflows/ci.yml`)

push · PR 마다 GPU 없이 돈다: 훅 단위 테스트 → 원장 무결성 → 범위 안 모든 커밋 메시지 규칙. 로컬 훅을 우회했거나 웹에서 고친 커밋을 여기서 잡는다.

## 5. 이슈

| 템플릿 | 언제 |
| --- | --- |
| 실험 | 가설 하나를 시험할 때. 구성 ID(B1·Q1·E1 …)와 기준선 run_id 를 적는다 |
| 버그 | 측정 도구·스크립트·훅이 틀렸을 때. 무효가 될 수 있는 run 을 적는다 |

라벨: `experiment` `bug` `env` `engine` `config` `quant` `bench` `eval` `docs`

## 6. 태그

되돌릴 수 없는 결정 지점에만 붙인다: `m0-e0-freeze`, `eval-freeze-v1`, `final-eval-opened`. 뜻은 [`docs/COMMIT_CONVENTION.md`](docs/COMMIT_CONVENTION.md).

## 7. AI 에이전트로 작업할 때

- `AGENTS.md` 의 시작 순서를 따른다. 끝나면 `STATE.md` 를 고친다.
- 에이전트 커밋은 `Co-Authored-By:` 트레일러를 남긴다.
- push 는 사람 승인 후. 본체는 저장소 전용 deploy key(`~/.ssh/strata_deploy`)로 push 한다.

## 8. 처음 받을 때

```powershell
git clone git@github.com:jinsan02/strata-local-llm.git C:\strata-lab
cd C:\strata-lab
git config core.hooksPath .githooks
powershell -NoProfile -ExecutionPolicy Bypass -File verify.ps1
```

conda 환경은 `docs/ENVIRONMENT.md` 대로 만든다.
