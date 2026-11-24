수정을 완료했습니다. `SpecifierSet` 클래스에 `bounds()` 메서드를 추가했습니다.

**변경 내용 요약:**

`src/packaging/specifiers.py` 의 `SpecifierSet` 클래스에 `bounds()` 메서드 추가 (약 100줄):

- `===` specifier 가 있으면 `ValueError` 발생
- 각 specifier 의 연산자에 따라 lower/upper 경계 계산:
  - `>=V` → lower `(V, True)`
  - `>V` → lower `(V, False)`
  - `<=V` → upper `(V, True)`
  - `<V` → upper `(V, False)`
  - `==V` (비와일드카드) → lower `(V, True)`, upper `(V, True)`
  - `==V.*` → lower `(V, True)`, upper `(V의 release 마지막+1, False)` (epoch 유지)
  - `~=V` → lower `(V, True)`, upper `(prefix_last+1, False)` (epoch 유지, pre/post/dev/local 없음)
  - `!=V` → 경계 영향 없음
- 여러 specifier 의 경계는 합침: lower 는 max, upper 는 min. 버전이 같으면 `inclusive=False` 쪽이 승리
- 빈 `SpecifierSet` → `(None, None)`