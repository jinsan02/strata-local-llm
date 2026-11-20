`src/packaging/dependency_groups.py` 파일에 다음 수정을 적용했습니다:

- `InvalidGroupName` 예외 클래스를 `ValueError` 하위 클래스로 추가하고 `__all__`에 등록했습니다.
- `packaging.utils._validate_regex`를 임포트하여 기존 `canonicalize_name`에서 사용하는 프로젝트 이름 검증 규칙을 그대로 재사용했습니다.
- `_normalize_group_names` 함수에서 각 키에 대해 `_validate_regex.fullmatch()` 검사를 수행하고, 실패 시 `InvalidGroupName`을 `_ErrorCollector`에 추가했습니다. 이로 인해 `DependencyGroupResolver.__init__` 호출 시 중복 이름 오류 등과 함께 `ExceptionGroup`으로 한꺼번에 보고됩니다. 메시지에는 `repr` 형태가 포함됩니다.
- `lookup()` 및 `resolve()` 메서드에서 전달된 그룹 이름이 규칙에 맞지 않으면 정규화나 캐시 조회 등 다른 처리 전에 `InvalidGroupName`을 단일 예외로 즉시 던지도록 했습니다.
- 기존 그룹 이름 정규화(`_normalize_name`), 중복 검사, include 파싱, 순환 검사 로직은 그대로 유지했습니다.