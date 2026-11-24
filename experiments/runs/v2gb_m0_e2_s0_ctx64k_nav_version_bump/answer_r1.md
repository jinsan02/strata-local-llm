수정 내용:
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.
  - `part`가 `"major"`, `"minor"`, `"micro"`인 경우 각각 release 튜플의 첫 번째, 두 번째, 세 번째 요소를 1 증가시키고, 그 뒤의 모든 요소를 0으로 설정한다.
  - 요청한 자리가 현재 release 길이보다 긴 경우 0을 채워 늘린다.
  - epoch는 그대로 유지하고, pre/post/dev/local은 모두 버린다.
  - 유효하지 않은 `part` 값은 `ValueError`를 던진다.
  - 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환한다.