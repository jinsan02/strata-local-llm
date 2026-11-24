수정 완료. 변경 내용을 요약하면:

### `src/packaging/markers.py`
- `NormalizedName = str` 타입 별칭 추가
- `_referenced_extras(markers)` 헬퍼 함수 추가: 마커 트리를 순회하며 `extra` 변수와 비교되는 모든 extra 이름을 정규화된 형태로 수집
- `_collect_referenced_extras(item, extras)` 재귀 헬퍼 함수 추가: 리스트(`and`/`or` 중첩), 문자열(`"and"`/`"or"` 연산자), 튜플(비교 연산) 처리
- `Marker.referenced_extras()` 메서드 추가: `_referenced_extras(self._markers)` 호출

### `src/packaging/requirements.py`
- `.markers` 모듈에서 `NormalizedName` import 추가
- `Requirement.marker_extras` property 추가: 마커가 없으면 빈 `frozenset`, 있으면 `self.marker.referenced_extras()` 결과 반환

기존 동작(문자열화, 비교, 해시, 평가)은 변경되지 않음.