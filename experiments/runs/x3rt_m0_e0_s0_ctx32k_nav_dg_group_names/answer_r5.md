수정 완료. `src/packaging/dependency_groups.py` 파일에 다음 사항을 적용했습니다:

1. `InvalidGroupName` 예외 클래스(`ValueError` 하위)를 정의하고 `__all__`에 추가했습니다.
2. 기존 `packaging.utils.canonicalize_name`의 검증 로직을 재사용하여 그룹 이름 유효성을 검사합니다.
3. `DependencyGroupResolver.__init__` 내부의 `_normalize_group_names` 함수에서 각 키를 검증하고, 규칙을 위반하면 `_ErrorCollector`를 통해 기존 오류(중복 이름 등)와 함께 한꺼번에 보고합니다.
4. `lookup()` 및 `resolve()` 메서드 시작 부분에 이름 검증을 추가하여, 유효하지 않은 이름이 전달되면 즉시 `InvalidGroupName` 단일 예외를 던지도록 했습니다.

기존 정상 동작은 변경되지 않았습니다.