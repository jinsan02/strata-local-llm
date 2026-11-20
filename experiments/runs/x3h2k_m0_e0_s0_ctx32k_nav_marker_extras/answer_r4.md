다음과 같이 수정했습니다:

1. `src/packaging/markers.py`: `Marker` 클래스에 `referenced_extras()` 메서드를 추가했습니다. `_markers` 트리를 재귀적으로 탐색하여 `extra` 변수와 비교(`==`, `!=` 등)되거나 `extras` 집합에 대한 멤버십 연산(`in`, `not in`)에 쓰인 모든 extra 이름을 수집하고, `canonicalize_name`으로 정규화하여 `frozenset[NormalizedName]`로 반환합니다. `and`/`or` 중첩 및 괄호 처리도 지원합니다.
2. `src/packaging/requirements.py`: `Requirement` 클래스에 `marker_extras` 속성(property)을 추가했습니다. 마커가 `None`이 아니면 `self.marker.referenced_extras()`를, 아니면 빈 `frozenset()`을 반환합니다.
3. 두 파일 모두 `packaging.utils`에서 `NormalizedName` 타입을 import하여 반환 타입 정의를 정확히 맞추었습니다.

기존 문자열화, 비교, 해시, 평가 동작은 전혀 변경하지 않았습니다.