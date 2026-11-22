수정 완료. 변경 사항을 요약하면:

1. **`src/packaging/markers.py`**:
   - `NormalizedName` import 추가
   - `Marker.referenced_extras()` 메서드 추가: 마커 트리를 재귀적으로 탐색하여 `extra == "x"`, `"x" == extra`, `extra != "x"`, `"x" in extras`, `"x" not in extras` 등의 형태로 쓰인 모든 extra 이름을 정규화된 이름으로 모아 `frozenset[NormalizedName]`로 반환. `and`/`or` 조합과 괄호 중첩도 처리. `dependency_groups` 등 다른 변수는 제외.
   - 내부 보조 메서드 `_collect_referenced_extras()` 추가

2. **`src/packaging/requirements.py`**:
   - `NormalizedName` import 추가
   - `Requirement.marker_extras` property 추가: 마커가 없으면 빈 `frozenset`, 있으면 `self.marker.referenced_extras()` 결과 반환