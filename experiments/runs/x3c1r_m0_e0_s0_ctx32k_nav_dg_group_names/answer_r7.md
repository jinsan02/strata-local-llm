수정 완료. 적용한 변경 사항 요약:

1. **`src/packaging/dependency_groups.py`**
   - `packaging.utils._validate_regex`를 import 하여 그룹 이름 검증 규칙으로 사용했다. 새 정규식을 만들지 않았다.
   - `InvalidGroupName(ValueError)` 예외 클래스를 정의하고 `__all__`에 추가했다.
   - `_normalize_group_names()` 함수에서 각 키(`group_name`)가 정규식에 맞는지 검사한다. 위반 시 `InvalidGroupName`을 `_ErrorCollector`에 기록하여 기존 중복 이름 오류 등 함께 `ExceptionGroup`으로 한꺼번에 보고하도록 했다. 메시지에는 원래 이름이 `repr` 형태로 포함된다.
   - `DependencyGroupResolver.lookup()` 과 `resolve()` 메서드에서 입력받은 그룹 이름이 규칙에 맞지 않으면 정규화(`_normalize_name`) 전에 즉시 `InvalidGroupName` 단일 예외를 던지도록 했다.
   - 기존 정규화, 중복 검사, 순환 검사 등 나머지 로직은 그대로 유지했다. 테스트 파일은 수정하지 않았다.