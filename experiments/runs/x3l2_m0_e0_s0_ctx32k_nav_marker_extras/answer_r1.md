수정 내용 요약:

**`src/packaging/markers.py`**
- `NormalizedName` import 추가
- `Marker` 클래스에 `referenced_extras()` 메서드 추가: 마커 트리를 재귀적으로 순회하며 `extra`/`extras` 변수와 비교되는 모든 값(문자열 리터럴)을 정규화된 이름으로 수집해 `frozenset` 으로 반환
- 보조 함수 `_referenced_extras()`, `_collect_extras_from_item()`, `_add_extra_value()` 추가

**`src/packaging/requirements.py`**
- `NormalizedName` import 추가
- `Requirement` 클래스에 `marker_extras` property 추가: 마커가 없으면 빈 `frozenset`, 있으면 `marker.referenced_extras()` 결과 반환

기존 동작(문자열화, 비교, 해시, 평가)은 전혀 변경하지 않았습니다.