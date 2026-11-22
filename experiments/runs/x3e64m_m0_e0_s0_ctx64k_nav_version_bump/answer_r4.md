`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part`가 `"major"`, `"minor"`, `"micro"`인 경우 해당 인덱스의 release 숫자를 1 증가시키고 뒤의 숫자는 모두 0으로 만든다.
- release 길이가 bump 대상 인덱스보다 짧으면 0을 채워 확장한다 (예: `1` → micro → `1.0.1`).
- epoch는 그대로 유지하고 pre/post/dev/local은 모두 버린다.
- 그 외의 `part` 값은 `ValueError`를 던진다.
- `__replace__`를 사용해 새 `Version` 객체를 반환하므로 원래 객체는 불변이다.