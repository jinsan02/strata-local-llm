요구사항 확인 결과:

1. **core metadata Name 규칙 재사용**: `dependency_groups.py:17` (`from .utils import _validate_regex`), `utils.py:73-75` (`_validate_regex`) — 새 정규식 없음 ✓
2. **`InvalidGroupName` 공개 예외 + `__all__`**: `dependency_groups.py:47-53` (`ValueError` 하위), `dependency_groups.py:25` (`__all__`) ✓
3. **`__init__` 에서 한꺼번에 보고 + `repr` 메시지**: `dependency_groups.py:342-345` (`_validate_regex.fullmatch` 검사 → `errors.error(InvalidGroupName(...))` → `errors.finalize` 로 `ExceptionGroup`), 메시지 `{group_name!r}` ✓
4. **`lookup()`/`resolve()` 에서 단일 예외 즉시 던지기**: `dependency_groups.py:158-159`, `174-175` (정규화 전 검사, `raise InvalidGroupName(...)`), 메시지 `{group!r}` ✓
5. **기존 동작 보존**: `dependency_groups.py:345` (`continue`로 규칙 위반 그룹은 중복 검사/정규화 로직에서 제외), `lookup`/`resolve` 나머지 로직 변경 없음 ✓

자동 검사: 129 passed, 문제 없음.

수정 완료.