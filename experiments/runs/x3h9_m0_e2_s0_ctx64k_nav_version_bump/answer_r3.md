`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

구현 내용:
- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고, 뒤의 모든 숫자를 0으로 만듦
- release 길이가 부족하면 0을 채워 확장 (예: `1` → micro → `1.0.1`)
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 버림
- 유효하지 않은 `part` 값이면 `ValueError` 발생
- `__replace__` 메서드 다음에 삽입함.