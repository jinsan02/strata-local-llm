`src/packaging/specifiers.py` 에 다음 내용을 추가했습니다.

1. `class SpecifierSet` 정의 앞에 `_next_prefix`, `_specifier_bounds`, `_pick_lower`, `_pick_upper` 헬퍼 함수를 추가했습니다.
2. `SpecifierSet` 클래스 내 `to_range()` 메서드 뒤에 `bounds()` 메서드를 구현했습니다.

구현 요약:
- 각 연산자(`>=`, `>`, `<=`, `<`, `==`, `==.*`, `~=`, `!=`) 에 맞춰 하한/상한을 `(Version, bool)` 또는 `None` 으로 반환합니다.
- `~=V` 와 `==V.*` 의 상한은 `epoch` 는 유지하고 `release` 의 마지막 숫자만 조작하여 생성합니다.
- 여러 specifier 가 있을 경우 `_pick_lower`/`_pick_upper` 로 가장 엄격한(최대 하한, 최소 상한) 경계로 합칩니다. 버전이 같으면 `inclusive=False` 가 우선합니다.
- `===` 가 하나라도 있으면 `ValueError` 를 던지며, 빈 집합은 `(None, None)` 을 반환합니다.
- 기존 `prereleases` 설정은 결과에 영향을 주지 않습니다.