수정 내용:
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.
  - `part`가 `"major"`, `"minor"`, `"micro"`인 경우 각각 release 튜플의 1, 2, 3번째 요소를 1 증가시키고 이후 요소를 0으로 만든다.
  - release 길이가 부족하면 0을 채워 늘린다.
  - epoch는 유지하고, pre/post/dev/local은 모두 버린다.
  - 유효하지 않은 `part` 값에는 `ValueError`를 던진다.
  - `Version.from_parts`를 사용해 새 `Version` 객체를 반환하므로 원래 객체는 변경되지 않는다.