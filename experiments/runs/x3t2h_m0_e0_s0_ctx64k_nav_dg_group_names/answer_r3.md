수정 내용을 요약하면 다음과 같습니다.

**파일: `src/packaging/dependency_groups.py`**

1.  **`InvalidGroupName` 예외 클래스 추가**: `ValueError`의 하위 클래스로 새로운 공개 예외를 정의했습니다.
2.  **`__all__` 수정**: `InvalidGroupName`을 모듈의 공개 인터페이스에 추가했습니다.
3.  **정규식 import**: `packaging.utils`에서 `Name` 필드 검증에 사용하는 `_validate_regex`를 가져왔습니다.
4.  **`DependencyGroupResolver.__init__` 동작 수정**: `_normalize_group_names` 함수 내에서 그룹 이름이 유효한지 검사하여, 규칙에 맞지 않으면 기존 오류(중복 등)와 같은 `_ErrorCollector` 방식(함께 보고)으로 `InvalidGroupName`을 추가합니다.
5.  **`lookup` 및 `resolve` 메서드 수정**: 입력된 그룹 이름이 유효하지 않으면 정규화나 다른 처리 전에 즉시 `InvalidGroupName` 예외를 던지도록 했습니다.