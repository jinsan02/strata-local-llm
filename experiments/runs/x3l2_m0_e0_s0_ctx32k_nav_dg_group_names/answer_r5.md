`src/packaging/dependency_groups.py` 파일에 다음 사항을 수정했습니다:

1. `from .utils import _validate_regex` 임포트 추가 (기존 `Name` 필드 검증 정규식 재사용)
2. `__all__`에 `InvalidGroupName` 추가
3. `InvalidGroupName` 예외 클래스 정의 (`ValueError` 상속)
4. `_normalize_group_names` 함수에 그룹 이름 유효성 검사 로직 추가. 검사 실패 시 `errors.error()`로 기존 오류 수집기(`_ErrorCollector`)에 함께 쌓이도록 처리
5. `DependencyGroupResolver.lookup()` 및 `resolve()` 메서드 시작 부분에 유효성 검사 추가. 실패 시 `InvalidGroupName` 예외를 즉시 `raise`
6. 기존 정규화, 중복 검사, 포함(include) 및 순환 검사 로직은 그대로 유지

모든 요구사항을 충족하도록 수정 완료.