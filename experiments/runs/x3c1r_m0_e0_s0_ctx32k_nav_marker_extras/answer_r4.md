수정 완료. 변경 사항을 요약하면 다음과 같습니다.

### `src/packaging/markers.py`
- `.utils.NormalizedName` import 추가
- 마커 트리를 재귀적으로 순회하며 `extra` 비교식(`extra == "x"`, `"x" == extra`)과 멤버십 연산식(`"x" in extras`)에서 리터럴 값을 추출하는 `_extract_referenced_extras()` 헬퍼 함수 추가
- `Marker` 클래스에 `referenced_extras() -> frozenset[NormalizedName]` 메서드 구현. `&`/`|` 중첩 및 `and`/`or` 구조를 모두 탐색하며, `dependency_groups` 등은 무시함

### `src/packaging/requirements.py`
- `.utils.NormalizedName` import 추가
- `Requirement` 클래스에 `marker_extras` property 추가. 마커가 없으면 빈 `frozenset()`, 있으면 해당 마커의 `referenced_extras()` 결과를 반환

기존 문자열화, 비교, 해시, 평가 로직은 변경하지 않았습니다. 테스트 파일 수정 없음.