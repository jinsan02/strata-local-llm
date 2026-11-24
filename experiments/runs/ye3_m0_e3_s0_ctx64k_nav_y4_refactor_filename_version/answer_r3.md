수정 완료. 변경 내용 요약:

1. **새 함수 `_parse_filename_version` 추가** (라인 202-212): `Version(version_part)` 를 호출하고 `InvalidVersion` 발생 시 지정된 예외 클래스로 메시지를 바꿔 던지는 공통 유틸 함수.

2. **`parse_wheel_filename` 수정** (라인 289): 기존 `try: Version(parts[1]) except InvalidVersion` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 대체.

3. **`parse_sdist_filename` 수정** (라인 373): 기존 `try: Version(version_part) except InvalidVersion` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 대체.

두 함수 모두에서 `Version(...)` 직접 호출과 `except InvalidVersion` 이 완전히 제거되었고, 예외 종류·메시지·반환값은 동일하게 유지된다. `__all__` 은 변경하지 않았다.