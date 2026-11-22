수정 사항을 요약하면:

1. **`src/packaging/markers.py`**:
   - `MarkerVar`, `NormalizedName` import 추가
   - `Marker.referenced_extras()` 메서드 추가: 마커 트리를 재귀적으로 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras`, `"x" not in extras` 형태에서 extra 이름을 정규화하여 `frozenset[NormalizedName]`로 반환
   - `_collect_extras()` 정적 메서드 추가: 재귀 순회 로직 담당 (list는 재귀, tuple은 연산자 좌변/우변이 Variable("extra") 또는 Variable("extras")인지 확인)

2. **`src/packaging/requirements.py`**:
   - `NormalizedName` import 추가
   - `Requirement.marker_extras` property 추가: marker가 없으면 빈 `frozenset()`, 있으면 `self.marker.referenced_extras()` 반환