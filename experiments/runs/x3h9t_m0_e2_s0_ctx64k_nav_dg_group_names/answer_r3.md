수정을 완료했습니다. 변경 내용은 다음과 같습니다:

- `src/packaging/dependency_groups.py` 파일에 `InvalidGroupName` 예외 클래스(`ValueError` 하위)를 추가하고 `__all__`에 등록했습니다.
- `packaging.utils._validate_regex`를 import하여 기존 `Name` 필드 검증 규칙을 그대로 재사용했습니다.
- `_normalize_group_names()` 함수에서 각 그룹 키를 검사하여 규칙을 위반하는 이름마다 `InvalidGroupName`을 생성해 기존 오류(중복 등)와 함께 `_ErrorCollector`에 수집하도록 했습니다.
- `DependencyGroupResolver.lookup()`과 `resolve()` 메서드에서 입력받은 이름이 유효한지 `_is_valid_group_name()`으로 먼저 검사하며, 위반 시 다른 처리 없이 즉시 `InvalidGroupName`을 단일 예외로 던지도록 했습니다.

기존 공개 테스트(`tests/test_dependency_groups.py`)는 모두 통과합니다. 기존 동작(정규화, 중복 검사, 순환 검사 등)은 변경되지 않았습니다.