`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고 뒤를 0으로 채웁니다.
- release 길이가 부족하면 0을 추가로 붙여 늘립니다.
- epoch는 그대로 유지되고, pre/post/dev/local은 모두 버립니다.
- 유효하지 않은 `part` 값에는 `ValueError`를 던집니다.
- `__replace__`를 재사용하여 새 `Version` 인스턴스를 반환합니다.