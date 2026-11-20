수정 내용:

- **파일**: `src/packaging/version.py`
- **변경 사항**: `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가함.
  - `part`는 `"major"`, `"minor"`, `"micro"`만 허용하며, 그 외 값은 `ValueError`를 던짐.
  - 해당 인덱스의 release 숫자를 1 올리고, 뒤의 모든 release 숫자는 0으로 만듦.
  - release 길이가 부족하면 0을 추가하여 늘림 (예: `"1"` → micro → `"1.0.1"`).
  - pre, post, dev, local 부분은 모두 버림(`None`).
  - epoch는 그대로 유지.
  - 기존 객체는 불변이며, 새 `Version` 인스턴스를 반환함 (`__replace__` 사용).