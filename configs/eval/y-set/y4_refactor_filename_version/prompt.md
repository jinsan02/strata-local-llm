`src/packaging/utils.py` 의 `parse_wheel_filename` 과 `parse_sdist_filename` 에는 '파일 이름의 버전 부분을 `Version` 으로 파싱하고, 실패하면 그 파일 형식의 예외로 바꿔 던지는' 같은 로직이 따로 들어 있다. 동작을 바꾸지 말고 이 중복을 함수 하나로 뽑아라.

- 새 모듈 수준 함수: `_parse_filename_version(version_part: str, filename: str, *, error: type[ValueError], kind: str) -> Version`
  - `Version(version_part)` 를 돌려준다.
  - `InvalidVersion` 이 나면 `error(f"Invalid {kind} filename (invalid version): {filename!r}")` 를 던지고, 원래 예외를 `__cause__` 로 남긴다(`raise ... from e`).
- `parse_wheel_filename` 은 `error=InvalidWheelFilename, kind="wheel"`, `parse_sdist_filename` 은 `error=InvalidSdistFilename, kind="sdist"` 로 이 함수를 불러 버전을 얻는다. 두 함수 안에는 `Version(...)` 직접 호출과 `except InvalidVersion` 이 남지 않아야 한다.
- 예외 종류 · 메시지 · 반환값 등 두 함수의 겉 동작은 하나도 바뀌면 안 된다. `__all__` 은 바꾸지 마라.
- 테스트 파일은 고치지 마라.
