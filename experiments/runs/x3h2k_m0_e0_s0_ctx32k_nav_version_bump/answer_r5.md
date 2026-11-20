`src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError`를 던집니다.
- 해당 인덱스의 release 숫자를 1 올리고, 뒤의 숫자들은 모두 0으로 만듭니다.
- 올릴 자리가 release 길이보다 크면 0으로 채워 길이를 늘립니다.
- epoch는 유지하고, pre/post/dev/local은 모두 제거합니다.
- `__replace__` 메서드를 활용하여 불변성(immutable)을 유지하면서 새 `Version` 객체를 반환합니다.