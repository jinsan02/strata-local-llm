`src/packaging/specifiers.py`의 `SpecifierSet` 클래스에 `bounds()` 메서드를 추가했습니다.

주요 변경 사항:
- `bounds()` 메서드 구현: `(lower, upper)` 튜플 반환. 각 경계는 `None` 또는 `(Version, inclusive: bool)` 형태.
- 모든 연산자(`>=`, `>`, `<=`, `<`, `==`, `==*`, `~=`, `!=`)에 대한 경계 계산 로직 포함.
- 여러 specifier의 경계는 합침: lower는 가장 큰 값, upper는 가장 작은 값. 버전이 같으면 `inclusive=False`를 우선 적용.
- `===` 연산자가 있으면 `ValueError` 발생.
- 빈 `SpecifierSet`은 `(None, None)` 반환.
- `prereleases` 설정은 결과에 영향을 주지 않음.

기존 테스트(`run_tests`)는 모두 통과했습니다.