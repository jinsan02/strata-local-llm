수정 내용 요약:
- `src/packaging/markers.py`: `utils`에서 `NormalizedName`을 추가 import하고, `_get_referenced_extras()` 헬퍼 함수를 추가하여 파싱된 마커 트리(`MarkerList`)를 재귀적으로 순회합니다. `extra` 변수와 비교(`==`, `!=` 등)되거나 `extras` 멤버십 테스트(`in`, `not in`)에 등장하는 리터럴 값을 추출해 정규화된 이름으로 모은 `frozenset`을 반환합니다. `Marker` 클래스에 `referenced_extras()` 메서드를 추가하여 이 헬퍼를 호출하도록 구현했습니다.
- `src/packaging/requirements.py`: `utils`에서 `NormalizedName`을 추가 import하고, `Requirement` 클래스에 `marker_extras` 속성(property)을 추가했습니다. 마커가 없으면 빈 `frozenset`을, 있으면 `self.marker.referenced_extras()` 결과를 그대로 돌려줍니다.

기존 문자열화(`__str__`), 비교(`__eq__`), 해시(`__hash__`), 평가(`evaluate`) 동작은 전혀 건드리지 않았습니다.