수정 완료. 변경된 내용은 다음과 같습니다.

1. **`src/packaging/markers.py`**:
   - `Marker` 클래스에 `referenced_extras()` 메서드를 추가했습니다. 이 메서드는 마커 표현식에서 `extra` 변수와 비교되는 모든 extra 이름을 정규화된 이름으로 모아 `frozenset`으로 반환합니다.
   - 마커 트리를 순회하여 extra 이름을 추출하는 내부 함수 `_extract_referenced_extras()`를 구현했습니다.
   - `NormalizedName` 타입을 `packaging.utils`에서 import했습니다.

2. **`src/packaging/requirements.py`**:
   - `Requirement` 클래스에 `marker_extras` 속성을 추가했습니다. 마커가 있으면 해당 마커의 `referenced_extras()` 결과를, 없으면 빈 `frozenset`을 반환합니다.
   - `NormalizedName` 타입을 `packaging.utils`에서 import했습니다.