수정 완료. 주요 변경 내용은 다음과 같습니다:

1. **`src/packaging/markers.py`**:
   - `NormalizedName` 타입을 `from .utils import ...`로 추가 import했습니다.
   - `Marker` 클래스에 `referenced_extras(self) -> frozenset[NormalizedName]` 메서드를 추가했습니다.
   - 마커 트리(`_markers`)를 재귀적으로 순회하며 `extra` 또는 `extras` 변수가 등장하는 모든 비교 구문(`==`, `!=`, `in`, `not in` 등)에서 리터럴 값을 추출해 정규화된 이름으로 모으는 `_collect_extras()` 정적 헬퍼 메서드를 함께 구현했습니다.

2. **`src/packaging/requirements.py`**:
   - `Requirement` 클래스에 `marker_extras` property를 추가했습니다. 마커가 없으면 빈 `frozenset`을, 있으면 `self.marker.referenced_extras()`의 결과를 반환합니다.

기존 `__str__`, `__eq__`, `__hash__`, `evaluate()` 등 모든 기존 동작과 API는 변경되지 않았습니다.