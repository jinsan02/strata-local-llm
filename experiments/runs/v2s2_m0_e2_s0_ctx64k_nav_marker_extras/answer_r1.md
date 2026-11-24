수정 내용을 요약하면:

1. **`src/packaging/markers.py`**:
   - `from .utils import canonicalize_name` → `from .utils import NormalizedName, canonicalize_name`로 import 추가
   - `Marker` 클래스에 `referenced_extras()` 메서드 추가: 마커 트리를 재귀적으로 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras`, `"x" not in extras` 등의 비교에서 extra 이름을 정규화하여 `frozenset[NormalizedName]`로 반환
   - 보조 메서드 `_collect_extras()` 추가: 마커 트리를 재귀적으로 탐색하여 extra 이름을 집합에 수집

2. **`src/packaging/requirements.py`**:
   - `from .utils import canonicalize_name` → `from .utils import NormalizedName, canonicalize_name`로 import 추가
   - `Requirement` 클래스에 `marker_extras` property 추가: 마커가 없으면 빈 `frozenset`, 있으면 `self.marker.referenced_extras()` 결과 반환