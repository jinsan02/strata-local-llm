수정을 완료했습니다. 변경된 내용은 다음과 같습니다.

- **src/packaging/specifiers.py**:
  - `_ranges` 모듈에서 `_next_prefix_dev0` 함수를 import 했습니다.
  - `SpecifierSet` 클래스에 `_strip_dev`, `_merge_lower`, `_merge_upper` 헬퍼 메서드를 추가했습니다.
  - `SpecifierSet` 클래스에 `bounds()` 메서드를 추가했습니다.