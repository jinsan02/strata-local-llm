수정 완료. 무엇을 바꿨는지 요약하면:

1. **새 모듈 수준 함수 `_parse_filename_version` 추가** (라인 72-78): `Version(version_part)` 를 호출하고, `InvalidVersion` 이 발생하면 `error(f"Invalid {kind} filename (invalid version): {filename!r}")` 를 `from e` 로 던짐.

2. **`parse_wheel_filename` 수정** (라인 285-287): `try/except InvalidVersion` 블록과 `Version(parts[1])` 직접 호출을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 교체.

3. **`parse_sdist_filename` 수정** (라인 371-373): `try/except InvalidVersion` 블록과 `Version(version_part)` 직접 호출을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 교체.

`__all__` 은 변경하지 않았으며, 새 함수는 `_` 로 시작하는 private 함수임. 겉 동작 (예외 종류, 메시지, 반환값) 은 동일하게 유지됨.