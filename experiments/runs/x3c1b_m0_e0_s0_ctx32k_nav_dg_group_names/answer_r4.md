수정을 완료했습니다. `src/packaging/dependency_groups.py` 파일에서 다음 사항을 변경하였습니다:

1. `.utils._validate_regex`를 import 하여 PEP 625 `Name` 필드 검증 규칙을 재사용했습니다.
2. 공개 예외 `InvalidGroupName` (`ValueError` 하위 클래스)을 정의하고 `__all__`에 등록했습니다.
3. `_normalize_group_names` 내부에서 각 그룹 키를 검증하여, 규칙 위반 이름마다 `InvalidGroupName` 오류를 기존 다른 오류들과 함께 수집하도록 만들었습니다.
4. `DependencyGroupResolver.lookup()` 및 `resolve()` 메서드에서 정규화 처리 전에 입력값을 즉시 검증하고, 위반 시 나머지 처리 없이 단일 `InvalidGroupName` 예외를 던지도록 수정했습니다.

기존의 정규화, 중복 검사, 순환 검사 등 기존 동작은 전혀 변경되지 않았습니다.