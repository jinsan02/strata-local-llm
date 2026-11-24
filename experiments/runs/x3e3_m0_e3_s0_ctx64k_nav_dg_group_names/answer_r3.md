수정 완료. 변경 사항을 요약하면:

1. `InvalidGroupName` 예외 클래스 추가 (`ValueError` 하위)
2. `__all__`에 `InvalidGroupName` 추가
3. `packaging.utils._validate_regex`를 import하여 그룹 이름 검증에 사용
4. `_normalize_group_names()`에서 각 그룹 이름이 정규식과 맞는지 검사하고, 틀리면 `_ErrorCollector`를 통해 기존 오류와 같은 방식으로 한꺼번에 보고
5. `lookup()`과 `resolve()`에서 입력 이름이 규칙에 맞지 않으면 `InvalidGroupName`을 단일 예외로 즉시 던짐