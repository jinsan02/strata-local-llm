수정 내용:
- `src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.
  - `"major"`, `"minor"`, `"micro"` 중 하나를 받아 해당 인덱스의 release 숫자를 1 올리고, 뒤의 모든 숫자는 0으로 설정한다.
  - release 길이가 부족하면 0을 채워 필요한 길이까지 늘린다.
  - epoch는 그대로 유지하고, pre/post/dev/local은 모두 버린다.
  - 유효하지 않은 `part` 값이면 `ValueError`를 던진다.