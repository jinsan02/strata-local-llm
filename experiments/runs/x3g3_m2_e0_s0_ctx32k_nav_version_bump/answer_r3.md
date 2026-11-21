`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `major`/`minor`/`micro` 중 하나를 받아 release의 해당 인덱스 숫자를 1 올리고, 뒤의 숫자는 모두 0으로 만든다.
- release 길이가 해당 인덱스보다 짧으면 0을 채워 확장한다.
- epoch는 유지하고 pre/post/dev/local은 모두 버린다.
- 유효하지 않은 `part` 값은 `ValueError`를 던진다.
- `__replace__`를 사용해 불변성을 유지하며 새 `Version` 객체를 반환한다.