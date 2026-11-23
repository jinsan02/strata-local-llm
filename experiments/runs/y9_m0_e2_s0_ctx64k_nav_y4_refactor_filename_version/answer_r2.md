수정 사항을 요약하면 다음과 같습니다:

1. **새 헬퍼 함수 `_parse_filename_version` 추가** (라인 202–217):
   - `Version(version_part)` 를 호출하여 `Version` 객체를 반환합니다.
   - `InvalidVersion` 예외가 발생하면 지정된 `error` 클래스로 `f"Invalid {kind} filename (invalid version): {filename!r}"` 메시지를 던지고, 원래 예외를 `__cause__` 로 남깁니다 (`raise ... from e`).

2. **`parse_wheel_filename` 수정**:
   - 기존 `try: Version(parts[1]) except InvalidVersion: ...` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 대체했습니다.

3. **`parse_sdist_filename` 수정**:
   - 기존 `try: Version(version_part) except InvalidVersion: ...` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 대체했습니다.

두 함수의 겉 동작(예외 종류, 메시지, 반환값)은 완전히 동일하게 유지됩니다. `__all__` 도 변경하지 않았습니다.