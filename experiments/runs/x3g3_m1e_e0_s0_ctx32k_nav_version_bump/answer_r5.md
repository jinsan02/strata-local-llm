수정하지 않은 테스트 파일이 bump 관련 테스트를 포함하고 있지 않으므로, 기존 테스트와의 충돌은 없다.

수정 내용 요약:
- `src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했다.
  - `part` 가 `"major"`, `"minor"`, `"micro"` 일 때 각각 release 튜플의 첫 번째, 두 번째, 세 번째 요소를 1 증가시키고 뒤의 요소를 0 으로 만든다.
  - 올릴 자리가 없으면 release 길이를 0 으로 채워 늘린다.
  - epoch 는 유지하고, pre/post/dev/local 은 모두 버린다.
  - 그 외 `part` 값은 `ValueError` 를 던진다.
  - `__replace__` 메서드를 재사용하여 새 `Version` 객체를 반환한다.