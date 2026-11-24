수정 완료. 변경 내용 요약:

- `src/packaging/utils.py` 에 새 모듈 수준 함수 `_parse_filename_version(version_part, filename, *, error, kind) -> Version` 추가. `Version(version_part)` 호출 후 `InvalidVersion` 발생 시 `error(...)` 예외를 `__cause__` 와 함께 던짐.
- `parse_wheel_filename` 에서 `Version(parts[1])` 직접 호출 + `except InvalidVersion` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 대체.
- `parse_sdist_filename` 에서 `Version(version_part)` 직접 호출 + `except InvalidVersion` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 대체.
- `__all__` 은 변경하지 않음. 두 함수의 겉 동작(예외 종류, 메시지, 반환값)은 동일하게 유지.