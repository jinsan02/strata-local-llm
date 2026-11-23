모든 요구사항을 확인한 결과, 누락이나 오류가 없습니다.

- **`part` 값 처리**: `"major"`/`"minor"`/`"micro"`만 허용, 나머지는 `ValueError` (src/packaging/version.py:1187-1198)
- **release 길이 유지 및 확장**: `while len(release) <= index: release.append(0)` (src/packaging/version.py:1202-1203)
- **epoch 유지, pre/post/dev/local 버림**: `__replace__(release=..., pre=None, post=None, dev=None, local=None)` (src/packaging/version.py:1209-1214)
- **대소문자 구분 ValueError**: `"Major"`, `"MINOR"` 등은 허용되지 않음 (src/packaging/version.py:1187-1198)
- **불변성**: `__replace__`가 새 `Version` 반환 (src/packaging/version.py:1209-1214)
- **기존 동작 불변**: 기존 테스트 51524개 모두 통과

수정 사항:
- `src/packaging/version.py`의 `Version` 클래스에 `bump(part: str) -> Version` 메서드 추가 (docstring 포함)