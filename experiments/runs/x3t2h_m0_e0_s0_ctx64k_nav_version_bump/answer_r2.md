수정 완료. `src/packaging/version.py` 파일의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

**주요 동작:**
- `part`가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고 뒤의 숫자를 모두 0으로 설정한다.
- release 길이가 부족하면 0을 채워 늘린다 (예: `1` → micro → `1.0.1`).
- pre/post/dev/local은 버리고 epoch는 유지한다.
- 유효하지 않은 `part` 값은 `ValueError`를 던진다.
- 기존 객체는 변경되지 않고 새 `Version`을 반환한다.