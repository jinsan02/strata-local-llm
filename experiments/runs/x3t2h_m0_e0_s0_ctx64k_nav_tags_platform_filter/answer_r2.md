수정 내용을 요약하면:

1. **`src/packaging/utils.py`** — `parse_wheel_filename` 함수에 `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
   - `typing.Iterable` import 추가
   - `tags._normalize_string` import 추가 (`.`, `-`, ` ` → `_`, 소문자)
   - `platforms is not None`일 때:
     - `str`을 직접 주면 `TypeError` 던짐
     - iterable의 각 요소를 `_normalize_string`으로 정규화
     - 태그의 플랫폼 중 `any`가 있거나 정규화된 플랫폼과 일치하면 통과
     - 일치하는 플랫폼이 없으면 `InvalidWheelFilename` 던짐
   - `platforms=None`이면 기존 동작과 동일하게 검증 없이 반환
   - docstring에 새 파라미터 설명과 `versionadded:: 26.4` 주석 추가