수정 내용:
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.
  - `part`가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError`를 던진다.
  - 해당 인덱스의 release 숫자를 1 올리고, 그 뒤의 모든 숫자를 0으로 만든다.
  - 올릴 자리가 release 길이보다 크면 0을 채워 늘린다 (예: `1` → micro → `1.0.1`).
  - epoch는 그대로 유지하고, pre/post/dev/local은 모두 버린다.
  - `__replace__`를 사용해 새 `Version` 객체를 반환하며 원래 객체는 변경되지 않는다.