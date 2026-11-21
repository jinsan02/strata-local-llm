`src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 일 때 각각 release 의 첫째, 둘째, 셋째 숫자를 1 올리고 뒤를 0 으로 채운다.
- 올릴 자리가 없으면 0 을 채워 그 자리까지 release 길이를 늘린다.
- epoch 는 유지하고, pre/post/dev/local 은 모두 버린다.
- 유효하지 않은 `part` 값은 `ValueError` 를 던진다.
- `__replace__` 를 사용해 새 `Version` 객체를 반환하므로 원래 객체는 불변이다.