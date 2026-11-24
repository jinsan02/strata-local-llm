수정을 마쳤습니다. `src/packaging/dependency_groups.py` 파일에 다음 변경 사항을 적용했습니다:

1. `InvalidGroupName` 예외 클래스(`ValueError` 하위 클래스)를 추가하고 `__all__`에 등록했습니다.
2. `packaging.utils`의 `_validate_regex`를 import하여 그룹 이름 유효성 검사에 재사용했습니다.
3. `_validate_group_name()` 헬퍼 함수를 추가했습니다.
4. `_normalize_group_names()` 함수에서 각 그룹 이름을 검증하고, 규칙 위반 시 `InvalidGroupName`을 기존 오류(중복 등)와 함께 `_ErrorCollector`에 모아 한꺼번에 보고하도록 수정했습니다.
5. `DependencyGroupResolver`의 `lookup()`과 `resolve()` 메서드 시작 부분에 이름 검증을 추가하여, 규칙에 맞지 않는 이름이 넘어오면 정규화나 파싱 전에 `InvalidGroupName` 단일 예외를 바로 던지도록 했습니다.

기존 유효한 이름의 동작(정규화, 중복 검사, include, 순환 검사)은 변경되지 않았습니다. 테스트 파일은 수정하지 않았습니다.