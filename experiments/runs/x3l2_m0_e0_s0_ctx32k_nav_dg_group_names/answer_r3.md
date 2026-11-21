`src/packaging/dependency_groups.py` 파일에 다음 내용을 수정했습니다:

1.  **예외 클래스 추가**: `InvalidGroupName` 예외 클래스를 `ValueError` 하위로 추가하고 `__all__`에 포함했습니다.
2.  **검증 로직 import**: `utils` 모듈의 `_validate_regex`를 import 했습니다.
3.  **생성자 검증**: `_normalize_group_names` 함수에서 그룹 이름 유효성을 검사하여, 규칙에 맞지 않는 이름마다 `InvalidGroupName` 오류를 에러 컬렉터에 추가했습니다.
4.  **메서드 검증**: `DependencyGroupResolver`의 `lookup` 및 `resolve` 메서드에서 그룹 이름 유효성을 검사하고, 유효하지 않으면 즉시 `InvalidGroupName` 예외를 던지도록 수정했습니다.