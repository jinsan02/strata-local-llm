`tests/test_y_canonicalize_version.py` 파일을 새로 생성하고, `canonicalize_version` 함수의 현재 동작을 고정하는 테스트 50여 개를 추가했습니다.

**주요 변경 내용:**
- `tests/test_y_canonicalize_version.py` 생성 (기존 파일 수정 없음)
- **기본 동작**: 단순 숫자, 알파/베타/RC, DEV, POST, LOCAL 세그먼트가 포함된 유효한 버전 문자열 테스트
- **`strip_trailing_zero` 옵션**: `True`(기본값)일 때 후행 0 제거, `False`일 때 원형 유지 테스트
- **잘못된 버전 문자열**: 공백, 특수문자, 빈 문자열, 파싱 불가 형식이 입력 시 원본 문자열 그대로 반환되는지 테스트
- **`Version` 객체 입력**: `Version` 인스턴스를 직접 전달해도 동일하게 처리되는지 테스트
- **세그먼트별 처리**: Epoch(`1!`), Pre-release, Post-release, Dev, Local 버전이 `strip_trailing_zero` 로직과 조합되었을 때 결과 문자열이 정확히 생성되는지 테스트
- **경계 사례**: `0.0.0`, 긴 릴리즈 세그먼트, 세그먼트 조합 순서 등

모든 테스트는 현재 저장소의 코드 동작을 기준으로 작성되었으며, 향후 `canonicalize_version` 또는 내부 `_trim_release`/`Version` 구현이 변경되면 실패하여 회귀를 즉시 알려줍니다.