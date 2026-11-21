수정 사항을 요약하면 다음과 같습니다:

1. **`src/packaging/markers.py`**:
   - `NormalizedName` 타입과 `MarkerVar` 타입을 import에 추가
   - `Marker` 클래스에 `referenced_extras()` 메서드 추가: 마커 트리를 재귀적으로 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras` 등의 비교에서 언급된 extra 이름을 정규화된 이름으로 `frozenset` 에 모아 반환
   - `Marker` 클래스에 `_collect_referenced_extras()` 및 `_collect_extras_from_atom()` 보조 메서드 추가 (재귀 순회 로직)

2. **`src/packaging/requirements.py`**:
   - `Requirement` 클래스에 `marker_extras` property 추가: 마커가 없으면 빈 `frozenset`, 있으면 `self.marker.referenced_extras()` 결과 반환

기존 동작(문자열화, 비교, 해시, 평가)은 변경되지 않았습니다.