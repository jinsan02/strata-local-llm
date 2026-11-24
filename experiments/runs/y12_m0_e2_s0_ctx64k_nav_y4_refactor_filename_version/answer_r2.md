수정 사항을 요약하면 다음과 같다:

1. **새 함수 `_parse_filename_version` 추가** (라인 305~311): `version_part` 를 `Version()` 으로 파싱하고, `InvalidVersion` 이 발생하면 `error` 로 지정된 예외 클래스로 `kind` 이름을 담은 메시지와 함께 `from e` 로 원래 예외를 `__cause__` 로 남기며 던진다.

2. **`parse_wheel_filename` 수정** (라인 276~278): 기존 `try: version = Version(parts[1]) except InvalidVersion` 블록을 `_parse_filename_version(parts[1], filename, error=InvalidWheelFilename, kind="wheel")` 호출로 교체.

3. **`parse_sdist_filename` 수정** (라인 371~373): 기존 `try: version = Version(version_part) except InvalidVersion` 블록을 `_parse_filename_version(version_part, filename, error=InvalidSdistFilename, kind="sdist")` 호출로 교체.

두 함수 모두 더 이상 `Version(...)` 직접 호출이나 `except InvalidVersion` 을 포함하지 않으며, 예외 종류·메시지·반환값은 동일하게 유지된다. `__all__` 도 변경하지 않았다.