`packaging.markers.Marker`에 `referenced_extras()` 메서드를, `packaging.requirements.Requirement`에 `marker_extras` 속성을 추가했습니다.

주요 변경 내용:
1. `src/packaging/markers.py`: 
   - `TYPE_CHECKING` 블록에 `NormalizedName` import 추가.
   - `Marker.referenced_extras()` 메서드 추가: 마커 트리를 재귀적으로 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras`, `"x" not in extras` 형태에서 extra 이름을 수집해 정규화된 `frozenset`으로 반환.
   - 내부 헬퍼 메서드 `_collect_extras()` 추가.
2. `src/packaging/requirements.py`:
   - `Requirement.marker_extras` 속성(property) 추가: 마커가 없으면 빈 `frozenset`, 있으면 `marker.referenced_extras()` 결과를 반환.

기존 문자열화, 비교, 해시, 평가 로직은 변경하지 않았으며 기존 테스트 파일도 수정하지 않았습니다. 작업이 완료되었습니다.