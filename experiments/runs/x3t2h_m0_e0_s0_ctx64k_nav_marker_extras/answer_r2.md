다음과 같이 수정했습니다:

1. **`src/packaging/markers.py`**
   - `NormalizedName` import 추가.
   - `Marker` 클래스에 `referenced_extras()` 메서드와 `_collect_referenced_extras()` 내부 헬퍼 메서드 추가. 마커 파싱 트리를 재귀적으로 순회하며 `extra` 변수 비교(`==`, `!=`, `>`, `<` 등)와 `in extras` / `not in extras` 조건에서 쓰인 리터럴 값을 수집하고, 최종적으로 정규화된 이름들의 `frozenset[NormalizedName]`로 반환합니다. `and`/`or` 연결이나 괄호 중첩도 모두 처리됩니다.

2. **`src/packaging/requirements.py`**
   - `Requirement` 클래스에 `marker_extras` 속성(property) 추가. 마커가 없으면 빈 `frozenset`, 있으면 해당 마커의 `referenced_extras()` 결과를 그대로 반환합니다.

기존 문자열화, 비교, 해시, 평가 동작은 변경되지 않았습니다.