`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고 뒤의 숫자를 모두 0 으로 만듭니다.
- 올릴 자리가 release 길이보다 크면 0 을 채워 해당 길이까지 늘립니다.
- epoch 는 유지하고, pre/post/dev/local 은 모두 버립니다.
- 그 밖의 `part` 값은 `ValueError` 를 던집니다.
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환합니다.