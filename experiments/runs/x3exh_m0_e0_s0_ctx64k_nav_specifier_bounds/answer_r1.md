`src/packaging/specifiers.py`에 `SpecifierSet.bounds()` 메서드를 추가했습니다.

- `bounds()` 메서드: 모든 specifier의 경계를 순회하며 합산하고, `===`가 있으면 `ValueError`를 던집니다.
- `_specifier_bounds()`, `_wildcard_bounds()`: 단일 specifier의 하한/상한을 `(Version, bool)` 형태로 반환합니다.
- `_next_prefix_dev0()`: `~=V`나 `==V.*`의 상한을 계산하는 도우미입니다.
- `_max_bound()`, `_min_bound()`: 하한은 최대, 상한은 최소를 선택하며, 버전이 같으면 `inclusive=False`가 우선하도록 합니다.

이전 `edit_file` 도구 호출을 통해 이미 파일에 적용되었습니다.