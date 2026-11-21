수정 내용:
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.
  - `part`가 `"major"`, `"minor"`, `"micro"` 중 하나이면 해당 인덱스의 release 숫자를 1 올리고, 그 뒤의 숫자는 모두 0으로 설정한다.
  - 올릴 자리가 release 길이보다 크면 0을 채워 해당 길이까지 늘린다.
  - epoch는 그대로 유지하고, pre/post/dev/local은 모두 버린다.
  - 유효하지 않은 `part` 값이면 `ValueError`를 던진다.
  - 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환한다.