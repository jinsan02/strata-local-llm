수정을 완료했습니다. 변경 내용은 다음과 같습니다.

1.  **`src/packaging/markers.py`**:
    *   `Marker` 클래스에 `referenced_extras()` 메서드를 추가했습니다.
    *   이 메서드는 마커 표현식(`and`, `or`, 괄호 포함) 전체를 스캔하여 `extra` 변수와 비교되거나 `extras` 집합에 대한 멤버십 테스트(`in`, `not in`)에 사용된 모든 extra 이름을 정규화된 형태로 `frozenset[NormalizedName]`로 반환합니다.

2.  **`src/packaging/requirements.py`**:
    *   `Requirement` 클래스에 `marker_extras` 속성(property)을 추가했습니다.
    *   이 속성은 마커가 없는 경우 빈 `frozenset`을, 마커가 있는 경우 해당 마커의 `referenced_extras()` 메서드 결과를 반환합니다.

기존 테스트(7921개)를 통과하여 기존 동작이 변경되지 않았음을 확인했습니다.