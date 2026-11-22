수정을 완료했습니다. 변경 내용은 다음과 같습니다.

1. `src/packaging/dependency_groups.py`:
   - `from .utils import _validate_regex` import 추가.
   - `__all__`에 `InvalidGroupName` 추가.
   - `InvalidGroupName` 예외 클래스 정의 (`ValueError` 하위 클래스).
   - `_normalize_group_names` 함수에서 그룹 이름 유효성 검사 추가 (`_validate_regex` 사용), 실패 시 `_ErrorCollector`를 통해 `InvalidGroupName` 오류 수집.
   - `DependencyGroupResolver.lookup()` 메서드에서 이름 검사 후 `InvalidGroupName` 즉시 던지기.
   - `DependencyGroupResolver.resolve()` 메서드에서 이름 검사 후 `InvalidGroupName` 즉시 던지기.