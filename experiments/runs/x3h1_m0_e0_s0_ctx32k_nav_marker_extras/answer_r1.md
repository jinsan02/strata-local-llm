요청한 기능을 구현하기 위해 다음 파일을 수정했습니다.

1. **`src/packaging/markers.py`**
   - `NormalizedName` 타입 import 추가
   - `_extract_extras(markers: MarkerList) -> set[NormalizedName]` 재귀 헬퍼 함수 추가: 마커 트리를 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras`, `"x" not in extras` 형태를 모두 탐지하고 이름을 정규화(`canonicalize_name`)하여 집합으로 수집합니다. `and`/`or` 논리 연산자나 괄호로 중첩된 구조도 재귀적으로 처리합니다.
   - `Marker.referenced_extras() -> frozenset[NormalizedName]` 메서드 추가: 위 헬퍼 함수를 호출하여 참조된 모든 extra 이름을 정렬되지 않은 상태의 `frozenset`으로 반환합니다.

2. **`src/packaging/requirements.py`**
   - `Requirement.marker_extras` 속성(property) 추가: 마커가 없으면 빈 `frozenset`을, 있으면 해당 마커의 `.referenced_extras()` 결과를 그대로 반환합니다. 기존 문자열화, 비교, 해시, 평가 로직에는 아무런 영향을 주지 않습니다.