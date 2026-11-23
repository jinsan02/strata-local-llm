수정 사항 요약:

1. **`src/packaging/markers.py`**: `Marker` 클래스에 `referenced_extras()` 메서드와 내부 보조 메서드 `_collect_extras()` 추가
   - `_markers` 트리를 재귀적으로 순회하며 `extra == "name"`, `"name" == extra`, `"name" in extras`, `"name" not in extras` 형태의 비교에서 extra 이름을 추출
   - `canonicalize_name()`으로 정규화된 이름만 모아 `frozenset`으로 반환
   - `and`/`or` 중첩과 괄호 모두 처리

2. **`src/packaging/requirements.py`**: `Requirement` 클래스에 `marker_extras` property 추가
   - 마커가 없으면 빈 `frozenset`, 있으면 `self.marker.referenced_extras()` 결과 반환