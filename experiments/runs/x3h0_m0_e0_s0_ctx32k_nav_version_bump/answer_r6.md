수정 완료했습니다. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

**변경 내용:**
- `Version.bump()` 메서드 추가 (`micro` property 다음, `_trim_release` 앞에 삽입)
- `"major"`, `"minor"`, `"micro"` 외의 part 값은 `ValueError` 발생
- 요청한 위치의 release 숫자를 1 증가시키고, 뒤의 모든 숫자를 0으로 설정
- release 길이가 부족하면 자동으로 0을 채워 확장 (예: `1` → micro → `1.0.1`)
- epoch는 유지하고 pre/post/dev/local은 모두 버림
- `__replace__()`를 사용하여 새 Version 객체 반환 (원본 불변)