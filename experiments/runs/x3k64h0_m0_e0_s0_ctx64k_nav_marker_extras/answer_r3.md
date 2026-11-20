### 변경 내용 요약
1. **`src/packaging/markers.py`**: `Marker` 클래스에 `referenced_extras()` 메서드를 추가했습니다. 내부적으로 `_collect_extras()` 정적 메서드를 재귀 호출하여 파싱된 마커 트리(`_markers`)를 순회하고, 각 비교 구문(tuple)에서 `extra` 변수 참조 또는 `extras` 집합 멤버십에 쓰인 extra 이름을 정규화해 `frozenset[NormalizedName]`으로 반환합니다. 요청사항에 따라 `dependency_groups` 등 다른 변수는 수집에서 제외됩니다.
2. **`src/packaging/requirements.py`**: `Requirement` 클래스에 `marker_extras` property를 추가했습니다. 마커가 없으면 빈 `frozenset`, 있으면 해당 마커의 `referenced_extras()` 결과를 그대로 반환합니다. 정렬된 타입 힌트를 위해 `.utils.NormalizedName`을 임포트했습니다.

기존 문자열화(`__str__`), 비교(`__eq__`), 해시(`__hash__`), 평가(`evaluate`) 동작은 일절 변경하지 않았습니다. 기존 테스트 파일은 수정하지 않았습니다.