`src/packaging/dependency_groups.py` 파일에 다음과 같은 수정을 적용했습니다:

1. `utils` 모듈에서 `InvalidName`, `canonicalize_name`을 import했습니다.
2. `InvalidGroupName` 예외 클래스를 정의하고(`ValueError` 하위 클래스), `__all__`에 추가했습니다.
3. `DependencyGroupResolver.__init__`에서 `dependency_groups`의 모든 키에 대해 `canonicalize_name(..., validate=True)`를 호출하여 유효하지 않은 이름을 `InvalidGroupName` 예외로 수집하고, 기존 오류(중복 이름 등)와 함께 `ExceptionGroup`으로 보고합니다.
4. `lookup()`과 `resolve()` 메서드에서 전달받은 그룹 이름에 대해 유효성 검사를 수행하고, 실패 시 `InvalidGroupName`을 단일 예외로 즉시 던지도록 수정했습니다.
5. 기존 정규화 로직(`_normalize_name`)은 내부적으로 유지되었으며, 공개 API(`lookup`, `resolve`)와 생성자에서만 검증 로직이 적용됩니다.