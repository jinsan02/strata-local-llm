`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part` 가 `"major"`·`"minor"`·`"micro"` 중 하나일 때 해당 인덱스의 release 숫자를 1 올리고 뒤의 숫자를 모두 0 으로 만듦
- release 길이가 부족하면 0 을 채워 확장 (예: `1` → `bump("micro")` → `1.0.1`)
- epoch 는 유지하고, pre/post/dev/local 은 모두 버림
- 유효하지 않은 `part` 값은 `ValueError` 던짐
- 원래 객체는 불변이며 새 `Version` 인스턴스 반환