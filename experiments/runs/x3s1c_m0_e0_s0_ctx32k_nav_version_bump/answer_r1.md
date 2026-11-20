수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고 뒤의 숫자는 모두 0으로 설정한다.
- release 길이가 부족하면 0을 채워 늘린다 (예: `1` → `bump("micro")` → `1.0.1`).
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 버린다.
- 유효하지 않은 `part` 값이면 `ValueError`를 던진다.
- `__replace__`를 사용해 새 `Version` 객체를 반환하므로 원래 객체는 불변이다.