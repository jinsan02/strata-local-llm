수정 사항을 요약하면 다음과 같습니다.

1. **`_validate_regex` 추가 임포트**: `packaging.utils._validate_regex`(Core Metadata `Name` 필드 검증 규칙)를 `.utils`에서 가져와 재사용했습니다. 새 정규식을 만들지 않았습니다.
2. **`InvalidGroupName` 예외 및 `__all__` 업데이트**: `ValueError` 하위 클래스 `InvalidGroupName`을 정의하고 공개 목록(`__all__`)에 포함했습니다.
3. **내부 검증 헬퍼 함수 추가**: `_check_valid_name()` 함수를 만들어 정규식 검증을 수행합니다. 실패 시 즉시 `InvalidGroupName`을 던집니다.
4. **`_normalize_group_names` 수정**: 컨스트럭터에서 그룹 키를 순회할 때 `_validate_regex.fullmatch()`로 유효성을 검사합니다. 규칙을 벗어난 이름은 기존 중복 오류 등 다른 오류와 동일하게 `_ErrorCollector`에 모아서 한꺼번에 보고(`errors.error()`)되며, 메시지에는 원래 이름의 `repr`이 포함됩니다.
5. **`lookup()` 및 `resolve()` 수정**: 메서드 진입 시 즉시 `_check_valid_name(group)`를 호출하여 정규화나 그외 전처리 전에 `InvalidGroupName`을 단일 예외로 바로 던지도록 했습니다.

기존 정규화, 중복 검사, include 참조 및 순환 검사 동작은 변경되지 않았습니다.