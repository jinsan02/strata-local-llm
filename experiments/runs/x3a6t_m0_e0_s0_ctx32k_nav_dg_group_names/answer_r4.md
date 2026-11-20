### 변경 내용 요약
`src/packaging/dependency_groups.py` 파일에서 다음 네 가지 수정을 적용했습니다:

1. **필요한 정규식 임포트**: `from .utils import _validate_regex` 추가하여 코어 메타데이터 `Name` 필드 검증 규칙을 재사용합니다.
2. **공개 예외 클래스 및 export 추가**: `InvalidGroupName(ValueError)` 예외 클래스를 정의하고, `__all__` 목록에 포함시켰습니다.
3. **`DependencyGroupResolver.__init__` 내 검증 로직 (`_normalize_group_names`)**: 그룹 이름마다 `_validate_regex.fullmatch()` 검사를 수행합니다. 규칙을 지키지 않는 경우 해당 이름을 `repr` 형태로 담은 `InvalidGroupName` 인스턴스를 생성해 기존 중복 오류 등과 함께 `_ErrorCollector`에 한꺼번에 수집한 뒤, 최종적으로 `ExceptionGroup`으로 보고하도록 수정했습니다.
4. **`lookup()` 및 `resolve()` 초기 검증**: 두 메서드 내부에서 정규화(`_normalize_name`)나 캐시 조회보다 먼저 `_validate_regex.fullmatch()` 검사를 수행합니다. 이름을 만족하지 않으면 즉시 단일 `InvalidGroupName` 예외를 던지도록 했습니다.

기존의 정규화, 중복 검사, 순환 검사 및 포함(include) 처리 로직은 변경되지 않았습니다.