수정 완료. 변경 내용 요약:

1. **`src/packaging/markers.py`**:
   - `from .utils import NormalizedName, canonicalize_name` import 추가
   - `Marker.referenced_extras()` 메서드 추가: 마커 트리를 재귀적으로 순회하며 `extra` 또는 `extras` 변수와 비교되는 모든 extra 값을 정규화하여 `frozenset[NormalizedName]`로 반환
   - 내부 보조 정적 메서드 `_collect_referenced_extras()` 추가: `Variable('extra')`/`Variable('extras')`가 LHS 또는 RHS에 있고 다른 쪽이 `Value`인 경우 정규화된 이름을 수집

2. **`src/packaging/requirements.py`**:
   - `from .utils import NormalizedName, canonicalize_name` import 추가
   - `Requirement.marker_extras` property 추가: 마커가 없으면 빈 `frozenset`, 있으면 `marker.referenced_extras()` 결과 반환