`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part` 가 `"major"`/`"minor"`/`"micro"`일 때 각각 release 튜플의 첫/둘/셋째 숫자를 1 올리고 뒤를 0 으로 채움
- 올릴 자리가 release 길이보다 길면 0 을 채워 확장 후 마지막을 1 로 함
- epoch 는 유지되고 pre/post/dev/local 은 모두 버림
- 잘못된 `part` 값은 `ValueError` 던짐
- `__replace__` 를 활용해 불변성을 유지하며 새 `Version` 반환