`src/packaging/version.py`의 `Version` 클래스에 `bump` 메서드를 추가했습니다.
- `part`가 `"major"`, `"minor"`, `"micro"`인 경우 해당 release 인덱스를 1 증가시키고 뒤의 인덱스를 0으로 설정합니다.
- 인덱스가 현재 release 길이보다 크면 0을 채워 길이를 늘립니다.
- pre, post, dev, local 세그먼트는 모두 제거됩니다.
- epoch는 유지됩니다.
- 유효하지 않은 `part` 값은 `ValueError`를 발생시킵니다.
- 기존 객체는 변경되지 않고 새 `Version` 인스턴스를 반환합니다.