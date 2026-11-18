수정 완료:

`src/_pytest/unittest.py` 파일의 `_make_xunit_fixture` 함수에서 생성하는 fixture 이름을 `"unittest_{setup_name}_fixture_{obj.__qualname__}"` 에서 `"_pytest_unittest_{setup_name}_fixture_{obj.__qualname__}"` 로 변경했습니다.

이전에는 fixture 이름이 언더스코어(_)로 시작하지 않아 pytest 가 이를 public fixture 로 인식했지만, 이제 `_pytest_unittest_` 접두사를 추가함으로써 private fixture 로 처리되어 `pytest --fixtures` 실행 시 기본적으로 표시되지 않습니다.