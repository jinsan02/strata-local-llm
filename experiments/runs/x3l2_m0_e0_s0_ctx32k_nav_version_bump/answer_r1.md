수정 완료. `src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고 뒤의 숫자는 0 으로 채운다.
- 올릴 자리가 release 길이보다 크면 0 을 채워 확장한다.
- epoch 는 유지하고, pre/post/dev/local 은 모두 `None` 으로 버린다.
- 그 밖의 `part` 값은 `ValueError` 를 던진다.
- 원래 객체는 불변이고 새 `Version` 인스턴스를 반환한다.