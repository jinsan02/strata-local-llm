수정 내용:

`src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError` 를 던진다.
- 해당 인덱스의 release 숫자를 1 올리고, 뒤의 모든 숫자를 0 으로 만든다.
- 인덱스가 현재 release 길이보다 크면 0 을 채워 늘린다.
- epoch 는 유지되고, pre/post/dev/local 은 모두 버린다.
- `__replace__` 메서드를 활용해 불변성을 지키며 새 `Version` 객체를 반환한다.