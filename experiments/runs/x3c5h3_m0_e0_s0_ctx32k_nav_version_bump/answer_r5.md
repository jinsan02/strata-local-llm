`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `"major"`, `"minor"`, `"micro"` 중 하나를 받아 release의 해당 세그먼트를 1 증가시키고, 뒤의 모든 세그먼트를 0으로 만든다.
- 요청한 부분이 현재 release 길이를 초과하면 0을 채워 해당 길이까지 확장이 일어난다 (예: `1` → micro → `1.0.1`).
- epoch는 유지되고 pre/post/dev/local은 모두 버린다.
- 유효하지 않은 part 값에 대해 `ValueError`를 던진다.