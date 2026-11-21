수정을 완료했습니다. 무엇을 바꿨는지 요약하면:

1. **`collections.abc.Iterable` import 추가**: `platforms` 인자의 타입 힌트에 사용.
2. **`_normalize_platform` 헬퍼 함수 추가**: 플랫폼 이름을 정규화하는 함수 (`.`/`-`/공백 → `_`, 소문자).
3. **`parse_wheel_filename` 함수 수정**:
   - 키워드 전용 인자 `platforms: Iterable[str] | None = None` 추가.
   - `platforms`가 `str`이면 `TypeError` 던짐.
   - `platforms`가 제공되면, 각 태그의 플랫폼을 정규화하여 주어진 플랫폼 목록과 비교. 하나라도 매칭되거나 `platform == "any"`이면 통과, 아니면 `InvalidWheelFilename` 던짐.
   - 기존 동작(`platforms=None`)은 변경 없음.
   - docstring에 `platforms` 파라미터 설명 및 `.. versionadded:: 26.4` 추가.