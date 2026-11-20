`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

**주요 동작:**
- `part`가 `"major"`·`"minor"`·`"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고, 뒤의 숫자를 모두 0으로 만듦
- 올릴 자리가 release 길이보다 크면 0을 채워 확장 (예: `1` → micro → `1.0.1`)
- epoch는 그대로 유지, pre/post/dev/local은 모두 버림
- 유효하지 않은 `part` 값은 `ValueError` 발생
- 원래 객체는 불변이고 새 `Version` 객체 반환