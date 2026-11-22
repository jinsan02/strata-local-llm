다음 파일들을 수정했습니다:

- `src/packaging/markers.py`: `Marker` 클래스에 `referenced_extras()` 메서드를 추가했습니다. 마커 트리를 재귀적으로 순회하여 `extra` 또는 `extras` 변수와 비교되는 모든 리터럴 값을 정규화하여 `frozenset`으로 반환합니다. 관련 헬퍼 메서드(`_collect_referenced_extras`, `_check_extra_comparison`)와 `MarkerVar` 임포트를 추가했습니다.
- `src/packaging/requirements.py`: `Requirement` 클래스에 `marker_extras` 속성(property)을 추가했습니다. 마커가 없으면 빈 `frozenset`을, 있으면 해당 마커의 `referenced_extras()` 결과를 반환합니다. `NormalizedName` 임포트를 추가했습니다.

기존 문자열화, 비교, 해시, 평가 동작은 변경되지 않았습니다.