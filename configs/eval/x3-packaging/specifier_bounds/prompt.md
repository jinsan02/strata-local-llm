`packaging.specifiers.SpecifierSet` 에 메서드 `bounds()` 를 추가하라. 반환값은 `(lower, upper)` 튜플이고, 각각 `None`(제한 없음)이거나 `(Version, inclusive: bool)` 이다.

각 specifier 가 주는 경계 (`V` 는 specifier 의 버전):

| 연산자 | lower | upper |
| --- | --- | --- |
| `>=V` | `(V, True)` | — |
| `>V` | `(V, False)` | — |
| `<=V` | — | `(V, True)` |
| `<V` | — | `(V, False)` |
| `==V` (와일드카드 아님) | `(V, True)` | `(V, True)` |
| `==V.*` | `(V, True)` | release 의 마지막 숫자를 1 올린 버전, `False` |
| `~=V` | `(V, True)` | release 의 마지막 숫자를 버리고, 남은 마지막 숫자를 1 올린 버전, `False` |
| `!=V` | — | — |

- 와일드카드 · `~=` 의 upper 는 epoch 를 유지하고 release 숫자만으로 만든다(pre · post · dev · local 없음). 예: `==1.2.*` → `(1.2, True)`, `(1.3, False)` · `==1!2.*` → upper `1!3` · `~=1.4.5` → upper `1.5` · `~=2.2` → upper `3` · `~=1.4.5rc1` → lower `1.4.5rc1`, upper `1.5`.
- 여러 specifier 의 경계는 합친다: lower 는 가장 큰 것, upper 는 가장 작은 것. 버전이 같으면(`Version` 비교로 같음, 예: `2` 와 `2.0`) `inclusive=False` 쪽이 이긴다.
- 빈 `SpecifierSet` 은 `(None, None)`. 결과가 공집합인지는 따지지 않는다(예: `>2,<1` 도 그대로 반환).
- `===` 가 하나라도 있으면 `ValueError` 를 던진다.
- prerelease 설정은 결과에 영향을 주지 않는다. 기존 동작은 바뀌면 안 된다.
