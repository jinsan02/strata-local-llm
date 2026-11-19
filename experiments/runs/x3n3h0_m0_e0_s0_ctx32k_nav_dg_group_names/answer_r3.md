모든 수정을 완료했습니다. `src/packaging/dependency_groups.py` 파일에 다음 변경 사항을 적용했습니다:

1. `.utils.canonicalize_name` 임포트 추가 (기존 정규식 검증 로직 재사용)
2. `__all__` 에 `"InvalidGroupName"` 추가
3. `InvalidGroupName(ValueError)` 예외 클래스 정의
4. `_normalize_group_names()` 에서 `canonicalize_name(..., validate=True)`로 그룹 이름 검증 및 정규화 수행. 실패 시 `InvalidGroupName` 예외를 오류 수집기에 누적 (기존 중복 검사 로직과 동일한 방식)
5. `DependencyGroupResolver.lookup()` 과 `.resolve()` 메소드 시작 부분에서 이름을 먼저 검증하고, 틀리면 즉시 `InvalidGroupName(f"{group!r} is not a valid name")` 단일 예외로 던지도록 변경

이외에 기존 동작(정규화, 중복 검사, include, 순환 검사)은 변하지 않았습니다.