`src/_pytest/unittest.py` 파일의 147 줄에서 fixture 이름을 `unittest_...`에서 `_unittest_...`로 변경했습니다.

이 수정으로 인해 pytest 가 생성하는 setUpClass/tearDownClass fixture 이름이 밑줄(`_`)로 시작하게 되어, 기본 `pytest --fixtures` 출력에서 숨겨집니다. `-v` 플래그를 사용하면 여전히 확인할 수 있습니다.