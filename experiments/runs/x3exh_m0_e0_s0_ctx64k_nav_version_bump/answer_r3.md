`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

주요 동작:
- `"major"`, `"minor"`, `"micro"` 중 하나를 받아 해당 위치의 release 숫자를 1 증가시키고 뒤의 숫자를 모두 0으로 만듦
- release 길이가 부족하면 0을 채워 확장 (예: `1` → micro → `1.0.1`)
- epoch는 유지하고, pre/post/dev/local은 모두 버림
- 유효하지 않은 `part` 값은 `ValueError` 발생
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환