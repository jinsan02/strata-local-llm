다음과 같이 수정했습니다:

- `packaging.utils._validate_regex`를 import하여 핵심 메타데이터 `Name` 필드 규칙 검증에 사용했습니다.
- `InvalidGroupName` 예외 클래스(`ValueError` 하위)를 `dependency_groups.py`에 추가하고 `__all__`에 등록했습니다.
- `_normalize_group_names` 함수에서 각 그룹 키를 `_validate_regex`로 검증합니다. 규칙을 위반하면 `InvalidGroupName`을 `_ErrorCollector`에 추가하여, `DependencyGroupResolver.__init__` 종료 시 기존 오류(중복 이름 등)와 함께 `ExceptionGroup`으로 한꺼번에 보고하도록 했습니다. 메시지에는 원래 이름의 `repr` 형태를 포함합니다.
- `lookup()`과 `resolve()` 메서드 시작 부분에 `_validate_regex` 검증을 추가하여, 유효하지 않은 이름이 전달되면 즉시 `InvalidGroupName` 단일 예외를 던지도록 했습니다.
- 기존 정규화, 중복 검사, `include` 및 순환 검사 로직은 전혀 변경되지 않았습니다.