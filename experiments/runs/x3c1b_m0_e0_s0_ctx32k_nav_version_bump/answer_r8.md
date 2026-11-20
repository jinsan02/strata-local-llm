수정 내용 요약:
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가함.
  - `part`가 `"major"`, `"minor"`, `"micro"` 중 하나일 때 해당 인덱스의 release 값을 1 증가시키고 뒤의 값들을 0으로 만듦.
  - release 길이가 부족한 경우 0을 채워 확장 (예: `(1,)` → micro → `(1, 0, 1)`).
  - epoch는 그대로 유지하고, pre/post/dev/local은 모두 버림.
  - 유효하지 않은 `part` 값이면 `ValueError` 발생.
  - 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환함.