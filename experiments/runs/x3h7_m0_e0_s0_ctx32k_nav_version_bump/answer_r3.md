수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

- `part`가 `"major"`/`"minor"`/`"micro"`일 때 각각 release의 1/2/3번째 숫자를 1 올리고 뒤를 0으로 채운다.
- release 길이가 부족하면 0을 채워 확장한다.
- epoch는 유지하고, pre/post/dev/local은 모두 버린다.
- 유효하지 않은 `part` 값은 `ValueError`를 던진다.
- `__replace__`를 사용해 새 `Version` 객체를 반환하며 원래 객체는 변경되지 않는다.