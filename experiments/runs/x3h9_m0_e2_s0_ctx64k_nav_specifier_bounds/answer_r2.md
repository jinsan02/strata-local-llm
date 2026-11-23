수정 사항을 요약하면:
1. `src/packaging/specifiers.py` import 문에 `_next_prefix_dev0`를 추가했다.
2. `SpecifierSet` 클래스에 `bounds()` 메서드를 구현했다. 각 연산자(`>=`, `>`, `<=`, `<`, `==`, `~=`, `!=`, `==V.*`)의 경계 규칙을 적용하고, 여러 specifier의 하한/상한을 합성한다(하한은 최대, 상한은 최소, 동일 버전 시 비포함 `inclusive=False`가 우선). 빈 집합은 `(None, None)`을 반환하며, `===` 연산자가 포함되면 `ValueError`를 던진다.