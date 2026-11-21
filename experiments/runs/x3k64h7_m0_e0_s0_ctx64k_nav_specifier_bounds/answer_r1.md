`src/packaging/specifiers.py`의 `SpecifierSet` 클래스에 `bounds()` 메서드를 추가했습니다.

주요 변경 사항:
- `bounds()` 메서드 추가: `(lower, upper)` 튜플 반환 (각각 `None` 또는 `(Version, inclusive: bool)`)
- `===` specifier가 있으면 `ValueError` 발생
- 빈 `SpecifierSet`은 `(None, None)` 반환
- 모든 연산자 처리: `>=`, `>`, `<=`, `<`, `==` (와일드카드 포함), `~=`, `!=` (경계 없음)
- 와일드카드 `==V.*`의 upper는 마지막 release 숫자를 1 증가시켜 계산
- `~=V`의 upper는 마지막 release 숫자를 제거한 후 새로운 마지막 숫자를 1 증가시켜 계산
- 버전이 같은 경우 `inclusive=False`가 `inclusive=True`보다 우선 (더 제한적인 경계 선택)
- 여러 specifier의 경계는 합쳐서 가장 큰 lower와 가장 작은 upper를 반환