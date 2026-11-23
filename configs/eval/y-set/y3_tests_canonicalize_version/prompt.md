`packaging.utils.canonicalize_version` 의 지금 동작을 고정하는 테스트를 새 파일 `tests/test_y_canonicalize_version.py` 에 써라.

- pytest 테스트 함수로 쓰고, **지금 코드에서 모두 통과**해야 한다. 나중에 누가 이 함수(와 이 함수가 쓰는 코드)를 잘못 고치면 실패해서 알려 주는 것이 목적이다.
- 함수의 문서와 구현(이 함수가 부르는 코드까지)을 읽고, 기본 동작 · `strip_trailing_zero` 옵션 · 잘못된 버전 문자열 · `Version` 객체 입력 · 버전의 각 부분이 결과에서 어떻게 다뤄지는지를 다뤄라.
- 소스 파일과 기존 테스트 파일은 고치지 마라. 새 테스트 파일 하나만 만든다.
