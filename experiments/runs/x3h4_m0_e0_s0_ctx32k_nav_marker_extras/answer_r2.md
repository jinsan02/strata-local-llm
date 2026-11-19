수정 완료. 변경 내용 요약:

**src/packaging/markers.py**
- `NormalizedName` 추가 import
- `Marker.referenced_extras()` 메서드 추가: 마커 트리에서 `extra == "x"`, `"x" == extra`, `"x" in extras` 형태를 재귀적으로 탐색해 정규화된 extra 이름 모음을 `frozenset[NormalizedName]`로 반환
- `_collect_referenced_extras()` 정적 메서드 추가: 재귀 순환용 헬퍼

**src/packaging/requirements.py**
- `NormalizedName` 추가 import
- `Requirement.marker_extras` property 추가: `marker`이 `None`이면 빈 `frozenset`, 아니면 `self.marker.referenced_extras()` 결과 반환