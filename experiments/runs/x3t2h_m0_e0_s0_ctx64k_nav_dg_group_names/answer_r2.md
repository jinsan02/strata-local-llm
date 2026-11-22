다음 내용을 `src/packaging/dependency_groups.py` 에 적용했습니다:

- `.utils._validate_regex`를 import하고 `InvalidGroupName` 예외 클래스를 추가했습니다.
- `_is_valid_group_name()` 헬퍼 함수를 추가했습니다.
- `_normalize_group_names()` 에서 그룹 이름 유효성 검사를 수행하여 `errors` 컬렉터에 모으도록 수정했습니다.
- `lookup()` 과 `resolve()` 메서드에서 입력된 그룹 이름이 규칙에 맞지 않으면 정규화 전에 즉시 `InvalidGroupName` 을 던지도록 수정했습니다.

기존 정규화, 중복 검사, include 및 순환 검사 로직은 그대로 유지되었습니다.