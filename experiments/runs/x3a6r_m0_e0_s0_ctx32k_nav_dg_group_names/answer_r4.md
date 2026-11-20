수정 완료. 변경 내용 요약:

- **`dependency_groups.py`**:
  - `.utils._validate_regex` import 추가
  - `InvalidGroupName(ValueError)` 예외 클래스 정의 및 `__all__` 등록
  - `_normalize_group_names()`: 그룹 이름 검증 로직(`_validate_regex.fullmatch`) 추가, 유효하지 않은 이름마다 `InvalidGroupName` 발생 (기존 중복 검사 등 오류와 같은 방식으로 `_ErrorCollector`에 쌓임)
  - `_validate_group_name()` 헬퍼 함수 정의
  - `DependencyGroupResolver.lookup()`, `resolve()`: 정규화 전에 `_validate_group_name()` 호출하여 단일 예외 즉시 던짐