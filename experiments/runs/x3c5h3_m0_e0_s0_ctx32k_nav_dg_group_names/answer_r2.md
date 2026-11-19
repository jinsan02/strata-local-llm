수정 내용 요약:

1. **`__all__` 수정**: `packaging.dependency_groups` 모듈의 공개 인터페이스에 `InvalidGroupName`을 추가했습니다.
2. **예외 클래스 추가**: `ValueError`를 상속하는 `InvalidGroupName` 예외 클래스를 정의했습니다.
3. **정규식 패턴 추가**: `packaging.utils`의 `Name` 필드 검증에 사용한 것과 동일한 정규식(`_GROUP_NAME_PATTERN`)을 재사용하여 패턴을 정의했습니다.
4. **`DependencyGroupResolver.__init__` 로직 수정 (`_normalize_group_names`)**: 그룹 이름을 정규화하는 과정에서 유효성 검사를 수행하며, 규칙을 지키지 않는 이름이 발견될 경우 `_ErrorCollector`를 통해 기존 오류(중복 등)와 함께 보고합니다.
5. **`lookup()` 메서드 수정**: 유효하지 않은 이름을 입력받으면 즉시 `InvalidGroupName` 예외를 단일 예외로 던집니다.
6. **`resolve()` 메서드 수정**: `lookup()`과 동일하게 유효하지 않은 이름을 입력받으면 즉시 `InvalidGroupName` 예외를 던지도록 했습니다.