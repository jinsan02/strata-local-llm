새 파일 `tests/test_y_canonicalize_version.py`를 생성했습니다.

- 기본 동작(`strip_trailing_zero=True`), `strip_trailing_zero=False` 옵션, 유효하지 않은 버전 문자열, `Version` 객체 입력을 모두 테스트합니다.
- 에포크(epoch), 프리릴리스(pre), 포스트릴리스(post), 디브릴리스(dev), 로컬 버전(local) 및 이들이 복합된 경우의 canonicalization 결과를 검증합니다.
- `Version.from_parts()`로 생성된 객체와 기존 `Version("...")` 객체 모두에 대해 테스트하며, 함수가 입력 객체를 불변으로 유지하는지도 확인합니다.
현재 코드에서 모든 테스트가 통과하며, 구현이 변경되면 실패하여 문제를 알려주는 역할입니다. 기존 테스트 파일은 수정하지 않았습니다.