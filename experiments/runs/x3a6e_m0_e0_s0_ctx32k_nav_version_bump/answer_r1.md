`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다. 

- `part`가 `"major"`, `"minor"`, `"micro"`일 때 각각 release 인덱스 0, 1, 2를 1 증가시킵니다.
- 증가시킬 위치가 현재 릴리즈 길이보다 크면 0을 채워 길이를 자동으로 확장합니다.
- 이후의 모든 릴리즈 인덱스는 0으로 초기화됩니다.
- `epoch`는 그대로 유지하며, `pre`, `post`, `dev`, `local` 세그먼트는 무조건 제거됩니다.
- 기존 객체는 수정되지 않고 새 `Version` 인스턴스를 반환합니다.
- 그 밖의 `part` 값은 `ValueError`를 던집니다.

기존 클래스 구조 및 테스트에는 영향을 주지 않도록 `__replace__`를 활용하여 구현했으며, 추가 수정은 없습니다.