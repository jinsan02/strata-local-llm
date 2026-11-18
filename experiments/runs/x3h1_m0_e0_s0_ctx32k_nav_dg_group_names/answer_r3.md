수정 완료. 다음 사항을 변경함:

- `src/packaging/dependency_groups.py`
  - `.utils` 모듈 임포트 추가
  - `InvalidGroupName(ValueError)` 예외 클래스 정의 및 `__all__` 등록
  - `_normalize_group_names`에서 그룹 이름 검증을 위해 `utils.canonicalize_name(…, validate=True)` 사용, 실패 시 `InvalidGroupName` 오류 수집 (중복 등 다른 오류와 동등하게 처리)
  - `DependencyGroupResolver.lookup()`과 `resolve()`에서 이름을 정규화하기 전에 즉시 검증하고, 유효하지 않으면 단일 `InvalidGroupName` 예외를 던지도록 수정