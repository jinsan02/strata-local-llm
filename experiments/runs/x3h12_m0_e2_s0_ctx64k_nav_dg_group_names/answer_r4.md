`src/packaging/dependency_groups.py` 파일에 다음 내용을 수정했습니다:

1. `utils._validate_regex` 임포트 추가
2. `InvalidGroupName` 예외 클래스 정의 (`ValueError` 하위)
3. `__all__` 에 `InvalidGroupName` 추가
4. `_normalize_group_names` 함수에서 그룹 이름 유효성 검사하여 `InvalidGroupName` 오류 수집 (중복 이름 오류와 함께 `ExceptionGroup` 발생)
5. `lookup()`, `resolve()` 메서드 시작 부분에서 `_check_group_name(group)` 호출하여 즉시 단일 예외 던지기