수정 완료. 변경 사항 요약:

1. **새 함수 `_parse_filename_version` 추가** (라인 202-212): `Version(version_part)` 호출과 `InvalidVersion` 예외를 `error(...)`로 변환하는 공통 로직.
2. **`parse_wheel_filename` 수정**: `Version(parts[1])` 직접 호출과 `except InvalidVersion` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 대체.
3. **`parse_sdist_filename` 수정**: `Version(version_part)` 직접 호출과 `except InvalidVersion` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 대체.

`__all__`과 테스트 파일은 변경하지 않았으며, 두 함수의 외부 동작(예외 종류, 메시지, 반환값)은 동일하게 유지됨.