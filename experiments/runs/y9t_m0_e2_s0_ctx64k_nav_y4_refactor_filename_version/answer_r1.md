수정 내용 요약:

- `src/packaging/utils.py` 에 새 헬퍼 함수 `_parse_filename_version(version_part, filename, *, error, kind)` 를 추가했다. `Version(version_part)` 를 호출하고 `InvalidVersion` 이면 `error(f"Invalid {kind} filename (invalid version): {filename!r}")` 를 `from e` 로 던진다.
- `parse_wheel_filename` 에서 `Version(...)` 직접 호출과 `except InvalidVersion` 블록을 `_parse_filename_version(..., error=InvalidWheelFilename, kind="wheel")` 호출로 대체했다.
- `parse_sdist_filename` 에서도 동일하게 `_parse_filename_version(..., error=InvalidSdistFilename, kind="sdist")` 호출로 대체했다.
- 기존 테스트 79개 모두 통과.