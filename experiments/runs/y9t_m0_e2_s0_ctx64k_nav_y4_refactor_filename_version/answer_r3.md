수정 완료. 기존 테스트 79개 모두 통과.

바꾼 내용:
- `src/packaging/utils.py` 에 새 모듈 수준 함수 `_parse_filename_version(version_part, filename, *, error, kind) -> Version` 추가. `Version(version_part)` 를 시도하고 `InvalidVersion` 이면 `error(f"Invalid {kind} filename (invalid version): {filename!r}")` 를 `from e` 로 던짐.
- `parse_wheel_filename` 의 `try/except InvalidVersion` 블록을 `_parse_filename_version(..., error=InvalidWheelFilename, kind="wheel")` 호출로 교체.
- `parse_sdist_filename` 의 `try/except InvalidVersion` 블록을 `_parse_filename_version(..., error=InvalidSdistFilename, kind="sdist")` 호출로 교체.