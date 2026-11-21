수정 내용 요약:
1. `InvalidGroupName` 예외 클래스(`ValueError` 하위)를 `dependency_groups.py`에 추가하고 `__all__`에 등록했습니다.
2. `.utils._validate_regex`를 임포트하여 핵심 메타데이터 `Name` 필드 규칙을 재사용했습니다.
3. `_validate_group_name` 헬퍼 함수를 추가했습니다.
4. `_normalize_group_names` 함수에서 그룹 키 검증 후, 기존 `_ErrorCollector` 패턴과 동일하게 검증 오류를 수집하여 `__init__` 시 한꺼번에 보고하도록 수정했습니다.
5. `DependencyGroupResolver.lookup()`과 `resolve()` 메서드에서 파라미터 검증 후 정규화 등 다른 처리 전 `InvalidGroupName`을 단일 예외로 즉시 던지도록 수정했습니다.
기존 정규화, 중복 검사, 순환 검사 로직은 변경하지 않았습니다.