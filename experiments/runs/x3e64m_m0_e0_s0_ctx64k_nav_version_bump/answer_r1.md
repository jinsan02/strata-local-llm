`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Self` 메서드를 추가했다.

- `part` 가 `"major"`, `"minor"`, `"micro"` 인 각각 release 튜플의 첫 번째, 두 번째, 세 번째 요소를 1 증가시키고, 그 뒤의 모든 요소를 0 으로 설정한다.
- 올릴 자리가 release 길이보다 크면 0 을 채워 해당 길이까지 늘린다.
- epoch 는 그대로 유지하고, pre/post/dev/local 은 모두 버린다(`__replace__` 에 `None` 을 전달).
- 유효하지 않은 `part` 값은 `ValueError` 를 던진다.
- 원래 객체는 불변이며 새 `Version` 인스턴스를 반환한다.