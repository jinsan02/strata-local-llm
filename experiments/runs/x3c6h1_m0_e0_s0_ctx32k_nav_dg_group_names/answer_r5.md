### 변경 내용 요약 (`src/packaging/dependency_groups.py`)
1. `packaging.utils._validate_regex` 임포트 추가.
2. `InvalidGroupName(ValueError)` 예외 클래스 생성 후 `__all__`에 등록.
3. `_normalize_group_names()` 함수 내 `dependency_groups` 키 순회 로직에 정규식 검사를 삽입하여, 규칙 위반 시 기존 `_ErrorCollector` 패턴과 동일하게 한꺼번에 수집되도록 수정 (메시지에 `repr` 원본 포함).
4. `DependencyGroupResolver.lookup()` 및 `resolve()` 메서드 상단에 입력값 유효성 검사 후 즉시 단일 `InvalidGroupName` 예외 던지기 로직 추가.
5. 기존 이름 정규화(`_normalize_name`), 중복 감지, `include-group` 순환 검사 등의 동작은 수정하지 않음.

수정 완료.