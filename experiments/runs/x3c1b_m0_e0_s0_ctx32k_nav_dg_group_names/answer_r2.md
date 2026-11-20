요청하신 수정 사항을 모두 `src/packaging/dependency_groups.py`에 적용했습니다. 주요 변경 내용은 다음과 같습니다:

1. `utils._validate_regex`(코어 메타데이터 `Name` 필드 규칙)를 임포트하여 재사용했습니다.
2. `__all__`에 `"InvalidGroupName"`을 추가하고, `ValueError` 하위 클래스로 예외를 정의했습니다.
3. `_normalize_group_names()` 내부에서 그룹 키마다 정규식 검사를 수행해 위반 항목이 있으면 `InvalidGroupName` 오류를 `_ErrorCollector`에 쌓아두어, 기존 중복 이름 오류 등과 함께 `ExceptionGroup`으로 한꺼번에 보고되도록 했습니다.
4. `DependencyGroupResolver.lookup()`과 `resolve()` 메서드 상단에 입력값 유효성 검사를 추가해, 규칙에 맞지 않는 이름이 넘어오면 즉시 `InvalidGroupName` 단일 예외를 던지도록 했습니다.

기존 테스트 파일은 건들지 않았으며, 기존 동작(정규화, 중복 검사, include, 순환 검사)은 변경되지 않았습니다.