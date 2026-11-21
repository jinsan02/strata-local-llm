수정 내용:
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가함.
  - `part`가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError` 발생.
  - 해당 인덱스의 release 숫자를 1 올리고, 뒤의 모든 숫자를 0으로 설정.
  - 인덱스가 현재 release 길이보다 길면 0을 채워 확장.
  - epoch는 유지하고, pre/post/dev/local은 모두 None으로 제거.
  - `__replace__`를 사용해 새 `Version` 객체 반환 (원본 불변).