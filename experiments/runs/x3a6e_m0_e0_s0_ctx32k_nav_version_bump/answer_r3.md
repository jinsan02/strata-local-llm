수정 사항:
- `src/packaging/version.py` 의 `Version` 클래스에 `bump(part: str) -> Version` 메서드를 추가함
  - `part` 가 `"major"`, `"minor"`, `"micro"` 중 하나가 아니면 `ValueError` 발생
  - 해당 release 숫자를 1 올리고, 뒤의 모든 숫자는 0 으로 만듦
  - 타겟 자리가 현재 release 길이를 초과하면 0 으로 패딩하여 확장 (예: `1` → micro → `1.0.1`)
  - epoch 는 유지하고 pre/post/dev/local 은 모두 버림
  - `__replace__` 를 사용하여 새 객체 반환 (원본 불변)