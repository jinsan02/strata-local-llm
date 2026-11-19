수정 완료했습니다. 

변경 내용:
- `src/_pytest/unittest.py` 의 147 라인에서 fixture 이름 앞에 `_`를 추가했습니다.
- 기존: `f"unittest_{setup_name}_fixture_{obj.__qualname__}"`
- 수정: `f"_unittest_{setup_name}_fixture_{obj.__qualname__}"`

이제 `pytest --fixtures` 실행 시 unittest fixtures 가 기본적으로 숨겨지고 `-v` 플래그를 사용할 때만 표시됩니다. 이로 인해 undocumented fixture CI 스크립트 경고가 발생하지 않습니다.