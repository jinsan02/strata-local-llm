수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part`가 `"major"`, `"minor"`, `"micro"`인 경우 각각 release의 첫 번째, 두 번째, 세 번째 숫자를 1 올리고 뒤의 숫자는 0으로 설정
- release 길이가 부족하면 0을 채워 확장 (예: `1` → micro → `1.0.1`)
- epoch는 유지, pre/post/dev/local은 모두 버림
- 유효하지 않은 `part` 값은 `ValueError` 던짐
- 원래 객체는 변경되지 않고 새 `Version` 반환