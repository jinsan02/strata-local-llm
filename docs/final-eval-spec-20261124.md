# F1 최종 평가 문제 제작 명세 (Codex 용 초안, 2026-11-24)

> 상태: **초안 — 사용자 검토 전.** 저장소 선택 · 다운로드 승인 · Codex 실행 방식은 사용자가 정한다.
> 이 문서는 형식과 규칙만 담는다. 문제 내용은 들어 있지 않으며, 이 문서를 쓴 쪽(Claude Code, 튜닝 담당)은 만들어진 문제를 보지 않는다.

## 0. 배경 · 목적

- 프로젝트: 로컬 LLM(Qwen3.6-35B-A3B, Q4 양자화, STRATA 엔진)을 코딩 워커로 쓰기 위해 하네스 · 엔진 · 설정을 조정했다. 조정에는 X3(pypa/packaging 6과제)와 Y(packaging · flask 6과제)를 썼다.
- F1 은 **조정에 한 번도 쓰지 않은 문제**로 최종 설정의 실력을 재는 마지막 검증이다. 그래서 튜닝 담당(Claude Code)과 분리된 제작자(Codex)가 만든다. (`STATE.md` 열린 질문 Q2 권장안: 합성 30 + 최근 이슈 20. 이번 초안은 **합성 30** 만 다루고 이슈 기반 20 은 나중에 정한다.)

## 1. 분리 규칙 (반드시 지킴)

