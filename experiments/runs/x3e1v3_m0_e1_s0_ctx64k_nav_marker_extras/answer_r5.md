`src/packaging/markers.py`에 `NormalizedName` import를 추가하고, `_referenced_extras` 및 `_collect_referenced_extras` 헬퍼 함수를 구현했다. `Marker` 클래스에 `referenced_extras()` 메서드를 추가했다.

`src/packaging/requirements.py`에 `NormalizedName` import를 추가하고, `Requirement` 클래스에 `marker_extras` 속성(property)을 추가했다.