수정 완료했습니다.

**변경 내용:**
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드 추가 (line 1112-1164)
- `part`가 `"major"`, `"minor"`, `"micro"`일 때 각각 release의 0, 1, 2번 인덱스를 1 증가시키고 뒤의 모든 값을 0으로 설정
- release 길이가 부족하면 0을 채워 늘림 (예: `1` → `micro` → `1.0.1`)
- epoch는 유지하고 pre/post/dev/local은 모두 버림
- 유효하지 않은 `part` 값은 `ValueError` 발생
- 기존 객체는 불변이며 새 `Version` 인스턴스 반환