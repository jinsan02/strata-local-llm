수정 내용을 요약하면:

**파일:** `src/packaging/version.py`

**변경 사항:** `Version` 클래스에 `bump(part: str) -> Version` 메서드 추가 (약 50줄).

**동작:**
- `"major"`, `"minor"`, `"micro"` 중 하나를 받아 해당 인덱스의 release 숫자를 1 올리고, 뒤의 모든 숫자를 0으로 함.
- 올릴 자리가 release 길이를 넘어가면 0을 채워 확장 (예: `1` → micro → `1.0.1`).
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 버림 (예: `2!1.2.3rc1.post2.dev3+abc` → micro → `2!1.2.4`).
- 유효하지 않은 part 값은 `ValueError` 발생.
- 기존 객체는 불변이며 새 `Version` 인스턴스를 반환.