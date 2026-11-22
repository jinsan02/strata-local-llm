### 변경 사항 요약

`src/packaging/specifiers.py` 파일에 다음 내용을 추가했습니다:

1.  **보조 함수 추가**:
    *   `_wildcard_upper(version)`: `==V.*`의 상한을 계산합니다 (예: `1.2.*` → `1.3`).
    *   `_compatible_upper(version)`: `~=V`의 상한을 계산합니다 (예: `~=1.4.5` → `1.5`).

2.  **`SpecifierSet.bounds()` 메서드 추가**:
    *   모든 specifier의 경계를 합산하여 `(lower, upper)` 튜플을 반환합니다.
    *   각 경계는 `None`이거나 `(Version, inclusive)` 형태입니다.
    *   경계 비교 시 `LowerBound`/`UpperBound` 클래스를 사용하여 동일 버전에서 `inclusive=False`가 더 엄격하게 적용되도록 처리했습니다.
    *   `===` 연산자가 포함된 경우 `ValueError`를 발생시킵니다.