`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `major` / `minor` / `micro`에 따라 release 튜플의 첫 번째 / 두 번째 / 세 번째 요소를 1 올리고, 그 뒤의 요소를 모두 0으로 만듭니다.
- 올릴 자리가 release 길이보다 크면 0을 채워 그 자리까지 늘립니다.
- epoch는 유지하고, pre/post/dev/local은 모두 버립니다.
- 유효하지 않은 `part` 값은 `ValueError`를 던집니다.
- `__replace__`를 재사용하여 새 `Version` 객체를 반환하므로 원래 객체는 불변입니다.