수정을 마쳤습니다. 변경 내용을 요약하면 다음과 같습니다:

- `src/packaging/dependency_groups.py`:
  - `InvalidGroupName(ValueError)` 하위 클래스를 정의하고 `__all__`에 추가했습니다.
  - `.utils._validate_regex`를 import하여 메타데이터 `Name` 규칙 검증에 재사용했습니다.
  - `_normalize_group_names()`: 그룹 이름(키)이 정규식과 일치하지 않으면 `_ErrorCollector`에 `InvalidGroupName`을 추가하여 중복 이름 등 기존 오류와 함께 한꺼번에 보고하도록 수정했습니다. 메시지에는 원래 이름의 `repr` 값을 포함합니다.
  - `DependencyGroupResolver.lookup()` 및 `resolve()`: 이름을 정규화하기 전에 유효성을 검사합니다. 규칙에 맞지 않는 이름이 전달되면 나머지 처리 없이 `InvalidGroupName` 예외를 즉시 단일 예외로 던집니다.
  - 이름이 유효한 경우 기존 동작(정규화, 중복 검사, 순환 검사 등)은 영향을 받지 않습니다.