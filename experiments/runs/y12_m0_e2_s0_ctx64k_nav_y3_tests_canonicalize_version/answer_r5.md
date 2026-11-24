새 파일 `tests/test_y_canonicalize_version.py`를 생성했습니다. 현재 `canonicalize_version` 함수의 동작을 고정하는 포괄적인 테스트를 포함하며, 주요 커버리지 영역은 다음과 같습니다:
- 기본 릴리즈 버전 (trailing zero 자동 제거)
- `strip_trailing_zero=False` 옵션 동작
- 유효하지 않은 버전 문자열 입력 시 원본 반환
- `Version` 객체 직접 입력
- Epoch, Pre-release, Post-release, Dev, Local 세그먼트별 처리
- 여러 세그먼트가 결합된 복잡한 버전
- `Version.from_parts()` 생성 객체 및 경계값/예외 처리 (`None`, `int`, `float`, `list` 등 `InvalidVersion` 발생)
모든 테스트는 현재 저장소의 구현을 기준으로 작성되어, 향후 코드 변경 시 회귀를 감지합니다. 기존 테스트 파일은 수정하지 않았습니다.