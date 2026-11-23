`src/packaging/dependency_groups.py` 파일에 다음 수정을 적용했습니다.

1. **`InvalidGroupName` 예외 클래스 추가**: `ValueError` 하위 클래스로, 그룹 이름이 core metadata의 `Name` 규칙을 따르지 않을 때 사용합니다.
2. **`__all__` 업데이트**: `InvalidGroupName`을 공개 API에 추가했습니다.
3. **`utils` 모듈 import**: 기존 이름 검증 로직을 재사용하기 위해 `packaging.utils`를 import했습니다.
4. **`_validate_group_name` 헬퍼 함수 추가**: 그룹 이름 유효성을 검사하고 유효하지 않으면 `InvalidGroupName`을 던집니다.
5. **`_normalize_group_names` 수정**: 초기화 시 그룹 이름을 검사하여 유효하지 않은 이름에 대해 `InvalidGroupName` 오류를 수집합니다. (중복 이름 등 기존 오류와 함께 보고됨)
6. **`lookup()`, `resolve()` 수정**: 호출 시 인자 이름을 즉시 검사하여 유효하지 않으면 `InvalidGroupName`을 단일 예외로 던집니다.

기존 테스트(`run_tests`)는 통과했습니다.