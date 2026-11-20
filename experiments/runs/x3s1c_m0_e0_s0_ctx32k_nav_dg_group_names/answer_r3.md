수정 완료. `src/packaging/dependency_groups.py` 파일에 다음 사항을 적용했습니다:

1. `InvalidGroupName` 예외 클래스(`ValueError` 하위)를 추가하고 `__all__` 에 등록했습니다.
2. `packaging.utils._validate_regex`를 임포트하여 core metadata `Name` 규칙을 재사용했습니다.
3. `_normalize_group_names()` 함수 내에서 그룹 이름 키를 검증하고, 규칙 위반 시 `InvalidGroupName` 오류를 `_ErrorCollector`에 수집하여 `DependencyGroupResolver.__init__`에서 기존 오류(중복 등)와 함께 한꺼번에 보고하도록 했습니다.
4. `lookup()` 및 `resolve()` 메서드 시작 부분에서 그룹 이름 검증 로직을 추가하여, 규칙 위반 시 즉시 `InvalidGroupName` 단일 예외를 던지도록 했습니다.

기존 정규화, 중복 검사, 순환 검사 로직은 변경 없이 유지되었습니다.