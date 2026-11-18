다음과 같이 수정하였습니다:
- `packaging.utils._validate_regex`를 임포트하여 핵심 메타데이터 `Name` 필드와 동일한 규칙으로 그룹 이름을 검증
- `InvalidGroupName(ValueError)` 예외 클래스 추가 및 `__all__` 에 등록
- `_normalize_group_names()` 에서 각 키의 유효성을 검사하고, 실패 시 `_ErrorCollector` 를 통해 기존 오류(중복 등)와 함께 한꺼번에 보고 (메시지에 `repr` 형태 포함)
- `_validate_name()` 헬퍼 함수 추가
- `DependencyGroupResolver.lookup()`, `resolve()` 진입 초기에 `_validate_name()` 호출하여 단일 예외를 즉시 던지도록 수정
기존 정규화, 중복 검사, include 및 순환 검사 등 정상 동작은 그대로 유지됨. 완료.