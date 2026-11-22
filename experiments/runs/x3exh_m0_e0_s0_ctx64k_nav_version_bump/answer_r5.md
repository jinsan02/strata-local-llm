`src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part` 가 `"major"`/`"minor"`/`"micro"` 일 때 각각 release 의 0/1/2 번째 인덱스를 1 올리고, 이후 인덱스를 0 으로 만든다.
- 올릴 위치가 release 에 없으면 0 을 채워 해당 길이까지 확장한다.
- epoch 는 유지하고 pre/post/dev/local 은 모두 버린다.
- 유효하지 않은 `part` 값은 `ValueError` 를 던진다.
- `from_parts` 를 사용해 새 `Version` 인스턴스를 반환하므로 원래 객체는 불변이다.