`packaging.markers.Marker`에 `referenced_extras()` 메서드를, `packaging.requirements.Requirement`에 `marker_extras` 속성을 추가했습니다.

**주요 변경 사항:**

1. **`src/packaging/markers.py`**:
   - `NormalizedName` 타입을 `.utils`에서 임포트했습니다.
   - 마커 트리를 재귀적으로 순회하며 `extra` 변수 비교(`==`, `!=`) 및 `extras` 집합 멤버십(`in`, `not in`)에 사용된 모든 extra 이름을 정규화하여 수집하는 `_get_referenced_extras()` 도우미 함수를 추가했습니다.
   - `Marker` 클래스에 `referenced_extras()` 메서드를 추가하여 수집된 extra 이름들을 `frozenset`으로 반환하도록 했습니다.

2. **`src/packaging/requirements.py`**:
   - `NormalizedName` 타입을 `.utils`에서 임포트했습니다.
   - `Requirement` 클래스에 `marker_extras` 속성을 추가했습니다. 마커가 없으면 빈 `frozenset`을, 있으면 해당 마커의 `referenced_extras()` 결과를 반환합니다.