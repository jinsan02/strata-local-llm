수정 사항:
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가함.
  - `"major"`, `"minor"`, `"micro"` 중 하나를 받으며, 해당 인덱스의 release 숫자를 1 올리고 뒤의 모든 숫자는 0으로 만듦.
  - 올릴 자리가 현재 release 길이보다 크면 0을 채워 늘림. (예: `Version("1").bump("micro")` → `Version("1.0.1")`, `Version("1.2.3.4").bump("minor")` → `Version("1.3.0.0")`)
  - epoch는 그대로 유지하고, pre/post/dev/local은 모두 None으로 버림.
  - invalid part는 `ValueError` 발생.
  - 원래 객체는 불변이며 새 `Version` 인스턴스를 반환함.