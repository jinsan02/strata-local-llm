수정을 완료했습니다. 다음 내용을 수정했습니다:

- `src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가함.
  - `"major"`/`"minor"`/`"micro"` 중 하나만 허용하고 나머지는 `ValueError` 던짐.
  - 해당 release 인덱스를 1 증가시키고, 뒤쪽 모든 요소를 0 으로 채움.
  - 요청한 자리가 release 길이를 초과하면 0 을 채워 확장함 (예: `(1,)` → micro → `(1,0,1)`).
  - epoch 는 유지하고, pre/post/dev/local 은 모두 버림.
  - `__replace__` 를 사용해 새 `Version` 객체를 반환 (원본 불변).