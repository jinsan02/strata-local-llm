수정 사항 요약:
- `src/packaging/dependency_groups.py`에 `InvalidGroupName(ValueError)` 예외 클래스를 추가하고 `__all__`에 등록했습니다.
- `.utils`의 기존 `canonicalize_name(..., validate=True)` 함수를 재사용하여 핵심 메타데이터 `Name` 필드의 검증 규칙을 따르도록 했습니다. (새 정규식 생성 없음)
- `_normalize_group_names()`에서 각 키를 검증해 잘못된 이름마다 `InvalidGroupName`을 `_ErrorCollector`로 수집하도록 수정했습니다. (`__init__` 시 기존 중복 이름 오류와 같은 방식으로 `ExceptionGroup`으로 한꺼번에 보고됨)
- `DependencyGroupResolver.lookup()`과 `resolve()`에서 입력된 그룹 이름이 규칙에 맞지 않으면 즉시 단일 `InvalidGroupName` 예외를 던지도록 했습니다.
기존 정규화, 중복 검사, include 순환 검사 등 기존 동작은 변경하지 않았습니다.