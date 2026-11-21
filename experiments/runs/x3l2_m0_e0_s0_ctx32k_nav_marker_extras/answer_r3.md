수정 내용을 요약하면:

1. **`src/packaging/markers.py`**:
   - `utils`에서 `NormalizedName` import 추가
   - `Marker` 클래스에 `referenced_extras()` 메서드 추가: `_markers` 트리를 재귀적으로 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras`, `"x" not in extras` 형태의 비교에서 extra 이름을 정규화하여 `frozenset[NormalizedName]`로 반환
   - 내부 보조 메서드 `_collect_referenced_extras()` 추가

2. **`src/packaging/requirements.py`**:
   - `Requirement` 클래스에 `marker_extras` property 추가: 마커가 없으면 빈 `frozenset()`, 있으면 `self.marker.referenced_extras()` 결과 반환