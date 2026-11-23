다음과 같이 `src/packaging/dependency_groups.py` 파일을 수정했습니다:

1. `utils._validate_regex`를 import하여 core metadata `Name` 필드 검증 규칙을 재사용했습니다.
2. `InvalidGroupName` 예외 클래스를 `ValueError` 하위 클래스로 추가하고 `__all__`에 등록했습니다.
3. `_normalize_group_names` 함수에서 그룹 키의 유효성을 검사하고, 규칙 위반 시 `InvalidGroupName`을 `_ErrorCollector`를 통해 기존 오류(중복 이름 등)와 함께 한꺼번에 보고하도록 했습니다.
4. `DependencyGroupResolver`의 `lookup()`과 `resolve()` 메서드에서 인자로 받은 그룹 이름이 규칙에 맞지 않으면 정규화 등 다른 처리 전에 `InvalidGroupName` 단일 예외를 즉시 던지도록 했습니다.

기존의 정규화, 중복 검사, include 및 순환 검사 로직은 변경하지 않았습니다.