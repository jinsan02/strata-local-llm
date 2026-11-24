수정 사항을 요약하면 다음과 같다:

1. **새 모듈 수준 함수 `_parse_filename_version` 추가** (라인 129-135): `version_part`를 `Version()`으로 파싱하고, `InvalidVersion` 예외가 발생하면 `error` 클래스로 `kind`를 포함하는 메시지를 붙여 `from e`로 원래 예외를 `__cause__`에 남기며 던진다.

2. **`parse_wheel_filename` 수정** (라인 285): 기존 `try: version = Version(parts[1]) except InvalidVersion ...` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 대체.

3. **`parse_sdist_filename` 수정** (라인 369): 기존 `try: version = Version(version_part) except InvalidVersion ...` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 대체.

두 함수 모두 `Version(...)` 직접 호출과 `except InvalidVersion` 블록이 완전히 제거되었으며, 예외 종류·메시지·반환값은 기존과 동일하게 유지된다. `__all__` 은 변경하지 않았다.