수정 완료. 변경 사항 요약:

1. **`InvalidGroupName` 예외 클래스 추가**: `ValueError` 하위 클래스로, 그룹 이름이 core metadata `Name` 필드 규칙을 따르지 않을 때 사용.

2. **`__all__` 에 `InvalidGroupName` 추가**: 공개 API로 노출.

3. **`utils._validate_regex` import**: `packaging.utils.canonicalize_name(..., validate=True)`에서 사용하는 동일한 정규식(`[a-z0-9]|[a-z0-9][a-z0-9._-]*[a-z0-9]`)을 재사용. 새 정규식 생성 없음.

4. **`_normalize_group_names` 수정**: 각 그룹 이름을 `_validate_regex`로 검사. 규칙을 위반하면 `_ErrorCollector`에 `InvalidGroupName`을 누적하여 `DependencyGroupResolver.__init__`에서 기존 오류(중복 이름 등)와 같은 방식으로 `ExceptionGroup`으로 한꺼번에 보고. 메시지에는 원래 이름이 `repr` 형태 포함.

5. **`lookup()` 과 `resolve()` 수정**: 정규화 전에 그룹 이름을 즉시 검사하여 규칙 위반 시 `InvalidGroupName`을 단일 예외로 바로 던짐.