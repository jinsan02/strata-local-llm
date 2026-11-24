수정 내용 요약:

1. **새 모듈 수준 함수 `_parse_filename_version` 추가** (라인 202-208): `Version(version_part)` 를 호출하고 `InvalidVersion` 이면 `error(f"Invalid {kind} filename (invalid version): {filename!r}")` 를 `__cause__` 로 던짐.

2. **`parse_wheel_filename` 수정**: `Version(parts[1])` 직접 호출과 `except InvalidVersion` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 대체.

3. **`parse_sdist_filename` 수정**: `Version(version_part)` 직접 호출과 `except InvalidVersion` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 대체.

`__all__` 은 변경하지 않았으며, 두 함수의 겉 동작(예외 종류, 메시지, 반환값)은 모두 동일하게 유지됨.