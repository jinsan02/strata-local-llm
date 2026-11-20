수정 내용을 요약하면:

1. **`src/packaging/utils.py`**에서 `parse_wheel_filename` 함수를 수정:
   - 키워드 전용 인자 `platforms=None` 추가 (기본값 `None`이면 기존 동작과 동일)
   - `platforms`가 `str`이면 즉시 `TypeError` 발생
   - `platforms`가 제공되면 `_normalize_string(p).lower()`로 정규화해 집합으로 저장 (`.`/`-`/공백 → `_`, 소문자)
   - 파일 이름 기본 검사(확장자, 파트 수, 이름, 버전, 빌드 번호, 태그)가 먼저 통과한 후 플랫폼 필터링 수행
   - 태그의 플랫폼이 `"any"`이면 어떤 `platforms`에도 통과 (빈 iterable 포함)
   - `"any"`도 없고 정규화된 플랫폼 중 매칭되는 것이 없으면 `InvalidWheelFilename` 발생
   - 반환값은 기존과 동일 (`frozenset[Tag]` 거르지 않음)

2. **`src/packaging/utils.py`** import에 `_normalize_string`을 추가:
   - `from .tags import InvalidTag, Tag, UnsortedTagsError, _normalize_string, parse_tag`