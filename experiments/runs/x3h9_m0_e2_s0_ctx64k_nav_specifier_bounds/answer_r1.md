`src/packaging/specifiers.py` 파일에 다음 내용을 추가했습니다:

1. **보조 함수 추가**:
   - `_upper_wildcard(version)`: `==V.*`의 upper bound를 계산 (마지막 release 숫자 +1).
   - `_upper_compatible(version)`: `~=V`의 upper bound를 계산 (마지막 release 숫자 제거 후 그 다음 숫자 +1).
   - `_max_lower_bound(current, new)`: 여러 lower bound 중 가장 큰(제한적인) 것을 선택. 버전이 같으면 `inclusive=False`가 승리.
   - `_min_upper_bound(current, new)`: 여러 upper bound 중 가장 작은(제한적인) 것을 선택. 버전이 같으면 `inclusive=False`가 승리.

2. **`SpecifierSet.bounds()` 메서드 추가**:
   - 각 specifier의 operator와 버전을 확인하여 lower/upper bound 튜플을 누적 결합합니다.
   - `===`가 포함된 경우 `ValueError`를 던집니다.
   - 빈 `SpecifierSet`은 `(None, None)`을 반환합니다.
   - `prereleases` 설정은 결과에 영향을 주지 않습니다.