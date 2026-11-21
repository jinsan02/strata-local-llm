다음과 같이 수정을 완료했습니다:

1. `src/packaging/markers.py`: `Marker` 클래스에 `referenced_extras()` 메서드를 추가했습니다. 마커 표현식 트리를 재귀적으로 순회하며 `extra` 변수 비교(`==`, `!=` 등) 및 `extras` 집합 멤버십(`in`, `not in`) 연산에 등장하는 extra 이름을 정규화된 이름으로 추출하여 `frozenset[NormalizedName]`으로 반환합니다. 이를 위해 `_collect_referenced_extras`, `_extract_extra_from_item` 보조 메서드를 함께 구현했습니다.
2. `src/packaging/requirements.py`: `Requirement` 클래스에 `marker_extras` 속성(property)을 추가했습니다. 마커가 없으면 빈 `frozenset`을, 있으면 해당 마커의 `referenced_extras()` 결과를 반환합니다.
3. 두 파일 모두 `NormalizedName` 타입을 `packaging.utils`에서 import하도록 수정했습니다.

기존 동작(문자열화, 비교, 해시, 평가 등)은 전혀 변경하지 않았습니다.