`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나일 때 각각 release 의 첫번째, 두번째, 세번째 숫자를 1 올리고 뒤의 숫자를 0 으로 채운다.
- 해당 자리가 release 길이보다 크면 0 으로 패딩하여 길이를 유지/확장한다.
- epoch 는 그대로 두고, pre/post/dev/local 은 모두 None 으로 클리어한다.
- 그 밖의 `part` 값은 `ValueError` 를 던진다.
- `__replace__` 를 활용하여 원래 객체는 변경하지 않고 새 `Version` 을 반환한다.