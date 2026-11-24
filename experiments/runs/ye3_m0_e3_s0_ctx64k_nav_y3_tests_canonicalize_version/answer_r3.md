`tests/test_y_canonicalize_version.py` 파일을 새로 생성했습니다.

- `canonicalize_version`의 기본 동작(유효 버전 파싱 및 정규화) 테스트
- `strip_trailing_zero=False` 옵션 동작 테스트
- 유효하지 않은 버전 문자열은 원본 그대로 반환하는 동작 테스트
- `Version` 객체 직접 입력 시 동작 테스트
- Epoch, Pre-release, Post-release, Dev release, Local version 세그먼트가 결과에서 어떻게 유지/처리되는지 테스트
- 경계 조건(단일 숫자, 대용량 버전, 객체/문자열 동치성 등) 테스트

기존 소스 및 테스트 파일은 수정하지 않았습니다. 모든 테스트는 현재 코드베이스의 동작을 정확히 반영하도록 작성되었습니다.