수정 사항을 요약하면 다음과 같습니다.

1.  **`InvalidGroupName` 추가**: `src/packaging/dependency_groups.py`에 `ValueError` 하위 클래스인 `InvalidGroupName` 예외를 정의하고 `__all__`에 등록했습니다. 메시지에는 `repr` 형식의 이름을 포함합니다.
2.  **규칙 적용**: `packaging.utils`의 `_validate_regex`(코어 메타데이터 `Name` 필드 검증용)를 가져와서 사용합니다. 새 정규식을 작성하지 않았습니다.
3.  **초기화(`__init__`) 수정**: `_normalize_group_names` 함수에서 그룹 이름(키)을 검사하여 유효하지 않은 경우 `_ErrorCollector`에 `InvalidGroupName` 오류를 추가합니다. 이를 통해 중복 이름 오류 등 기존 오류와 동일한 방식으로 한꺼번에 보고됩니다.
4.  **`lookup()` 및 `resolve()` 수정**: 두 메서드 모두 입력 문자열이 정규식에 일치하는지 즉시 검사하고, 불일치 시 `InvalidGroupName`을 단일 예외로 던집니다. 이후 정규화(normalization) 과정은 유지됩니다.