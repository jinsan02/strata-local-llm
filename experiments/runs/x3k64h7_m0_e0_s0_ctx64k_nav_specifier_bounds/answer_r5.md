수정을 마쳤습니다. 다음을 변경했습니다:

1. **보조 함수 3개 추가** (`InvalidSpecifier` 클래스 앞에):
   - `_upper_wildcard(version)`: `==V.*` 의 upper bound (마지막 release 숫자 +1)
   - `_upper_compatible(version)`: `~=V` 의 upper bound (마지막 release digit 버리고 전 digit +1)
   - `_specifier_bounds(op, ver_str, version)`: 단일 specifier 의 `(lower, upper)` 반환
   - `_merge_bounds(current, new, is_lower)`: 두 bound 병합 (동일 버전이면 exclusive 가 승)

2. **`SpecifierSet.bounds()` 메서드 추가**:
   - `===` 가 있으면 `ValueError` 던짐
   - 빈 `SpecifierSet` 은 `(None, None)` 반환
   - 모든 specifier 의 경계를 합산 (lower 는 최대, upper 는 최소, 동일 버전 시 exclusive 우선)