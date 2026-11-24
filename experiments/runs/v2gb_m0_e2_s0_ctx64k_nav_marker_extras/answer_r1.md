다음과 같이 수정했습니다.

1. **`src/packaging/markers.py`**
   - `NormalizedName` import 추가.
   - 마커 트리를 순회하여 `extra` 변수 비교(`==`, `!=`) 및 `extras` 집합 멤버십(`in`, `not in`)에 등장하는 extra 이름을 수집하는 `_referenced_extras` 및 `_collect_referenced_extras` 헬퍼 함수 추가.
   - `Marker` 클래스에 `referenced_extras()` 메서드 추가.

2. **`src/packaging/requirements.py`**
   - `NormalizedName` import 추가.
   - `Requirement` 클래스에 `marker_extras` 속성(property) 추가 (마커가 없으면 빈 `frozenset`, 있으면 `marker.referenced_extras()` 결과 반환).