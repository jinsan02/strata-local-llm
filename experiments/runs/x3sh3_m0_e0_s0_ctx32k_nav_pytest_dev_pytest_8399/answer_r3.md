수정 완료:

`src/_pytest/unittest.py` 147 라인에서 fixture 이름을 `"unittest_{setup_name}_fixture_{obj.__qualname__}"` 에서 `"_unittest_{setup_name}_fixture_{obj.__qualname__}"` 로 변경했습니다.

이제 unittest setUpClass/tearDownClass fixture 들은 이름 앞에 `_` 가 붙어서 hidden fixture 로 취급되며, `pytest --fixtures` 실행 시 `-v` 플래그 없이 숨겨집니다.