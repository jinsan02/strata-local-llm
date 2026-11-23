`src/packaging/specifiers.py` 파일에 다음 내용을 수정했습니다.

1.  **보조 함수 추가**:
    *   `_specifier_bounds(spec)`: 개별 `Specifier`의 하한/상한 경계를 `(Version, bool)` 튜플로 반환합니다. `===` 연산자는 `ValueError`를 던집니다.
    *   `_max_lower(a, b)`, `_min_upper(a, b)`: 두 경계 중 더 큰(또는 더 작은) 것을 선택하며, 버전이 같을 때는 `inclusive=False`가 더 큰(또는 더 작은) 것으로 처리합니다.
    *   `_next_prefix_version`, `_compatible_upper`: 와일드카드와 `~=` 연산자의 상한 버전을 계산합니다.

2.  **`SpecifierSet.bounds()` 메서드 추가**:
    *   클래스 내의 `bounds()` 메서드를 구현했습니다.
    *   빈 세트는 `(None, None)`을 반환합니다.
    *   `===`가 포함된 경우 `ValueError`를 던집니다.
    *   모든 specifier의 경계를 집계하여 `(lower, upper)` 튜플을 반환합니다.