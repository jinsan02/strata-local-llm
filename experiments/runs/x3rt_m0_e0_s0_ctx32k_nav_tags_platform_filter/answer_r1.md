다음과 같이 수정했습니다:

1. **`src/packaging/utils.py`**
   - `typing.Iterable` import 추가
   - `tags._normalize_string` import 추가
   - `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `str`이면 `TypeError` 던짐
   - `platforms`가 `None`이 아니면 각 플랫폼 이름을 `_normalize_string` + `.lower()`로 정규화하고, 태그의 플랫폼 중 `"any"`이거나 정규화된 플랫폼 집합과 일치하는 것이 있으면 통과, 아니면 `InvalidWheelFilename` 던짐
   - docstring에 `platforms` 파라미터 설명 및 버전 정보 추가