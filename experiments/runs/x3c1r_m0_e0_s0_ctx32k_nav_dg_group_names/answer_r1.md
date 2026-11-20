`src/packaging/dependency_groups.py` 파일에 다음 수정을 적용했습니다:

1. `.utils`의 `_validate_regex`를 `import`하여 핵심 메타데이터 `Name` 필드 검증 규칙을 재사용했습니다.
2. `InvalidGroupName` (`ValueError` 하위 클래스) 예외를 정의하고 공개 인터페이스(`__all__`)에 추가했습니다.
3. `_is_valid_group_name()` 헬퍼 함수를 추가해 `_validate_regex.fullmatch()`로 유효성을 검사합니다.
4. `_normalize_group_names()`에서 매핑의 각 키에 대해 유효성 검사를 수행하며, 규칙을 위반하는 이름이 있으면 기존 중복명 오류와 동일하게 `_ErrorCollector`를 통해 `InvalidGroupName` 예외를 누적합니다. 최종적으로 `finalize()` 호출 시 하나의 ExceptionGroup으로 한꺼번에 보고됩니다. 메시지에는 원래 이름이 `{group!r}` 형식으로 포함됩니다.
5. `DependencyGroupResolver.lookup()`과 `resolve()`는 매개변수로 넘어온 그룹 이름의 유효성을 정규화(`_normalize_name`) 전 단계에서 즉시 검사하며, 위반 시 `InvalidGroupName`을 단일 예외로 바로 던지도록 수정했습니다. 기존 검증·정규화·순환 검사 로직은 그대로 유지됩니다.