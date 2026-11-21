The implementation is complete. Here's a summary of what was changed:

**수정 파일:** `src/packaging/utils.py`

1. **import 추가**: `from collections.abc import Iterable` 추가
2. **`parse_wheel_filename` 시그니처 변경**: `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
3. **플랫폼 검증 로직 추가**:
   - `platforms`가 `str`이면 `TypeError` 발생
   - 각 플랫폼 이름을 `_normalize_string(p).lower()`로 정규화 (`.`, `-`, ` ` → `_`, 소문자)
   - 태그 중 `platform == "any"`인 것이 있거나 정규화된 태그 플랫폼이 입력과 일치하면 통과
   - 일치하는 것이 없으면 `InvalidWheelFilename` 발생
4. **docstring 업데이트**: `platforms` 파라미터 설명, `:raises TypeError:`, `.. versionadded:: 26.4` 섹션 추가