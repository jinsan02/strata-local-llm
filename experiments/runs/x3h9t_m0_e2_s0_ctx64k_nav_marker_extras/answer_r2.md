수정 사항을 요약하면:

1. **`src/packaging/markers.py`**:
   - `NormalizedName`를 `utils`에서 import 추가
   - `Marker` 클래스에 `referenced_extras()` 메서드 추가: `_markers` 트리를 재귀적으로 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras` 형태에서 `x` 값을 수집하여 정규화된 이름들의 `frozenset`으로 반환
   - 내부 보조 메서드 `_collect_extras()` 구현

2. **`src/packaging/requirements.py`**:
   - `NormalizedName`를 `utils`에서 import 추가
   - `Requirement` 클래스에 `marker_extras` property 추가: 마커가 없으면 빈 `frozenset`, 있으면 `marker.referenced_extras()` 결과 반환

기존 테스트 7921개 모두 통과.