과제 완료.

수정 내용 요약:
- `src/packaging/utils.py` 에 `_parse_filename_version(version_part, filename, *, error, kind)` 모듈 수준 함수를 새로 추가 (`Version` 호출 + `InvalidVersion` → `error` 예외 변환)
- `parse_wheel_filename` 의 `Version(parts[1])`/`except InvalidVersion` 블록을 `_parse_filename_version(..., error=InvalidWheelFilename, kind="wheel")` 호출로 대체
- `parse_sdist_filename` 의 `Version(version_part)`/`except InvalidVersion` 블록을 `_parse_filename_version(..., error=InvalidSdistFilename, kind="sdist")` 호출로 대체
- `__all__` 은 변경하지 않음
- 기존 테스트 79개 모두 통과