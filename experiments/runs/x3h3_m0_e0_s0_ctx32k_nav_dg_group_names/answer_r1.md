`src/packaging/dependency_groups.py` 파일에 다음 사항을 수정했습니다.

1. **가져오기 추가**: `.utils` 모듈에서 `InvalidName`, `canonicalize_name`을 가져와 PEP 503 / Core Metadata `Name` 규칙 검증에 활용하도록 했습니다.
2. **공개 예외 클래스 추가**: `class InvalidGroupName(ValueError)`를 정의하고 `__all__` 에 등록했습니다.
3. **초기화 시 누적 검증 (`__init__`)**: `_normalize_group_names` 함수에서 그룹 키를 처리할 때 `canonicalize_name(key, validate=True)`를 사용했습니다. 유효하지 않은 이름이 나오면 `_ErrorCollector`에 `InvalidGroupName(f"invalid group name: {key!r}")`을 누적으로 보고하여 기존 중복 에러와 같은 방식으로 한꺼번에 제출합니다.
4. **`lookup()` / `resolve()` 즉시 던지기**: 두 메서드 모두 입력 인자를 정규화하기 전에 `canonicalize_name(..., validate=True)`로 검증합니다. 규칙 위반 시 별도의 Collector 없이 `InvalidGroupName(f"invalid group name: {arg!r}")`을 단일 예외로 바로 raise 합니다.
5. **기존 동작 보존**: 그룹 내부의 `include-group` 참조 및 순환/중복 검사 로직은 기존 `_normalize_name` 함수와 에러 수집 방식을 그대로 유지하여 수정하지 않았습니다.