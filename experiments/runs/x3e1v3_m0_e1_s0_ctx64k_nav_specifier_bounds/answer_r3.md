src/packaging/specifiers.py 파일에 다음 세 가지를 추가했습니다:

1. `Specifier._bounds()`: 단일 specifier 의 연산자(`>=`, `>`, `<=`, `<`, `==`, `~=`, `!=`) 에 따라 `(lower, upper)` 경계 튜플을 반환합니다. 와일드카드(`.*`) 와 `~=` 의 upper 는 release tuple 의 마지막 숫자를 기준으로 계산하며 epoch 는 유지합니다.
2. `SpecifierSet._compare_bounds()`: 두 경계를 비교해 더 엄격한 경계(하한은 최대, 상한은 최소, 버전이 같으면 `inclusive=False` 가 우세) 를 선택하는 헬퍼입니다.
3. `SpecifierSet.bounds()`: 모든 specifier 의 경계를 `_compare_bounds` 로 합쳐 `(lower, upper)` 튜플을 반환합니다. `===` 가 포함되면 `ValueError` 를 던지며, 빈 specifier set 은 `(None, None)` 을 반환합니다. 기존 테스트 파일은 수정하지 않았습니다.