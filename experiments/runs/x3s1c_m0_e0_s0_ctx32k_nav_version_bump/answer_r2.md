`src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가했습니다.

**변경 내용:**
- `Version` 클래스에 `bump` 메서드 추가 (라인 1112~1169)
  - `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError` 던짐
  - 해당 인덱스의 release 숫자를 1 올리고, 뒤의 모든 숫자를 0 으로 설정
  - 인덱스가 release 길이보다 크면 0 을 채워 확장 (예: `1` → micro → `1.0.1`)
  - epoch 는 그대로 유지, pre/post/dev/local 은 모두 버림
  - `__replace__` 를 사용해 새 `Version` 객체 반환 (원본 불변)