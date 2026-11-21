`src/packaging/specifiers.py` 파일에 다음 내용을 추가/수정했습니다:

1. `Specifier` 클래스 정의 앞에 `_combine_lower`, `_combine_upper`, `_wildcard_upper`, `_tilde_upper` 헬퍼 함수를 추가했습니다.
2. `SpecifierSet` 클래스에 `bounds()` 메서드를 추가했습니다. 이 메서드는 `===` 연산자가 포함되면 `ValueError`를 던지고, 나머지 연산자에 대해 하한(lower)과 상한(upper)을 계산한 후 결합 로직을 적용해 `(lower, upper)` 튜플로 반환합니다. 빈 집합은 `(None, None)`을 반환합니다.
3. 버전이 동일한 경우 `inclusive=False`가 우선하도록 결합 함수를 구현했으며, 와일드카드(`.*`)와 `~=` 연산자의 상한 계산 시 epoch는 유지하고 pre/post/dev/local은 제거하도록 처리했습니다.

수정이 완료되었습니다.