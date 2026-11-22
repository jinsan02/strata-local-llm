`packaging.markers.Marker` 클래스에 `referenced_extras()` 메서드와 `packaging.requirements.Requirement` 클래스에 `marker_extras` 속성(property)를 추가했습니다.

주요 수정 사항:
- `src/packaging/markers.py`: `NormalizedName` import 추가, `_collect_extras` 재귀 수집 함수 추가, `Marker.referenced_extras()` 메서드 구현.
- `src/packaging/requirements.py`: `NormalizedName` import 추가, `Requirement.marker_extras` property 구현.

기존 동작(문자열화, 비교, 해시, 평가)은 변경되지 않았습니다.