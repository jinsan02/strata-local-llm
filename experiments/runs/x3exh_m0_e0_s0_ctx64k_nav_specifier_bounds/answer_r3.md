수정 사항을 정리하면:

1. **`src/packaging/specifiers.py`**:
   - `_max_lower(a, b)`: 두 하한 중 더 높은(강한) 것을 반환. 버전이 같으면 `inclusive=False` 쪽이 승리.
   - `_min_upper(a, b)`: 두 상한 중 더 낮은(강한) 것을 반환. 버전이 같으면 `inclusive=False` 쪽이 승리.
   - `_next_prefix_release(version)`: 버전의 마지막 release 숫자를 1 올린 새 버전 생성 (dev/post/pre/local 없음). epoch는 유지.
   - `SpecifierSet.bounds()`: 모든 specifier의 경계를 합쳐 `(lower, upper)` 튜플로 반환. `===` 가 있으면 `ValueError`.

구현한 specifier별 매핑:
| 연산자 | lower | upper |
|---|---|---|
| `>=V` | `(V, True)` | — |
| `>V` | `(V, False)` | — |
| `<=V` | — | `(V, True)` |
| `<V` | — | `(V, False)` |
| `==V` | `(V, True)` | `(V, True)` |
| `==V.*` | `(V, True)` | `(next_prefix(V), False)` |
| `~=V` | `(V, True)` | `(next_prefix(V[:-1]), False)` |
| `!=V` | — | — |