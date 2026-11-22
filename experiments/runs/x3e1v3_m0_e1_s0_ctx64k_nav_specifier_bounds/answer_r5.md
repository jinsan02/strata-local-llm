`src/packaging/specifiers.py` 파일에 다음 내용을 수정했습니다:

1.  **헬퍼 함수 추가**: `bounds()` 메서드 구현에 필요한 `_next_wildcard_upper`, `_next_compatible_upper`, `_lower_bound_gt`, `_upper_bound_lt` 함수를 파일 상단에 추가했습니다.
2.  **`SpecifierSet.bounds()` 메서드 추가**: `SpecifierSet` 클래스에 요청된仕様に따라 경계를 계산하고 합치는 `bounds()` 메서드를 구현했습니다.
    *   `===` 연산자가 있으면 `ValueError`를 던집니다.
    *   각 연산자(`>=`, `>`, `<=`, `<`, `==`, `~=`, `!=`)에 따른 하한/상한 경계를 추출합니다.
    *   `==V.*`와 `~=V`의 상한은 epoch를 유지하고 release 숫자만 처리합니다.
    *   여러 specifier의 경계는 합쳐서 가장 큰 하한과 가장 작은 상한을 반환하며, 버전이 같을 때는 `inclusive=False`가 우선하도록 처리했습니다.
    *   빈 `SpecifierSet`은 `(None, None)`을 반환합니다.