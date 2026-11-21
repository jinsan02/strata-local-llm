수정을 완료했습니다. `src/packaging/dependency_groups.py` 파일에서 다음 사항을 변경했습니다:

1. `InvalidGroupName` 예외 클래스 추가 (`ValueError` 하위 클래스).
2. `__all__`에 `InvalidGroupName` 추가.
3. `packaging.utils`의 `canonicalize_name`과 `InvalidName`을 임포트하여 기존 `Name` 필드 검증 규칙을 재사용.
4. `_normalize_group_names` 함수에 이름 유효성 검사 로직 추가 (기존 중복 이름 오류와 함께 `ExceptionGroup`으로 수집).
5. `lookup()` 및 `resolve()` 메서드에서 전달된 이름이 유효하지 않으면 즉시 `InvalidGroupName` 예외를 던지도록 수정.