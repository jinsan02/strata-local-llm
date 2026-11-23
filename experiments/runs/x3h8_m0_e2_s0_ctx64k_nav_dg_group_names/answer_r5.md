모든 요구사항 확인 완료:

- **core metadata Name 규칙 재사용**: `src/packaging/dependency_groups.py:17` (`from .utils import _validate_regex`), `:323-325` (`_validate_regex.fullmatch`)
- **`InvalidGroupName` 공개 예외**: `:47-52` (ValueError 하위 클래스), `:25` (`__all__` 포함)
- **`DependencyGroupResolver.__init__` 에서 한꺼번 보고**: `:342-346` (`_normalize_group_names` → `errors.error(e)`), `:324` (`{name!r}` repr 형식)
- **`lookup()`/`resolve()` 에서 단일 예외 즉시 던짐**: `:157`, `:171` (`_validate_group_name()` → 정규화 전 호출)
- **기존 동작 유지**: 중복 검사, 정규화, include, 순환 검사 로직 변경 없음
- **자동 검사**: 코드 검사 통과, 테스트 129개 모두 통과

수정 사항 없음. 과제 완료.