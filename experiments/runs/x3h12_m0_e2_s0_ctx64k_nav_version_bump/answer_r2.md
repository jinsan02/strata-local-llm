수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

**변경 내용:**
- `Version` 클래스에 `bump` 메서드 추가 (1112–1168 라인)
  - `part`가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고 뒤의 모든 숫자를 0으로 설정
  - release 길이가 부족하면 0을 채워 확장 (예: `1` → micro → `1.0.1`)
  - epoch는 유지, pre/post/dev/local은 모두 버림
  - 유효하지 않은 `part` 값이면 `ValueError` 던짐
  - `__replace__`를 사용해 새 `Version` 객체 반환 (원본 불변)