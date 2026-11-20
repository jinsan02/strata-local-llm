수정 내용을 요약하면 다음과 같습니다:

1. `src/packaging/dependency_groups.py`에 `InvalidGroupName` 예외 클래스(`ValueError` 하위)를 추가하고 `__all__`에 등록했습니다.
2. `.utils` 모듈에서 `canonicalize_name`과 `InvalidName`을 임포트하여 핵심 메타데이터 `Name` 필드의 검증 규칙을 재사용했습니다.
3. `_normalize_group_names` 함수에서 각 그룹 키에 대해 `canonicalize_name(..., validate=True)`를 호출합니다. 규칙을 위반한 키는 `InvalidGroupName` 예외로 생성하여 기존 에러 컬렉터에 함께 수집합니다. (메시지에는 `!r` 포맷으로 원래 이름이 포함됩니다.)
4. `DependencyGroupResolver.lookup()` 및 `resolve()` 메서드에서 인자로 받은 그룹 이름이 유효한지 즉시 검사합니다. 위반 시 다른 처리 없이 `InvalidGroupName` 단일 예외를 던지도록 수정했습니다.
5. 기존 정규화, 중복 이름 검사, include 및 순환 검사 로직은 그대로 유지하였습니다.

기존 테스트는 모두 통과하였습니다.