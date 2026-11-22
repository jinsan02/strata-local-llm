수정을 완료했습니다. 변경 내용은 다음과 같습니다.

1. **src/packaging/markers.py**
   - `Marker` 클래스에 `referenced_extras()` 메서드를 추가했습니다. 이 메서드는 마커에서 `extra` 변수와 비교되는 리터럴 문자열(예: `"dev"`)을 찾아 정규화된 이름들의 `frozenset`을 반환합니다.
   - 재귀적으로 마커 트리를 순회하는 `_collect_extras()` 도우미 메서드를 추가했습니다.
   - `NormalizedName` 타입을 import했습니다.

2. **src/packaging/requirements.py**
   - `Requirement` 클래스에 `marker_extras` 속성을 추가했습니다. 마커가 없으면 빈 `frozenset`을, 있으면 `marker.referenced_extras()` 결과를 반환합니다.
   - `NormalizedName` 타입을 import했습니다.