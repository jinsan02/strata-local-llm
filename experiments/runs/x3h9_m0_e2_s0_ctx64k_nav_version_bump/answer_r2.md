`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Self` 메서드를 추가했습니다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나면 해당 인덱스의 release 숫자를 1 올리고, 뒤의 모든 숫자를 0 으로 만듭니다.
- release 길이가 부족하면 0 을 채워 늘립니다 (예: `1` → micro → `1.0.1`).
- epoch 는 그대로 유지하고, pre/post/dev/local 은 모두 버립니다.
- 그 밖의 `part` 값은 `ValueError` 를 던집니다.
- 원래 객체는 변하지 않고 새 `Version` 인스턴스를 반환합니다.