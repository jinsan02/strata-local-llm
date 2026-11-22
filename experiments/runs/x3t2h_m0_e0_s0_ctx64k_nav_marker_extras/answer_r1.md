`packaging.markers.Marker` 클래스에 `referenced_extras()` 메서드를, `packaging.requirements.Requirement` 클래스에 `marker_extras` 속성을 추가했습니다.

- `Marker.referenced_extras()`: 마커에서 `extra` 변수와 비교되거나 `extras`에 대한 멤버십 테스트에 사용된 모든 extra 이름을 정규화하여 `frozenset`으로 반환합니다.
- `Requirement.marker_extras`: 마커가 없으면 빈 `frozenset`, 있으면 `marker.referenced_extras()`의 결과를 반환하는 property입니다.