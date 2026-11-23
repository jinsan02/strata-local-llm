수정 내용 요약:

- `src/packaging/utils.py` 에 모듈 수준 헬퍼 함수 `_parse_filename_version(version_part, filename, *, error, kind) -> Version` 을 추가했다. `Version(version_part)` 를 호출하고, `InvalidVersion` 이 발생하면 `error(f"Invalid {kind} filename (invalid version): {filename!r}")` 를 `from e` 로 던진다.
- `parse_wheel_filename` 에서 `Version(parts[1])` + `except InvalidVersion` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 치환했다.
- `parse_sdist_filename` 에서 `Version(version_part)` + `except InvalidVersion` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 치환했다.
- `__all__` 은 건드리지 않았으며, 기존 테스트 79개 모두 통과했다.