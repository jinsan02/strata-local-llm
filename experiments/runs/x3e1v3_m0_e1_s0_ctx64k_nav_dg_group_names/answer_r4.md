수정을 완료했습니다. 변경 내용은 다음과 같습니다:

1. `src/packaging/dependency_groups.py`:
   - `InvalidGroupName` 예외 클래스 (`ValueError` 서브클래스) 추가 및 `__all__`에 등록.
   - `packaging.utils`의 `_validate_regex`를 import하여 이름 검증에 사용.
   - `_normalize_group_names` 함수에서 그룹 이름 유효성 검사를 수행하고, 유효하지 않은 경우 `_ErrorCollector`에 `InvalidGroupName` 오류를 추가하여 `__init__`에서 기존 오류(중복 등)와 함께 한꺼번에 보고.
   - `lookup()` 및 `resolve()` 메서드에서 유효하지 않은 그룹 이름이 입력되면 즉시 `InvalidGroupName` 예외를 던지도록 수정.