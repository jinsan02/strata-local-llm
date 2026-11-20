### 변경 내용 요약

1. **`src/packaging/markers.py`**
   - `NormalizedName` 타입을 `utils`에서 import.
   - `Marker.referenced_extras()` 메서드 추가: 마커 트리를 재귀적으로 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras`, `"x" not in extras` 등에서 참조된 extra 이름을 정규화하여 `frozenset`으로 반환.
   - 내부 보조 메서드 `_collect_extras()` 추가.

2. **`src/packaging/requirements.py`**
   - `NormalizedName` 타입을 `utils`에서 import.
   - `Requirement.marker_extras` 속성(property) 추가: 마커가 없으면 빈 `frozenset`, 있으면 해당 마커의 `referenced_extras()` 결과를 반환.

기존 문자열화, 비교, 해시, 평가 로직은 변경하지 않았습니다.