다음과 같이 수정했습니다:

1. **`src/packaging/utils.py`**:
   - `from collections.abc import Iterable` import 추가
   - `from .tags import ... _normalize_string, ...` import 추가
   - `parse_wheel_filename` 함수 시그니처에 `platforms: Iterable[str] | None = None` 키워드 전용 파라미터 추가
   - docstring 에 platforms 파라미터 설명, `:raises TypeError`, `.. versionadded:: 26.4` 추가
   - 함수 본문에 platforms 검증 로직 추가:
     - `platforms` 가 `str` 이면 `TypeError` 던짐
     - `platforms` 가 `None` 이 아니면 `_normalize_string` 으로 정규화하여 `frozenset` 으로 저장
     - 태그 중 `platform == "any"` 이면 통과
     - 태그 중 정규화된 platform 이 `normalized_platforms` 에 있으면 통과
     - 모두 아니면 `InvalidWheelFilename` 던짐