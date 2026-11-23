수정 내용 요약:

1. **`typing.Iterable` import 추가** — `Iterable[str] | None` 타입을 위해 `src/packaging/utils.py`의 import에 추가.

2. **`_normalize_platform` 헬퍼 함수 추가** — `packaging.tags.Tag`와 동일한 정규화 규칙(`.`·`-`·공백 → `_`, 소문자)을 적용.

3. **`parse_wheel_filename` 함수 수정**:
   - 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가.
   - `platforms`가 `None`이 아니면 `str` 직접 전달 시 `TypeError` 던짐.
   - 주어진 플랫폼 이름들을 정규화한 `frozenset`을 만들고, 태그 중 하나라도 `"any"`이거나 정규화된 이름이 집합에 있으면 통과.
   - 통과 못 하면 `InvalidWheelFilename` 던짐.
   - `platforms=None`(기본값)이면 기존 동작 그대로.