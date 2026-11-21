수정 내용을 요약하면:

1. **`src/packaging/markers.py`** — `Marker` 클래스에 두 메서드 추가:
   - `referenced_extras()`: 마커 트리를 재귀적으로 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras`, `"x" not in extras` 등에서 언급된 모든 extra 이름을 정규화된 이름(normalized name)으로 모아 `frozenset[str]`로 반환. `and`/`or` 체인과 괄호로 중첩된 식 전체를 모두 봄.
   - `_collect_referenced_extras()`: `referenced_extras()` 내부에서 쓰는 정적 보조 메서드.

2. **`src/packaging/requirements.py`** — `Requirement` 클래스에 property 추가:
   - `marker_extras`: 마커가 없으면 빈 `frozenset()`, 있으면 `self.marker.referenced_extras()` 결과를 반환.

기존 동작(문자열화, 비교, 해시, 평가)은 전혀 건드리지 않았다.