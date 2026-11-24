수정 내용을 요약하면:

1. **새 함수 `_parse_filename_version` 추가** (202~212줄): `Version(version_part)` 를 호출하고, `InvalidVersion` 이면 `error(...)` 예외를 `from e` 로 던지는 공통 로직.

2. **`parse_wheel_filename` 수정**: `try: Version(parts[1]) except InvalidVersion` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 대체.

3. **`parse_sdist_filename` 수정**: `try: Version(version_part) except InvalidVersion` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 대체.

두 함수 모두 `Version(...)` 직접 호출과 `except InvalidVersion` 이 완전히 제거되었으며, 예외 종류·메시지·`__cause__` 체이닝 등 겉 동작은 동일하게 유지됨. `__all__` 도 변경 없음.