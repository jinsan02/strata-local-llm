수정 완료. `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.

구현 내용:
- `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나인 경우 해당 인덱스의 release 숫자를 1 올리고, 뒤의 숫자는 모두 0 으로 채움
- 올릴 자리가 release 길이보다 긴 경우 release 길이를 0 을 채워 늘림
- epoch 는 유지하고, pre/post/dev/local 은 모두 None 으로 설정 (버림)
- 유효하지 않은 `part` 값은 `ValueError` 던짐
- `__replace__` 메서드를 사용해 새 `Version` 객체 반환 (원본 객체 불변)