`packaging/dependency_groups.py` 파일을 수정했습니다:

- `_validate_regex`를 `.utils` 모듈에서 임포트하여 그룹 이름 검사에 사용하도록 했습니다.
- `InvalidGroupName` 예외 클래스를 추가하고 `__all__` 에 포함했습니다.
- `_is_valid_group_name()` 헬퍼 함수를 추가했습니다.
- `_normalize_group_names()` 내부에서 그룹 이름을 검사하고, 유효하지 않은 이름은 `InvalidGroupName` 으로 수집하여 정규화 대상에서 제외합니다.
- `DependencyGroupResolver.lookup()` 과 `resolve()` 메서드에 이름 유효성 검사를 삽입하여, 잘못된 그룹 이름이 전달되면 정규화 전에 `InvalidGroupName` 을 즉시 발생시킵니다.