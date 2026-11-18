<<<<<<< SEARCH
          # Use a unique name to speed up lookup.
          name=f"unittest_{setup_name}_fixture_{obj.__qualname__}",
=======
          # Use a unique name to speed up lookup.
          name=f"_unittest_{setup_name}_fixture_{obj.__qualname__}",
>>>>>>> REPLACE

`src/_pytest/unittest.py`의 `_make_xunit_fixture` 함수에서 동적으로 생성하는 fixture 이름 앞에 언더스코어(`_`)를 추가했습니다. pytest는 `--fixtures` 출력 시 이름이 `_`로 시작하는 fixture를 숨기므로, unittest 기반 setUpClass/setup_method fixture가 더 이상 일반 사용자에게 노출되지 않도록 기존 동작을 복구했습니다.