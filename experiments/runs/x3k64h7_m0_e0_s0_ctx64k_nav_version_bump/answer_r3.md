`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part`가 `"major"`, `"minor"`, `"micro"`인 경우 각각 release의 첫 번째, 두 번째, 세 번째 숫자를 1 올리고 뒤의 숫자를 0으로 만듭니다.
- 올릴 자리가 현재 release보다 길면 0을 채워 확장합니다 (예: `1` → micro → `1.0.1`).
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 버립니다.
- 그 밖의 `part` 값은 `ValueError`를 던집니다.
- 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환합니다.