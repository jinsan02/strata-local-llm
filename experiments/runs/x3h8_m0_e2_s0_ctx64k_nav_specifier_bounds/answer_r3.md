### 요구사항 확인

| 요구사항 | 반영 여부 | 비고 |
|---|---|---|
| `bounds()` 메서드 추가 | `specifiers.py:1423` | 완료 |
| 반환값 `(lower, upper)`, 각 `None` 또는 `(Version, bool)` | `specifiers.py:1425-1427` | 완료 |
| `>=V` → lower `(V, True)` | `specifiers.py:1467-1468` | 완료 |
| `>V` → lower `(V, False)` | `specifiers.py:1469-1470` | 완료 |
| `<=V` → upper `(V, True)` | `specifiers.py:1471-1472` | 완료 |
| `<V` → upper `(V, False)` | `specifiers.py:1473-1474` | 완료 |
| `==V` → lower/upper `(V, True)` | `specifiers.py:1480-1482` | 완료 |
| `==V.*` → lower `(V, True)`, upper `(next_prefix, False)` | `specifiers.py:1476-1479` | `_next_prefix` 사용 |
| `~=V` → lower `(V, True)`, upper `(next_prefix_compat, False)` | `specifiers.py:1483-1486` | `_next_prefix_for_compatible` 사용 |
| `!=V` → 경계 없음 | `specifiers.py:1487-1488` | 완료 |
| 와일드카드/`~=` upper: epoch 유지, release만, pre/post/dev/local 없음 | `_ranges.py:917-933` | `Version.from_parts(epoch=..., release=..., dev=0)` |
| 여러 specifier 경계 합치기: lower max, upper min, 동점 시 `inclusive=False` 승리 | `specifiers.py:1492-1516` | 완료 |
| 빈 `SpecifierSet` → `(None, None)` | `specifiers.py:1457-1458` | 완료 |
| 공집합 여부 무시 | `specifiers.py:1423-1520` | 범위 계산만 수행 |
| `===` 있으면 `ValueError` | `specifiers.py:1454-1455` | `_has_arbitrary` 체크 |
| prerelease 설정 영향 없음 | `specifiers.py:1423-1520` | `prereleases` 파라미터/속성 미사용 |
| 기존 테스트 2108개 통과 | `자동 검사` | 완료 |

모든 요구사항을 충족하며 기존 테스트도 통과함.