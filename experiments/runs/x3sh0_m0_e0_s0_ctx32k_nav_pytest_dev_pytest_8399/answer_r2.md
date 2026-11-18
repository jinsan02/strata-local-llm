수정 내용:

`src/_pytest/unittest.py`의 `_make_xunit_fixture` 함수에서 생성되는 fixture 이름 앞에 `_`를 추가했습니다. 

- 기존: `f"unittest_{setup_name}_fixture_{obj.__qualname__}"`
- 변경: `f"_unittest_{setup_name}_fixture_{obj.__qualname__}"`

이로 인해 fixture 이름이 `_`로 시작하게 되어, `pytest --fixtures` 실행 시 verbose <= 0일 경우 숨겨지게 됩니다 (`src/_pytest/python.py`의 1429번 줄에서 `argname.startswith("_")` 조건으로 처리됨).