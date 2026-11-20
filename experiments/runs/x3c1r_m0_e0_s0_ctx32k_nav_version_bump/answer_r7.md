수정 내용:
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.
  - `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나일 때 해당 인덱스의 release 요소를 1 증가시키고, 이후 모든 요소를 0 으로 설정한다.
  - 요청된 인덱스가 현재 release 길이보다 크면 0 으로 채워 확장한다 (예: `(1,)` → micro → `(1, 0, 1)`).
  - epoch 는 그대로 유지하고, pre/post/dev/local 은 모두 버린다.
  - 유효하지 않은 `part` 값이면 `ValueError` 를 던진다.
  - 원래 객체는 변하지 않고 새 `Version` 인스턴스를 반환한다.