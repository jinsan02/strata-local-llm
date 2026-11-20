`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part`가 `"major"`·`"minor"`·`"micro"` 중 하나가 아니면 `ValueError`를 던짐
- 해당 인덱스의 release 숫자를 1 올리고, 뒤의 모든 숫자를 0으로 만듦
- release 길이가 부족하면 0을 채워 늘림 (예: `1` → micro → `1.0.1`)
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 버림
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환함

기존 테스트 51524개 모두 통과했습니다.