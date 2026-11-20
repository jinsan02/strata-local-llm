수정 내용을 요약하면 다음과 같습니다.

1. `src/packaging/dependency_groups.py` 파일에 `.utils._validate_regex`를 import했습니다. (기존 `canonicalize_name`의 검증 로직과 동일한 정규식)
2. `ValueError` 하위 클래스인 `InvalidGroupName` 예외를 정의하고 `__all__`에 추가했습니다. 메시지에는 `repr()` 포맷된 원래 이름이 포함됩니다.
3. `_normalize_group_names()` 함수에서 각 키의 유효성을 즉시 검사하여 규칙 위반 시 해당 오류를 기존 `_ErrorCollector`에 추가합니다. 중복 검사 로직과 함께 한꺼번에 보고됩니다.
4. `DependencyGroupResolver.lookup()` 및 `resolve()` 메서드 상단에 `_validate_regex.fullmatch(group)` 검사를 추가하여, 다른 처리(정규화, 캐시 조회 등) 전에 `InvalidGroupName` 단일 예외를 즉시 던지도록 수정했습니다.

기존의 이름 정규화, 중복 검사, include 순환 검사 동작은 변하지 않습니다.