`src/packaging/dependency_groups.py` 파일에 다음 수정을 완료했습니다:

1.  **`InvalidGroupName` 예외 클래스 추가**: `ValueError` 하위 클래스로 정의하고 `__all__`에 등록했습니다.
2.  **검증 로직 통합**: `packaging.utils`의 `_validate_regex`를 import하여 기존 정규식 구현을 재사용했습니다.
3.  **`_normalize_group_names` 수정**: 그룹 이름이 유효한지 검사하여 `InvalidGroupName`을 기존 오류 수집기에 추가했습니다.
4.  **`lookup()`, `resolve()` 수정**: 입력된 그룹 이름이 유효한지 즉시 검사하고, 유효하지 않으면 `InvalidGroupName`을 단일 예외로 던지도록 했습니다.

기존의 정규화, 중복 검사, 순환 검사 등 기존 동작은 변경되지 않았습니다.