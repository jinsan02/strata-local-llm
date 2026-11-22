수정 완료. 변경 내용 요약:

**src/packaging/markers.py**
- `NormalizedName` import 추가
- `_collect_referenced_extras()` 함수 추가: 마커 트리를 재귀적으로 탐색해 `extra` 변수 비교(`extra == "x"`, `"x" == extra`)와 `extras` 멤버십(`"x" in extras`, `"x" not in extras`)에서 쓰인 extra 이름을 수집
- `_get_referenced_extras()` 함수 추가: 위 함수를 호출해 집합을 반환
- `Marker.referenced_extras()` 메서드 추가: `_get_referenced_extras()` 결과를 `frozenset[NormalizedName]`로 반환

**src/packaging/requirements.py**
- `NormalizedName` import 추가
- `Requirement.marker_extras` 속성(property) 추가: 마커가 없으면 빈 `frozenset`, 있으면 `self.marker.referenced_extras()` 반환