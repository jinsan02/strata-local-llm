`packaging.markers.Marker`에 `referenced_extras()` 메서드를, `packaging.requirements.Requirement`에 `marker_extras` 속성을 추가했습니다.

**수정 파일:**
- `src/packaging/markers.py`: `Marker` 클래스에 `referenced_extras()` 메서드와 내부 순회를 돕는 `_extract_extras()` 정적 메서드 추가. `NormalizedName` import 추가.
- `src/packaging/requirements.py`: `Requirement` 클래스에 `marker_extras` property 추가. `NormalizedName` import 추가.