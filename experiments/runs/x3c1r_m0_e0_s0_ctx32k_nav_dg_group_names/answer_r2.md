수정 완료. 변경 사항을 요약하면 다음과 같습니다:

1. `src/packaging/dependency_groups.py`에 `InvalidGroupName(ValueError)` 예외 클래스를 추가하고 `__all__`에 등록했습니다.
2. `.utils.canonicalize_name(..., validate=True)`와 `.utils.InvalidName`을 임포트하여 PEP 735 그룹 이름 검증에 기존 `Name` 필드 규칙을 재사용했습니다. 새 정규식을 만들지 않았습니다.
3. `_normalize_group_names()` 함수에서 각 그룹 이름을 검증합니다. 유효하지 않은 이름은 `_ErrorCollector`를 통해 `InvalidGroupName` 예외로 수집하며, 메시지에는 `utils.py`의 구현에 따라 원래 이름이 `repr` 형태로 포함됩니다. (기존 중복 검사 로직과는 별개로 동작하여 기존 동작을 해치지 않습니다.)
4. `DependencyGroupResolver.lookup()` 및 `resolve()` 메서드에서 무효한 그룹 이름이 전달되면, 정규화나 캐시 확인 등 다른 처리 전에 즉시 `InvalidGroupName` 예외를 던지도록 수정했습니다.
5. 그 외 기존 정규화, 중복 검사, include 처리, 순환 검사 로직은 전혀 변경하지 않았습니다. 기존 테스트 파일도 건드리지 않았습니다. 

필요한 추가 편집 블록은 없으며 작업이 완료되었습니다.