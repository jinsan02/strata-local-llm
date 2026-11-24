수정 내용:
- `src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Self` 메서드를 추가했다.
  - `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나인 경우 해당 인덱스의 release 값을 1 증가시키고 뒤의 값을 모두 0 으로 설정한다.
  - 인덱스가 release 길이보다 크면 release 튜플을 0 으로 채워 확장한다.
  - epoch 는 그대로 유지하고, pre/post/dev/local 은 버린다.
  - 유효하지 않은 `part` 값이면 `ValueError` 를 던진다.
  - 원래 객체는 변경되지 않고 새 `Version` 인스턴스를 반환한다.