수정을 완료했습니다. `src/packaging/dependency_groups.py` 파일에서 다음 사항을 적용했습니다:

- `InvalidGroupName` 예외 클래스를 `ValueError` 하위로 추가하고 `__all__`에 등록했습니다.
- `packaging.utils._validate_regex`를 import하여 코어 메타데이터 `Name` 필드와 동일한 규칙을 재사용했습니다.
- `_normalize_group_names` 함수에서 각 그룹 이름 키를 검증하고, 규칙을 위반하는 경우 `InvalidGroupName` 예외를 기존 오류(중복 이름 등)와 함께 에러 컬렉터에 누적하도록 수정했습니다.
- `DependencyGroupResolver`의 `lookup()`과 `resolve()` 메서드에서 입력된 이름이 규칙에 맞지 않으면 정규화나 기타 처리 전에 즉시 단일 `InvalidGroupName` 예외를 던지도록 했습니다. 예외 메시지에는 `repr()` 형태로 원래 이름이 포함됩니다.
- 기존 이름 정규화, 중복 검사, 순환 검사 로직은 전혀 변경되지 않았습니다.