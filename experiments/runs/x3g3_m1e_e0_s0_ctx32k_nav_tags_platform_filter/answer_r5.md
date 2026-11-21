수정 내용을 요약하면:

1. **`src/packaging/utils.py`**:
   - `from collections.abc import Iterable` import 추가
   - `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `None`이 아니면:
     - `str`을 직접 받으면 `TypeError` 던짐
     - 각 플랫폼 이름을 `.`·`-`·` ` → `_` 치환 + 소문자로 정규화하여 `frozenset`으로 저장
     - 태그의 platform이 `"any"`이거나 정규화된 플랫폼 집합에 포함되면 통과, 아니면 `InvalidWheelFilename` 던짐
   - docstring에 `platforms` 파라미터 설명 및 버전 정보 추가