다음과 같이 `src/packaging/dependency_groups.py`를 수정했습니다:

- `utils._validate_regex`를 import하여 기존 `Name` 필드 검증 규칙을 재사용했습니다.
- `InvalidGroupName(ValueError)` 예외 클래스를 정의하고 `__all__`에 추가했습니다.
- `_normalize_group_names` 함수에서 각 그룹 이름의 유효성을 검사하여 `errors.error()`로 수집하고, 초기화 완료 시 기존 오류와 함께 `ExceptionGroup`으로 한꺼번에 보고하도록 수정했습니다.
- `lookup()`과 `resolve()` 메서드에서 입력 파라미터의 유효성을 즉시 검사하여, 규칙 위반 시 `InvalidGroupName`을 단일 예외로 바로 던지도록 수정했습니다.
기존 정규화, 중복 검사, include 및 순환 검사 동작은 그대로 유지되었습니다.