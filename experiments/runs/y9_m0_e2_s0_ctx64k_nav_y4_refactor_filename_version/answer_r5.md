수정을 마쳤다. 요약:

1. `src/packaging/utils.py` 에 새 모듈 수준 함수 `_parse_filename_version(version_part, filename, *, error, kind) -> Version` 을 추가했다. `Version(version_part)` 를 호출하고 `InvalidVersion` 이 발생하면 `error(f"Invalid {kind} filename (invalid version): {filename!r}")` 를 `from e` 로 던진다.
2. `parse_wheel_filename` 에서 `Version(parts[1])` 호출과 `except InvalidVersion` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 바꿨다.
3. `parse_sdist_filename` 에서 `Version(version_part)` 호출과 `except InvalidVersion` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 바꿨다.
4. `__all__` 은 변경하지 않았다.