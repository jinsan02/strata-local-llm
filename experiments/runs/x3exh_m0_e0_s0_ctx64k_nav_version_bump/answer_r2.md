`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part`가 `"major"`, `"minor"`, `"micro"`일 때 각각 release 튜플의 첫 번째, 두 번째, 세 번째 요소를 1 증가시키고 그 뒤의 요소를 0으로 만듭니다.
- release 길이가 부족하면 0을 채워 필요한 길이까지 확장합니다.
- epoch는 유지하고 pre/post/dev/local은 모두 버립니다.
- 그 외의 `part` 값은 `ValueError`를 던집니다.
- `__replace__`를 사용해 불변성을 유지하며 새 `Version` 객체를 반환합니다.