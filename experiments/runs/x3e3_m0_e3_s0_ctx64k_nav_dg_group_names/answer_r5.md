수정 완료. 변경 내용을 요약하면 다음과 같습니다.

- `src/packaging/dependency_groups.py`
  - `__all__`에 `InvalidGroupName` 추가.
  - `InvalidGroupName(ValueError)` 예외 클래스 정의.
  - `packaging.utils._validate_regex` 임포트하여 핵심 메타데이터 `Name` 필드 검증 규칙 재사용.
  - `_normalize_group_names` 함수에서 그룹 키 순회 시 `_validate_regex.fullmatch()` 검증 추가. 규칙 위반 시 `InvalidGroupName`을 생성해 `_ErrorCollector`에 수집 (중복 이름 오류 등 기존 오류와 동일한 방식으로 `ExceptionGroup`으로 통합 보고).
  - `DependencyGroupResolver.lookup()` 및 `resolve()` 메서드 시작 부분에 입력 문자열 검증 추가. 규칙 위반 시 정규화나 캐시 조회 등 다른 처리 없이 `InvalidGroupName`을 단일 예외로 즉시 던짐.
  - 기존 이름 정규화, 중복 검사, include 순환 검사 등 핵심 동작은 변경 없음.