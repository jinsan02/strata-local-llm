`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part`가 `"major"`/`"minor"`/`"micro"`일 때 해당 release 인덱스(0/1/2)의 숫자를 1 증가시키고, 뒤의 모든 release 숫자를 0으로 설정한다.
- release 길이가 부족하면 0을 채워 해당 자리까지 늘린다.
- epoch는 유지되고, pre/post/dev/local은 모두 `None`으로 초기화된다.
- 유효하지 않은 `part`는 `ValueError`를 던진다.
- `__replace__`를 재사용하여 불변성을 보장한다.