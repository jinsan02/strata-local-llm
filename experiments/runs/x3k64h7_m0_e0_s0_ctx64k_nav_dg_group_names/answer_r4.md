수정이 완료되었습니다. 변경 사항을 요약하면:

1. **`InvalidGroupName` 예외 클래스 추가**: `ValueError` 하위 클래스로, 그룹 이름이 core metadata의 `Name` 필드 규칙을 따르지 않을 때 사용됨.
2. **`__all__`에 `InvalidGroupName` 추가**: 공개 API로 노출.
3. **`utils._validate_regex` import**: 기존에 `packaging.utils`에 있는 정규식을 재사용하여 새 정규식 creation을 피함.
4. **`_normalize_group_names` 수정**: 각 그룹 이름에 대해 `_validate_regex.fullmatch()` 검사. 실패 시 `InvalidGroupName`을 `_ErrorCollector`에 추가하여 기존 오류(중복 이름 등)와 같은 방식으로 한꺼번에 보고.
5. **`lookup()` 수정**: 정규화 전에 그룹 이름 유효성 검사. 실패 시 `InvalidGroupName` 단일 예외 던짐.
6. **`resolve()` 수정**: 정규화 전에 그룹 이름 유효성 검사. 실패 시 `InvalidGroupName` 단일 예외 던짐.