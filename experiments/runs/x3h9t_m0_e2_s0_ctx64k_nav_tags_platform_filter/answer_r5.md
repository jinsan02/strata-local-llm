수정을 마쳤습니다. 다음을 변경했습니다:

1. **`src/packaging/utils.py`**:
   - `collections.abc.Iterable` import 추가
   - `parse_wheel_filename` 함수 시그니처에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `None`이 아닌 경우:
     - 인자가 `str`이면 `TypeError` 던짐
     - 각 플랫폼 이름을 `.`, `-`, 공백을 `_`로 바꾸고 소문자로 정규화하여 집합으로 저장
     - 태그 중 `platform == "any"`이거나 정규화된 플랫폼 이름과 일치하는 것이 있으면 통과
     - 일치하는 것이 없으면 `InvalidWheelFilename` 던짐
   - docstring에 `platforms` 파라미터 설명과 `TypeError` raise 항목 추가