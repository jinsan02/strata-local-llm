`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나인 경우 해당 인덱스의 release 숫자를 1 올리고 뒤의 숫자들을 0으로 설정한다.
- release 길이가 부족하면 0을 채워 확장한다 (예: `1` → `bump("micro")` → `1.0.1`).
- epoch는 유지되고, pre/post/dev/local은 모두 버린다.
- 그 밖의 `part` 값은 `ValueError`를 던진다.
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환한다.