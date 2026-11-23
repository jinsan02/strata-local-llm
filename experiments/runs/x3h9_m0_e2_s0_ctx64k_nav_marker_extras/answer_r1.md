수정 완료. 변경 내용 요약:

1. `src/packaging/markers.py`
   - `NormalizedName` 타입 임포트 추가
   - `Marker` 클래스에 `referenced_extras()` 메서드 추가: 마커 트리를 재귀적으로 스캔해 `extra == "x"`, `"x" == extra`, `"x" in extras` 등 `extra` 변수가 등장하는 모든 비교 대상 이름을 정규화하여 `frozenset[NormalizedName]`로 반환

2. `src/packaging/requirements.py`
   - `NormalizedName` 타입 임포트 추가
   - `Requirement` 클래스에 `marker_extras` property 추가: 마커가 없으면 빈 `frozenset`, 있으면 해당 마커의 `referenced_extras()` 결과를 반환

기존 문자열화, 비교, 해시, 평가 동작은 전혀 변경하지 않았습니다.