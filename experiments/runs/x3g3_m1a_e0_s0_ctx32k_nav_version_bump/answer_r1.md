`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고, 뒤의 숫자는 모두 0으로 한다.
- 인덱스가 현재 release 길이보다 크면 0을 채워 늘린다.
- pre, post, dev, local은 모두 버리고 epoch는 유지한다.
- 유효하지 않은 `part` 값이면 `ValueError`를 던진다.
- `__replace__`를 사용해 새 `Version` 객체를 반환하므로 원래 객체는 변하지 않는다.