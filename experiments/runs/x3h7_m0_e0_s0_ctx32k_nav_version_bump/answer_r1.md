`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

- `part`가 `"major"`, `"minor"`, `"micro"`인 경우 각각 release의 첫 번째, 두 번째, 세 번째 숫자를 1 증가시키고, 뒤의 숫자를 모두 0으로 만듭니다.
- 올릴 자리가 release 길이보다 크면 0을 채워 늘립니다 (예: `1` → `1.0.1`).
- epoch는 그대로 유지하고, pre/post/dev/local은 모두 버립니다.
- 잘못된 `part` 값은 `ValueError`를 던집니다.
- `__replace__`를 사용해 새 `Version` 객체를 반환하므로 원래 객체는 변하지 않습니다.