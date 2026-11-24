수정 완료. 변경 사항을 요약하면:

1. **`InvalidGroupName` 예외 클래스 추가**: `ValueError` 하위 클래스로 `src/packaging/dependency_groups.py`에 정의하고 `__all__` 에 등록.

2. **`_validate_regex` import**: `packaging.utils`에서 core metadata `Name` 필드 검증에 사용하는 정규식(`_validate_regex`)을 가져옴. 새 정규식을 만들지 않음.

3. **`_validate_name()` 헬퍼 함수 추가**: `_validate_regex.fullmatch()`로 그룹 이름 유효성 검사. 실패 시 `InvalidGroupName` 예외 던짐. 메시지에는 `repr` 형태 포함.

4. **`DependencyGroupResolver.__init__`**: `_normalize_group_names()` 내에서 각 그룹 이름을 `_validate_name()`으로 검사. 규칙 위반 시 `InvalidGroupName`을 `_ErrorCollector`에 수집하여 기존 오류(중복 이름 등)와 같은 방식으로 `ExceptionGroup`으로 한꺼번에 보고.

5. **`lookup()`과 `resolve()`**: 다른 처리(정규화 등) 전에 `_validate_name()`으로 이름을 즉시 검사. 규칙 위반 시 단일 `InvalidGroupName` 예외를 바로 던짐.