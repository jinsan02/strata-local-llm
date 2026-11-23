수정 완료. 변경 사항을 요약하면 다음과 같습니다.

1. **`src/packaging/markers.py`**
   - `NormalizedName` 타입을 `.utils`에서 import 추가.
   - `Marker` 클래스에 `referenced_extras()` 메서드 추가: 마커 표현식 트리를 재귀적으로 순회(`_collect_extras`)하며 `extra == "x"`, `"x" == extra`, `"x" in extras`, `"x" not in extras` 형태에서 extra 이름을 찾아 `canonicalize_name`으로 정규화한 `frozenset[NormalizedName]`을 반환.
   - 중첩된 `and`/`or`/괄호 구조도 자연스럽게 처리하도록 설계됨.

2. **`src/packaging/requirements.py`**
   - `Requirement` 클래스에 `marker_extras` 속성(property) 추가: `marker`가 `None`이면 빈 `frozenset`, 그렇지 않으면 `self.marker.referenced_extras()` 결과를 반환.

기존 문자열화(`__str__`), 비교(`__eq__`), 해시(`__hash__`), 평가(`evaluate`, `evaluate_prepared`) 동작은 전혀 건드리지 않았습니다. 모든 수정이 적용되었습니다.