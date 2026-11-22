수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

**변경 내용:**
- `Version` 클래스의 `__replace__` 메서드 뒤에 `bump` 메서드 추가 (약 67줄)
- `part`가 `"major"`, `"minor"`, `"micro"`인 경우 각각 release 튜플의 인덱스 0, 1, 2를 1 증가시키고 뒤의 요소를 0으로 설정
- 인덱스가 현재 release 길이보다 크면 release 튜플을 0으로 확장 후 해당 인덱스를 1로 설정
- epoch는 유지하고, pre/post/dev/local은 모두 제거 (None)
- 유효하지 않은 `part` 값은 `ValueError` 발생
- `__replace__`를 사용해 새 `Version` 객체 반환 (원본 불변)