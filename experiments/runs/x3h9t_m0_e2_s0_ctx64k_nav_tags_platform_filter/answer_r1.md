수정 내용 요약:

- `src/packaging/utils.py` 수정:
  - `from collections.abc import Iterable` import 추가
  - `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
  - `platforms`가 `None`이 아니면:
    - `isinstance(platforms, str)` → `TypeError` 던짐
    - 각 플랫폼 이름을 `.`·`-`·` `를 `_`로 바꾸고 소문자로 정규화하여 `frozenset`으로 저장
    - 태그의 플랫폼이 `"any"`이거나 정규화된 플랫폼 목록과 일치하면 통과, 하나도 없으면 `InvalidWheelFilename` 던짐
  - docstring에 `platforms` 파라미터 설명과 `.. versionadded:: 26.4` 추가

기존 테스트 317개 모두 통과.