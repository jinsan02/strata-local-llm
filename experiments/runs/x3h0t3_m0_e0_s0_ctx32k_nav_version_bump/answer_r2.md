`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part`가 `"major"`·`"minor"`·`"micro"`인 경우 각각 release의 첫번째·둘째·셋째 숫자를 1 올리고 뒤를 0으로 만듦
- 올릴 자리가 없으면 release 길이를 자동으로 확장 (예: `1` → micro → `1.0.1`)
- epoch는 그대로 두고 pre/post/dev/local은 모두 버림
- 그 밖의 part 값은 `ValueError` 던짐
- 원래 객체는 불변이고 새 `Version` 반환