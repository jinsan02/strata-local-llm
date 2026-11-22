수정을 완료했습니다. 다음을 변경했습니다:

1. **`src/packaging/utils.py`**:
   - `collections.abc.Iterable` import 추가
   - `parse_wheel_filename` 함수에 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가
   - `platforms`가 `str`이면 `TypeError` 발생
   - 주어진 플랫폼 이름들을 `.`, `-`, ` ` → `_` 로 바꾸고 소문자로 정규화하여 비교
   - 태그 중 `platform == "any"`인 것이 있거나 정규화된 플랫폼과 일치하는 것이 있으면 통과
   - 일치하는 태그가 없으면 `InvalidWheelFilename` 발생
   - 기존 동작 (`platforms=None`) 은 변경 없음