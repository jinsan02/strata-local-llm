수정 완료했습니다.

**바꾼 내용:** `src/packaging/version.py` 파일 내 `Version` 클래스의 `__replace__` 메서드 뒤에 `bump(self, part: str) -> Version` 메서드를 추가했습니다. 이 메서드는 다음과 같이 동작합니다:

- `part` 가 `"major"` (첫 번째), `"minor"` (두 번째), `"micro"` (세 번째) 에 따라 해당 위치의 숫자를 1 증가시키고 이후 숫자를 모두 잘라냅니다.
- 요청한 위치가 현재 release 튜플보다 크면 0 을 채워 그 자리까지 확장합니다.
- epoch 는 그대로 유지하고, pre/post/dev/local 은 모두 버립니다.
- 잘못된 `part` 값이면 `ValueError` 를 던집니다.