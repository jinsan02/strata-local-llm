수정 완료. 변경 사항을 요약하면:

1. **`src/packaging/markers.py`**: `Marker` 클래스에 `referenced_extras()` 메서드와 정적 보조 메서드 `_collect_extras()` 추가
   - 마커 트리를 재귀적으로 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras`, `"x" not in extras` 형태에서 extra 이름을 추출
   - `&`/`|`로 연결된 마커나 괄호로 중첩된 구조도 모두 처리
   - 모든 이름은 `canonicalize_name()`으로 정규화하여 `frozenset`으로 반환

2. **`src/packaging/requirements.py`**: `Requirement` 클래스에 `marker_extras` property 추가
   - 마커가 없으면 빈 `frozenset`, 있으면 `marker.referenced_extras()` 결과 반환