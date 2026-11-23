`src/packaging/dependency_groups.py` 파일에 다음 수정을 적용했습니다:

1. `packaging.utils._validate_regex`를 import하여 기존 `Name` 필드 검증 규칙을复用.
2. `InvalidGroupName` 예외 클래스(`ValueError` 하위)를 정의하고 `__all__`에 등록.
3. `_validate_group_name()` 헬퍼 함수를 추가.
4. `_normalize_group_names()` 함수에서 그룹 이름 키를 검증하고, 규칙 위반 시 `InvalidGroupName`을 `_ErrorCollector`에 추가하여 기존 오류(중복 이름 등)와 함께 `ExceptionGroup`으로 한꺼번에 보고하도록 수정.
5. `DependencyGroupResolver`의 `lookup()` 및 `resolve()` 메서드 시작 부분에 `_validate_group_name(group)` 호출을 추가하여, 유효하지 않은 이름을 넘기면 `InvalidGroupName`을 단일 예외로 즉시 던지도록 수정.

기존 정규화, 중복 검사, include, 순환 검사 동작은 변경되지 않았습니다.