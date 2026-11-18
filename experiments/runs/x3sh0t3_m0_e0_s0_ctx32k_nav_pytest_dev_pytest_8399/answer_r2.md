수정 내용을 요약하면:

- **파일**: `src/_pytest/unittest.py`
- **변경**: `_make_xunit_fixture` 함수에서 생성되는 fixture 이름의 접두사를 `"unittest_"`에서 `"_pytest_"`로 변경
- **이유**: pytest는 underscore(`_`)로 시작하는 fixture 이름을 "private"로 간주하여 기본 `--fixtures` 출력에서 숨깁니다. 기존 `"unittest_setUpClass_fixture_Tests"`는 public으로 표시되어 모든 사용자에게 보였으나, `"_pytest_setUpClass_fixture_Tests"`로 변경되어 이제 기본적으로 숨겨집니다 ( `-v` 옵션 필요).