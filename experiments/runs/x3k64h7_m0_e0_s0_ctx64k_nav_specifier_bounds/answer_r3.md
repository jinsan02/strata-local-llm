수정 사항을 요약하면:

**`src/packaging/specifiers.py`** — `SpecifierSet` 클래스에 `bounds()` 메서드 추가 (약 120줄)

- `bounds()` 메서드는 `(lower, upper)` 튜플을 반환하며, 각 요소는 `None` 또는 `(Version, inclusive: bool)`
- 각 연산자별 경계:
  - `>=V` → lower `(V, True)`
  - `>V` → lower `(V, False)`
  - `<=V` → upper `(V, True)`
  - `<V` → upper `(V, False)`
  - `==V` → lower `(V, True)`, upper `(V, True)`
  - `==V.*` → lower `(V, True)`, upper `(last_digit_incremented, False)` (epoch 유지, pre/post/dev/local 없음)
  - `~=V` → lower `(V, True)`, upper `(prefix_last_digit_incremented, False)` (epoch 유지, pre/post/dev/local 없음)
  - `!=V` → 경계 없음
- 여러 specifier 의 경계는 합침: lower 는 가장 큰 것, upper 는 가장 작은 것. 버전이 같을 때 `inclusive=False` 가 승리
- `===` 가 있으면 `ValueError`
- 빈 `SpecifierSet` 은 `(None, None)`