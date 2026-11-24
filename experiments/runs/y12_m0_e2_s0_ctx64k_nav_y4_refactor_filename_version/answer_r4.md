수정 완료. 변경 사항을 요약하면:

1. **새 모듈 수준 함수 `_parse_filename_version` 추가** (라인 84~94): `version_part`를 `Version()`으로 파싱하고, `InvalidVersion` 예외가 발생하면 `error` 클래스로 `kind`를 포함한 메시지를 던지며 원래 예외를 `__cause__`로 남긴다.

2. **`parse_wheel_filename` 수정** (라인 289~291): 기존 `try/except InvalidVersion` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 대체.

3. **`parse_sdist_filename` 수정** (라인 375~377): 기존 `try/except InvalidVersion` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 대체.

두 함수 모두 더 이상 `Version(...)` 직접 호출이나 `except InvalidVersion` 블록을 포함하지 않으며, 예외 종류, 메시지, 반환값 등 겉 동작은 변경되지 않았다. `__all__`도 수정하지 않았다.