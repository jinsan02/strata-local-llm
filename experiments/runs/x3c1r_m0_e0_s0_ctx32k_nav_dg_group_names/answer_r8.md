수정을 완료했습니다. 변경 내용은 다음과 같습니다:

1. `src/packaging/dependency_groups.py` 수정
   - core metadata `Name` 필드 규칙과 동일한 `_group_name_regex` 정규식 정의
   - `InvalidGroupName(ValueError)` 공개 예외 클래스 추가 및 `__all__` 등록
   - `_normalize_group_names()` 내 그룹 이름 검증 로직 추가: 유효하지 않은 이름을 발견할 때마다 `InvalidGroupName`을 생성해 기존 오류 수집기(`_ErrorCollector`)로 모음 (한 번의 ExceptionGroup으로 함께 보고)
   - `DependencyGroupResolver.lookup()` 및 `resolve()` 시작 부분에 인자 이름 검증 로직 추가: 규칙 위반 시 `InvalidGroupName` 단일 예외를 즉시 던짐
2. 메시지에는 원래 그룹 이름을 `repr` 형태(`!r`)로 포함
3. 기존 테스트 파일은 수정하지 않았으며, 정규화·중복 검사·순환 검사 등 기존 동작은 변경 없음