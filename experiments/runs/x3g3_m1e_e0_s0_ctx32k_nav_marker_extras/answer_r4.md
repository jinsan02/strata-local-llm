수정 완료 후 결과를 요약합니다:

1. **`src/packaging/markers.py`**:
   - `NormalizedName` 타입을 `from .utils import NormalizedName`로 추가 import
   - `Marker` 클래스에 `referenced_extras()` 메서드 추가: 마커 트리를 재귀적으로 순회하며 `extra` 변수나 `extras` 변수와 비교되는 모든 extra 이름(Value)을 정규화된 이름으로 추출하여 `frozenset[NormalizedName]`로 반환

2. **`src/packaging/requirements.py`**:
   - `Requirement` 클래스에 `marker_extras` 속성(property) 추가: 마커가 없으면 빈 `frozenset`, 있으면 `self.marker.referenced_extras()` 결과 반환

구현 상세:
- `referenced_extras()`는 `_markers` 트리를 재귀적으로 탐색
- `Variable("extra")`가 좌변 또는 우변에 있고 다른 쪽이 `Value`인 경우: `Value.value`를 extra 이름으로 추출
- `Variable("extras")`가 좌변 또는 우변에 있고 다른 쪽이 `Value`인 경우: `Value.value`를 extra 이름으로 추출 ( `"x" in extras` 형태)
- 이미 `_normalize_extras`에서 extra 값이 정규화되므로 추출된 값은 그대로 정규화된 이름
- `and`/`or`로 연결된 마커나 괄호로 중첩된 식 전체를 재귀적으로 처리