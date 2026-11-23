수정 내용 요약:

1. **`src/packaging/markers.py`**
   - `NormalizedName = str` 타입 별칭 추가
   - `_referenced_extras()` 및 `_collect_referenced_extras()` 헬퍼 함수 추가: 마커 트리를 재귀적으로 순회하며 `extra` 변수와 비교되거나 `extras` 집합에 대한 멤버십 연산(`in`/`not in`)에 쓰인 모든 extra 이름을 정규화하여 수집
   - `Marker` 클래스에 `referenced_extras() -> frozenset[NormalizedName]` 메서드 추가: `and`/`or` 중첩 및 괄호 처리를 포함한 전체 마커 식에서 extra 이름을 반환

2. **`src/packaging/requirements.py`**
   - `Requirement` 클래스에 `marker_extras` 속성(property) 추가: 마커가 없으면 빈 `frozenset()`, 있으면 해당 마커의 `referenced_extras()` 결과를 반환

기존 동작(문자열화, 비교, 해시, 평가, pickle 호환성 등)은 전혀 변경하지 않았습니다.