### 변경 내용 요약

**`src/packaging/markers.py`**
- `Marker.referenced_extras()`: 마커 트리를 재귀적으로 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras` 등에서 쓰인 모든 extra 이름을 정규화해 `frozenset`으로 반환.
- `Marker._collect_extras()`: 위 메서드의 구현을 담은 정적 헬퍼 메서드.

**`src/packaging/requirements.py`**
- `Requirement.marker_extras`: 마커가 없으면 빈 `frozenset`, 있으면 `marker.referenced_extras()` 결과를 반환하는 property 추가.

기존 동작(문자열화, 비교, 해시, 평가)은 전혀 변경하지 않았습니다.