| # | 규칙 |
|---|---|
| S1 | 만든 파일은 본체 `C:\strata-lab\final_eval\` 아래에만 둔다. 이 폴더는 git 에서 제외돼 있고 커밋 훅이 막는다. **공개 저장소에 올리지 않는다** |
| S2 | 튜닝 담당(Claude Code)은 `final_eval/` 의 내용을 읽거나 출력하지 않는다. 검증 · 채점 스크립트는 **과제 ID 와 개수 · 통과 여부만** 화면에 낸다. 자세한 검증 기록은 `final_eval/_validation/` 에 파일로 남기고, 그 파일은 Codex 와 사람만 본다 |
| S3 | 튜닝에 쓴 저장소(**pypa/packaging, pallets/flask**)와 그 과제(`configs/eval/x3-packaging`, `configs/eval/y-set`)는 쓰지 않는다. 형식 참고로 `configs/eval/y-set/*/task.json` 의 **구조**만 볼 수 있다(내용은 베끼지 않는다) |
| S4 | 문제 제작 중 로컬 LLM 서버를 쓰지 않는다(모델이 문제를 미리 보면 안 됨) |
| S5 | 네트워크로 받는 것(저장소 · 패키지)은 사용자가 승인한 목록만. 새 conda 환경은 `final_*` 이름으로만 만들고, 기존 환경은 건드리지 않는다 |

## 2. 저장소 고르기

조건: 순수 Python · pytest 로 1분 안에 도는 테스트 · 의존성이 적음 · **`src/` 레이아웃**(하네스가 `PYTHONPATH=src` 로 돈다. `src/` 가 아니면 task.json 에 `"pythonpath": "."` 를 적고, 하네스 쪽 수정이 따로 필요) · 라이선스가 허용적.

권장 후보 (사용자가 3~4개 고름):

| 저장소 | 레이아웃 | 메모 |
|---|---|---|
| python-attrs/attrs | `src/attr`, `src/attrs` | 의존성 거의 없음, 테스트 풍부 |
| pallets/click | `src/click` | flask 와 같은 조직이지만 다른 저장소 |
| dateutil/dateutil | `src/dateutil` | 날짜 계산 · 파싱, 버그 심기 좋음 |
| pytest-dev/pluggy | `src/pluggy` | 작고 깔끔 |
| hukkin/tomli | `src/tomli` | 아주 작음(파서) |

- 레이아웃 · 테스트 시간은 기억에 기댄 것이라, 고른 뒤 고정 커밋에서 다시 확인한다.
- 각 저장소는 **고정 커밋 하나**로 쓴다(task.json 에 해시). 본체에 git bundle 로 둔다(`work/final/bundles/<repo>.bundle`).
- **11-24 확정(사용자)**: attrs 26.1.0(`7bfc49e9b22d5ba25b6e429524c3d49fee27cb36`) · click 8.5.1(`cf19179e8e2fd54c601378cec9e0d21bb12b6fb1`) · dateutil 4.0.0(`a78cbd81d5d03b5f126eb36edb92bca78972c804`) · pluggy 1.7.0(`4c7f6365f2dde09c11e72db67d0f615231d64c19`). task.json 의 `repo` 는 `attrs` · `click` · `dateutil` · `pluggy`.
- conda 환경은 네 저장소가 같이 쓰는 **`final_eval` 하나**(x3_packaging 을 오프라인 복제 + freezegun · tzdata · pympler · cloudpickle). freezegun 이 python-dateutil 패키지를 끌고 오지만 `PYTHONPATH=src` 가 앞서므로 시험 대상은 항상 저장소의 `src/` 다.
- dateutil 저장소 루트에 `AGENTS.md`(AI 에이전트 지침)가 있다. 모델이 과제 중에 읽을 수 있으니, 과제 내용과 부딪히지 않게 한다.

## 3. 과제 30개 구성

Y 세트와 같은 유형 분포로, 저장소마다 고르게 나눈다.

| 유형 | 개수 | 설명 | 채점 |
|---|---:|---|---|
| F1 버그 보고 | 6 | 증상 설명(재현 코드 · 기대 vs 실제)만 주고 원인은 찾게 한다 | 숨은 테스트 |
| F2 실패 테스트 | 6 | 기존 테스트가 실패하는 출력(pytest 로그)을 주고 소스를 고치게 한다 | 숨은 테스트 + 회귀 |
| F3 작은 기능 | 6 | 함수 · 옵션 하나 추가, 동작 명세를 글로 준다 | 숨은 테스트 |
| F4 여러 곳 연결 | 4 | 설정값 하나를 2~3개 파일에 걸쳐 이어야 하는 변경 | 숨은 테스트 |
| F5 리팩터링 | 4 | 동작은 그대로, 구조만 바꿈(함수 추출 · 이름 정리 등). 숨은 테스트가 새 구조(공개 이름)와 기존 동작을 함께 확인 | 숨은 테스트 + 회귀 |
| F6 테스트 작성 | 4 | 지정한 함수의 테스트 파일을 쓰게 한다 | 돌연변이(아래 4.3) |

- 난이도: 과제마다 `"difficulty": "easy|medium|hard"` 를 적고 대략 1/3 씩. hard 는 큰 파일(800줄 이상)이나 두 모듈 이상을 읽어야 하는 것.
- 버그는 **사람이 실제로 낼 법한 것**(경계값 · off-by-one · 잘못된 기본값 · 빠진 분기 · 정규식 · 타입 처리)으로 심는다. 코드를 크게 지우거나 무작위로 망가뜨리지 않는다.
- 모델이 기억으로 풀 수 없게: 심은 버그 · 요구 기능은 그 저장소의 실제 이력(이슈 · 커밋)을 그대로 옮기지 않는다.

## 4. 과제 폴더 형식 (Y 세트와 같음)

```
final_eval/<저장소>/<과제ID>/
  task.json
  prompt.md
  private/
    setup.patch        # 버그 심기 등 출발 상태 (F2 · F1 · F5 에서 필요할 때)
    test_x3_hidden.py  # 숨은 테스트 (F6 은 없음)
    ref.patch          # 참조 해답 (F6 은 private/ref_test.py)
    mutants/*.patch    # F6 만
```

과제 ID 는 `f<유형번호>_<저장소 약자>_<짧은 이름>` (예: `f2_attrs_validator_order`).

### 4.1 task.json

```json
{
  "task": "f2_attrs_validator_order",
  "type": "F2 실패 테스트",
  "difficulty": "medium",
  "repo": "attrs",
  "commit": "<고정 커밋 40자>",
  "setup_patch": "private/setup.patch",
  "required_files": ["src/attr/_make.py"],
  "regress": ["tests/test_make.py"],
  "hidden_test": "private/test_x3_hidden.py",
  "ref_patch": "private/ref.patch"
}
```

- `required_files`: 고쳐야 하는 파일(채점에는 안 쓰고 분석용).
- `regress`: 저장소 기존 테스트 파일 중 이 변경과 관련된 것(1~3개, 합쳐 60초 안). 기준 커밋에서 실패하는 테스트가 있으면 `--deselect` 로 빼고 `"_regress_note"` 에 이유.
- F6 은 Y3 형식: `"grade": "mutants"`, `"test_file"`, `"write_allow": [test_file]`, `"kill_min"`, `"ref_test"`, 그리고 **`"copy_from"`**(대상 함수를 다루는 저장소 기존 테스트 파일 경로 — V7 검사에 쓴다).

### 4.2 prompt.md

- 한국어. 사람이 동료에게 맡기듯 자연스럽게. 고칠 파일 이름이나 정답 위치를 직접 알려 주지 않는다(F2 의 pytest 출력에 파일 · 줄이 보이는 것은 괜찮다).
- 끝에 공통 규칙 줄: "테스트 파일은 고치지 마라." (F6 은 "새로 만들 파일: <test_file>").
- 숨은 테스트가 확인하는 동작은 **prompt 에 모두 적혀 있어야 한다**(지시에 없는 것을 채점하지 않는다).

### 4.3 숨은 테스트 · 돌연변이

- 숨은 테스트: 공개 API 로만 확인(내부 함수 이름 · 구현 방식을 강제하지 않음. F5 는 prompt 에 적은 새 공개 이름은 확인 가능). 테스트 6~20개, 결정적(시간 · 난수 · 네트워크 · 파일 시스템 바깥 의존 없음).
- F6 돌연변이: 대상 함수에 사람이 낼 법한 버그 8~12개를 각각 패치로. `ref_test.py` 는 전부 잡아야 하고, `kill_min` 은 대략 70%.

## 5. 검증 기준 (본체 자동 검사, 과제마다 모두 통과해야 채택)

| # | 검사 |
|---|---|
| V1 | 고정 커밋 + setup.patch 가 깨끗하게 적용된다 |
| V2 | 기준 상태(setup 뒤)에서 숨은 테스트가 **하나 이상 실패**한다 (F6: 기준 상태에서 ref_test 통과) |
| V3 | 참조 패치를 넣으면 숨은 테스트 **전부 통과**, 회귀 테스트 **전부 통과** (F6: ref_test 가 돌연변이를 전부 잡음) |
| V4 | 참조 패치는 `src/` 아래만 바꾼다(F6 은 test_file 만) |
| V5 | 숨은 테스트 + 회귀 테스트가 60초 안에 끝난다 |
| V6 | 같은 검사를 두 번 돌려 결과가 같다(흔들리는 테스트 없음) |
| V7 | (F6) 저장소 기존 테스트 파일을 그대로 test_file 로 복사하면 kill_min 미만이다(기존 테스트 베끼기로 통과 못 함 — Y3 의 한계 보완) |

검증은 본체 스크립트 `validate_final.py`(튜닝 담당이 만든다, 내용을 출력하지 않음)로 돌리고, 과제별 자세한 결과는 `final_eval/_validation/<과제ID>.json` 에 쓴다. Codex 는 그 파일을 보고 실패한 과제를 고친다.

## 6. 작업 흐름

1. **사용자**: 저장소 3~4개 선택, 저장소 clone · conda 환경 생성 승인.
2. **튜닝 담당(Claude Code)**: 본체에 저장소 bundle · `final_*` 환경 준비, `validate_final.py` · 하네스의 저장소 등록(`run_x3.py REPOS`)을 만든다. 문제 내용에는 손대지 않는다.
3. **Codex(노트북, 클라우드 모델)**: 이 명세대로 과제를 만든다. 노트북에는 Python 이 없으므로 테스트 실행 · 검증은 본체에서 한다 — Codex 가 `ssh desktop-5070` 으로 `final_eval/` 에 올리고 `validate_final.py` 를 돌려 `_validation/` 결과를 보며 고친다.
4. **사용자**: 과제 목록(ID · 유형 · 난이도 · prompt 요약)을 훑어보고 승인.
5. **튜닝 담당**: 확정된 운영 설정으로 F1 을 돌린다(과제별 1회 또는 3회, 결과는 개수 · 통과율만 본다).

## 7. Codex 에게 줄 첫 지시 (초안)

```
너는 로컬 LLM 코딩 워커의 최종 평가 문제를 만드는 출제자다. 첨부한 명세(final-eval-spec-20261124.md)를 그대로 따른다.
- 저장소: <사용자가 고른 목록>, 각 고정 커밋은 본체 bundle 의 HEAD.
- 이번 차례: <저장소 하나>에서 유형별로 <개수>개.
- 결과는 본체 C:\strata-lab\final_eval\<저장소>\<과제ID>\ 에 4절 형식으로 올리고,
  `ssh desktop-5070 "<python> C:\strata-lab\scripts\bench\validate_final.py <과제ID>"` 로 검증한 뒤
  final_eval\_validation\<과제ID>.json 을 보고 V1~V7 이 모두 통과할 때까지 고친다.
- packaging · flask 와 configs/eval 의 과제 내용은 보지 않는다. 형식은 이 명세만 따른다.
- 로컬 LLM 서버(127.0.0.1:8080)는 쓰지 않는다.
```

## 8. 열린 결정 (사용자)

| # | 정할 것 | 권장 |
|---|---|---|
| D1 | 저장소 3~4개 | attrs · click · dateutil (+ pluggy) |
| D2 | Codex 실행 위치 | 노트북 Codex CLI(클라우드 모델), 본체에는 설치하지 않음 |
| D3 | F1 반복 횟수 | 과제당 3회(90회), 통과율과 과제별 3/3 · 2/3 분포를 같이 본다 |
| D4 | 이슈 기반 20개 | 합성 30 의 결과를 본 뒤 결정 |
| D5 | 사람 승인 범위 | 과제 목록 · prompt 요약만(숨은 테스트까지 볼지는 선택) |
