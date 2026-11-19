# X3 평가 과제 — pypa/packaging (탐색 평가, Q8)

최종 50문항과 분리된 **탐색 세트**다. 이 과제와 변형은 최종 평가(F1)에 쓰지 않는다.

## 출처 고정

| 항목 | 값 |
| --- | --- |
| 저장소 | https://github.com/pypa/packaging |
| 커밋 | `6a69a83d8d89c6a01d554a8ad1b420cbb45fb4bc` (2026-11-17, "perf(ranges): keep closures out of VersionRange._build (#1551)") |
| 라이선스 | Apache-2.0 또는 BSD-2-Clause 이중 라이선스 (`LICENSE`, `LICENSE.APACHE`, `LICENSE.BSD`). 과제 파일은 원 코드를 복사하지 않고, 실행 시 고정 커밋을 clone 해서 쓴다 |
| 실행 Python | conda 환경 `x3_packaging` (conda-forge): Python 3.12, pytest 9.x, pretend, hypothesis, tomli-w (`requires-python >= 3.10`, 테스트 의존성은 `pyproject.toml [dependency-groups] test`) |
| 테스트 명령 | 작업 복사본 루트에서 `PYTHONPATH=src python -m pytest -q -p no:cacheprovider -o addopts= <파일>` — conda 의 pytest 가 site-packages 에 packaging 을 깔아 두므로 `src` 를 앞에 둔다 |
| 작업 복사본 | 실행마다 `work/x3-runs/<run>` 에 고정 커밋을 새로 clone (깨끗한 상태에서 시작) |

## 비공개 자료

`<과제>/private/` 의 `ref.patch`(참조 패치)와 `test_x3_hidden.py`(채점 테스트)는 모델 입력과 작업 복사본에 들어가지 않는다. 채점할 때만 `tests/` 에 잠시 복사하고 지운다. 실패 로그(보완 단계)에는 일반 CI 처럼 실패한 테스트 이름과 assert 줄이 보인다.

## 과제 6개 설계 (우선 3개 구현)

| ID | 유형 | 과제 | 필수 파일 | 회귀 테스트 | 상태 |
| --- | --- | --- | --- | --- | --- |
| `dg_group_names` | **A** 한 파일의 규칙 → 다른 파일 호출부 | dependency group 이름을 core metadata Name 규칙(utils 의 기존 구현)으로 검사. `InvalidGroupName` 공개 예외, 생성 시 오류 묶음에 수집, lookup · resolve 는 단일 예외 | `dependency_groups.py`, `utils.py`, `errors.py` | `test_dependency_groups.py`, `test_utils.py` | 구현 · 검증 |
| `marker_extras` | **B** 두 모듈 동시 수정 | `Marker.referenced_extras()` (중첩 마커 구조 순회, `extra` 비교 · `in extras`, 정규화) + `Requirement.marker_extras` | `markers.py`, `requirements.py` | `test_markers.py`, `test_requirements.py` | 구현 · 검증 |
| `version_bump` | **C** 실패 로그 보고 1회 보완 | `Version.bump(part)` — 길이 유지 · 0 채움 · epoch 유지 · pre/post/dev/local 제거 · 대소문자 엄격 | `version.py` | `test_version.py` | 구현 · 검증 |
| `tags_platform_filter` | A | `tags.py` 의 플랫폼 태그 규칙을 읽고 `utils.parse_wheel_filename` 에 플랫폼 필터 인자 추가 | `tags.py`, `utils.py` | `test_tags.py`, `test_utils.py` | 구현 · 검증 (11-19, 확인 전용) |
| `metadata_extra_dupes` | B | 메타데이터 `Provides-Extra` 정규화 후 중복 검사 + `Requires-Dist` 마커가 선언되지 않은 extra 를 쓰면 오류 (metadata · markers) | `metadata.py`, `markers.py`, `_parser.py` | `test_metadata.py`, `test_markers.py` | 구현 · 검증 (11-19, 확인 전용). markers 는 읽기만(과제 B 의 `referenced_extras` 와 겹치지 않게) |
| `specifier_bounds` | C | `SpecifierSet` 에서 하한 · 상한 버전을 계산하는 메서드 (포함/제외 경계, `~=` · `==*` 처리) | `specifiers.py`, `version.py` | `test_specifiers.py` | 구현 · 검증 (11-19, 확인 전용) |

모든 과제는 공통 지시(편집 블록 형식)를 붙인다. 형식: `### EDIT: <경로>` + `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE`.

## 검증 (기준 실패 · 참조 통과) — `validation.json`

| 과제 | 기준 커밋 새 테스트 | 기준 커밋 회귀 | 참조 패치 새 테스트 | 참조 패치 회귀 |
| --- | --- | --- | --- | --- |
| dg_group_names | 10 failed, 4 passed (실패) | 통과 | 14 passed | 129 passed |
| marker_extras | 11 failed | 통과 | 11 passed | 7,921 passed, 1 skipped |
| version_bump | 16 failed | 통과 | 16 passed | 51,524 passed |
| tags_platform_filter | 18 failed, 1 passed (실패) | 통과 (317) | 19 passed | 317 passed |
| metadata_extra_dupes | 10 failed, 10 passed (실패) | 통과 (2,854) | 20 passed | 2,854 passed |
| specifier_bounds | 30 failed | 통과 (2,108, 2 skipped) | 30 passed | 2,108 passed, 2 skipped |

D · E · F 는 `scripts/bench/make_def.py` 가 고정 커밋 사본에서 참조 패치를 뽑아 만들고(원본 불변, `git apply --check`),
`scripts/bench/validate_def.py` 가 측정 체인이 없을 때 검증한다. **확인 전용**: 하네스 튜닝 · 비교에 쓰지 않고 채택 확인에만 쓴다.

## 실행 방식 (`scripts/bench/run_x3.py`)

- **preload (길이 효과 · 수정 능력):** 앞에 의존하지 않는 패딩 파일(고정 목록 · 순서, 16K 는 24K 의 앞부분) → 필수 파일(항상 같은 순서 · 위치) → 과제 · 형식. 입력 목표: 필수 파일만(dg 약 8K, marker · version 약 12K — **8K 는 필수 파일만으로도 넘어 불가**), 16,384, 24,320. 첫 패치가 실패하면 테스트 로그(최대 4,000자)를 주고 1회 보완(그 요청의 예산은 32K 에서 남는 만큼, 최대 8,192).
- **navigate (탐색 확인):** 파일을 넣지 않고 `list_files` · `grep` · `read_file` 도구만 준다. 필수 파일을 실제로 `read_file` 했는지 도구 로그로 판정. 모든 필수 파일을 미리 넣은 preload 결과로 탐색 성공률을 계산하지 않는다.
- 기록: 첫 패치 통과 / 보완 후 통과, 회귀, 입력 · 출력 토큰, 모델 시간과 도구 · 테스트 시간 분리, 오류 유형(`no_edit` · `apply_fail` · `import_or_syntax` · `test_fail` · `regress_fail` · `pass`).
