수정 완료. `src/packaging/dependency_groups.py` 파일에서 다음 사항을 변경했습니다:

1. `packaging.utils._validate_regex`를 import하여 프로젝트 이름 규칙을 재사용.
2. `InvalidGroupName` 예외 클래스(`ValueError` 하위)를 정의하고 `__all__`에 추가.
3. `_normalize_group_names` 함수에 그룹 이름 유효성 검사 로직을 추가하여, `DependencyGroupResolver` 초기화 시 중복 이름 오류 등 기존 오류와 함께 `ExceptionGroup`으로 수집되도록 처리.
4. `lookup()` 및 `resolve()` 메서드에 이름 검사 로직을 추가하여, 유효하지 않은 이름이 전달되면 즉시 `InvalidGroupName` 단일 예외를 던지도록 처리.