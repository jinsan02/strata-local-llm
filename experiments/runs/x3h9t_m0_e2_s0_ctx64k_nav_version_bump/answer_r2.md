`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part`가 `"major"`·`"minor"`·`"micro"`인 경우 각각 release의 0·1·2 번째 인덱스를 1 올리고, 그 뒤의 모든 인덱스를 0으로 설정한다.
- 올릴 위치가 현재 release 길이보다 크면 0을 채워 release를 확장한다 (예: `1` → micro → `1.0.1`).
- epoch는 유지하고, pre/post/dev/local은 모두 버린다.
- 유효하지 않은 `part` 값은 `ValueError`를 던진다.
- `__replace__`를 사용해 새 `Version`을 반환하므로 원래 객체는 불변이다.