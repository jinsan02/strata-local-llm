`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `"major"` → release[0] + 1, 뒤는 모두 0
- `"minor"` → release[1] + 1, 뒤는 모두 0
- `"micro"` → release[2] + 1, 뒤는 모두 0
- 목표 인덱스가 release 길이를 초과하면 0을 채워 확장
- pre/post/dev/local은 버리고 epoch만 유지
- 올바르지 않은 `part` 값은 `ValueError` 발생
- 기존 객체는 변경되지 않고 새 `Version` 반환