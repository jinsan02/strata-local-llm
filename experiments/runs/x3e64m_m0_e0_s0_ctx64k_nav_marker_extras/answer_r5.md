수정을 완료했습니다. 변경 내용은 다음과 같습니다:

- `src/packaging/markers.py`: `Marker` 클래스에 `referenced_extras()` 메서드를 추가했습니다. `_collect_referenced_extras()` 헬퍼 메서드를 통해 파싱된 마커 트리를 재귀적으로 순회하며 `extra` 변수 비교(`==`, `!=`)와 `extras`/`dependency_groups` 멤버십(`in`, `not in`) 연산에 사용된 extra 이름을 추출합니다. 파싱 단계(`_normalize_extras`)에서 이미 정규화(`canonicalize_name`)가 적용되었으므로 `frozenset[str]`로 직접 반환합니다.
- `src/packaging/requirements.py`: `Requirement` 클래스에 `marker_extras` 속성(property)을 추가했습니다. 마커가 없으면 빈 `frozenset`을, 있으면 해당 마커의 `referenced_extras()` 결과를 반환합니다.

기존 문자열화, 비교, 해시, 평가 동작은 전혀 변경하지 않았습니다.