수정 완료. 변경 내용 요약:

- `src/packaging/dependency_groups.py`:
  - `InvalidGroupName` 예외 클래스 추가 (`ValueError` 하위)
  - `__all__`에 `"InvalidGroupName"` 추가
  - `utils.canonicalize_name` import
  - `_normalize_group_names()`: 그룹 이름 유효성 검사 추가 → 실패 시 `InvalidGroupName`을 `_ErrorCollector`에 추가 (기존 중복 오류와 함께 `ExceptionGroup`으로 한꺼번 보고)
  - `DependencyGroupResolver.__init__()`: 기존 동작 유지
  - `lookup()`, `resolve()`: 이름 유효성 검사 후 실패 시 `InvalidGroupName` 단일 예외 즉시 던짐