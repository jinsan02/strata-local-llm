`src/packaging/utils.py` 파일에서 다음과 같이 수정했습니다:

1. **새 헬퍼 함수 추가**: `_parse_filename_version(version_part, filename, *, error, kind) -> Version` 함수를 `parse_wheel_filename` 앞에 삽입했습니다. 이 함수는 `Version(version_part)` 를 호출하고, `InvalidVersion` 예외가 발생하면 `error(f"Invalid {kind} filename (invalid version): {filename!r}")` 를 `from e` 로 던집니다.

2. **`parse_wheel_filename` 수정**: 기존 `try/except InvalidVersion` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 대체했습니다.

3. **`parse_sdist_filename` 수정**: 기존 `try/except InvalidVersion` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 대체했습니다.

두 함수 모두 더 이상 `Version(...)` 직접 호출과 `except InvalidVersion` 블록을 포함하지 않으며, 겉 동작(예외 종류, 메시지, 반환값)은 동일하게 유지됩니다. `__all__` 도 변경하지 않았습니다.