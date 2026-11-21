수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나일 때 해당 인덱스의 release 요소를 1 증가시키고 이후 요소를 모두 0으로 설정한다.
- release 길이가 부족하면 0을 채워 해당 인덱스까지 늘린다.
- epoch는 `__replace__`에서 기본값으로 유지되고, pre/post/dev/local은 명시적으로 `None`으로 클리어한다.
- 그 밖의 `part` 값은 `ValueError`를 던진다.
- 원래 객체는 불변이며 새 `Version` 인스턴스를 반환한다.