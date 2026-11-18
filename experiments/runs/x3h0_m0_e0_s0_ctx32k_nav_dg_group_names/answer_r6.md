수정을 마쳤습니다. `src/packaging/dependency_groups.py` 파일에 다음 사항을 적용했습니다:

1. `.utils._validate_regex`를 import하여 core metadata `Name` 필드 규칙 검증에 공유했습니다.
2. `InvalidGroupName(ValueError)` 예외 클래스를 추가하고 `__all__`에 등록했습니다. 메시지 포맷은 `{group_name!r}`을 포함합니다.
3. `DependencyGroupResolver.__init__`에서 입력 매핑의 키들을 순회하며 유효성을 검사하고, `_ErrorCollector`를 통해 기존 중복 오류 등과 동일한 방식으로 수집 후 집합 예외로 보고하도록 변경했습니다.
4. `lookup()` 및 `resolve()` 메서드에 정규식 검증을 최상단에 배치하여, 이름이 규칙에 맞지 않으면 정규화나 캐시 조회 등 다른 처리 전에 즉시 단일 `InvalidGroupName` 예외를 던지도록 수정했습니다.

기존의 이름 정규화, 중복 검사, include 순환 검사 로직은 그대로 유지되었습니다.