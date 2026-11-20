`src/packaging/utils.py` 파일에서 `parse_wheel_filename` 함수를 다음과 같이 수정했습니다:

1. **시그니처**: `platforms: Iterable[str] | None = None` 키워드 전용 인자 추가
2. **문서화**: docstring에 `platforms` 파라미터 설명과 `.. versionadded:: 26.3` 주석 추가
3. **로직**: 기존 검사(`extension`, `dashes`, `name`, `version`, `build`, `tag`) 통과 후 `platforms is not None`이면:
   - `isinstance(platforms, str)` → `TypeError` 발생
   - 입력 iterable의 각 문자열을 `.replace(".", "_").replace("-", "_").replace(" ", "_").lower()`로 정규화하여 `frozenset`으로 전환
   - 태그 중 `platform == "any"`가 하나라도 있으면 즉시 통과 (빈 iterable 포함)
   - 그렇지 않으면 태그 플랫폼 집합과 교집합 확인 → 교집합이 비면 `InvalidWheelFilename` 발생

기존 반환값은 변경하지 않았으며, `validate_order` 파라미터와 함께 정상적으로 동작합니다.