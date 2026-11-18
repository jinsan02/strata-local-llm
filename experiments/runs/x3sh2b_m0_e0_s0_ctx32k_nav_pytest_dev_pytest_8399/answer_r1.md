`src/_pytest/unittest.py`에서 `_make_xunit_fixture` 함수가 생성하는 fixture 이름 앞에 언더스코어(`_`)를 추가했다:

- 기존: `f"unittest_{setup_name}_fixture_{obj.__qualname__}"`
- 수정 후: `f"_unittest_{setup_name}_fixture_{obj.__qualname__}"`

이로 인해 unittest의 `setUpClass`, `tearDownClass`, `setup_method`, `teardown_method` 등에 대한 내부 pytest fixture 이름이 `_unittest_...`로 시작하게 되어, 기존 동작처럼 `pytest --fixtures` 실행 시 기본적으로 숨겨지고 `-v` 플래그를 사용해야 볼 수 있게 되었다.