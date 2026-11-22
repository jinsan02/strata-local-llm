`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `major`, `minor`, `micro` 세 가지 `part`를 지원하며, 각각 release 튜플의 첫 번째·둘째·셋째 요소를 1 증가시키고 그 뒤의 모든 요소를 0으로 만듭니다.
- 요청한 자리가 현재 release 길이보다 길면 0을 채워 늘립니다 (예: `1` → micro → `1.0.1`).
- epoch는 유지되고, pre/post/dev/local은 모두 버립니다 (`__replace__`로 처리).
- 유효하지 않은 `part` 값은 `ValueError`를 던집니다.
- 원래 객체는 불변이며 새 `Version` 인스턴스를 반환합니다.