`src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Self` 메서드를 추가했습니다.

변경 내용 요약:
- `Version.bump` 메서드 추가: `part` ("major", "minor", "micro")에 따라 release 튜플의 해당 인덱스를 1 증가시키고, 뒤쪽 요소를 0으로 채웁니다.
- pre/post/dev/local 세그먼트는 삭제되고 epoch는 유지됩니다.
- 유효하지 않은 `part` 입력 시 `ValueError`를 던집니다.
- 기존 동작은 영향받지 않습니다.