수정 완료: `src/_pytest/unittest.py` 파일의 147행에서 피스처 이름 생성 패턴을 `"unittest_..."` 에서 `"_unittest_..."` 로 변경했습니다. 

이로 인해 unittest `setUpClass`, `tearDownClass`, `setup_method`, `teardown_method` 등에서 생성되는 피스처 이름이 `_`로 시작하게 되어 pytest `--fixtures` 명령어에서 기본 숨김 처리됩니다.