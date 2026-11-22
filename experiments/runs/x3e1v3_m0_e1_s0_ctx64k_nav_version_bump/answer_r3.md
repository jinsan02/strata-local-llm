`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

구현 내용:
- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나인 경우 해당 인덱스의 release 숫자를 1 올리고 뒤의 모든 숫자를 0으로 설정
- 올릴 자리가 release 튜플보다 긴 경우 0을 채워 확장 (예: `1` → micro → `1.0.1`)
- epoch는 유지하고 pre/post/dev/local은 모두 버림 (`Version.from_parts`로 새 객체 생성)
- 원래 객체는 불변이며 새 `Version` 객체를 반환
- 대소문자를 구분하므로 `"Major"`, `"MAJOR"` 등 다른 경우의 `part`는 `ValueError` 발생