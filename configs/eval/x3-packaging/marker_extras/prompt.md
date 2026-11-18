`packaging.markers.Marker` 에 메서드 `referenced_extras()` 를, `packaging.requirements.Requirement` 에 속성(property) `marker_extras` 를 추가하라.

- `Marker.referenced_extras() -> frozenset[NormalizedName]`: 마커 안에서 `extra` 변수와 비교되는 모든 extra 이름(`extra == "x"`, `"x" == extra`, `extra != "x"` 등 모든 비교 연산)과, `"x" in extras` / `"x" not in extras` 형태로 쓰인 이름을 **정규화된 이름**으로 모아 돌려준다.
  - `and` / `or` 와 괄호로 중첩된 식 전체를 본다.
  - `dependency_groups` 등 다른 변수의 값은 넣지 않는다. extra 를 쓰지 않는 마커는 빈 `frozenset` 을 돌려준다.
  - `&` · `|` 로 합친 마커에서도 동작해야 한다.
- `Requirement.marker_extras`: 마커가 없으면 빈 `frozenset`, 있으면 그 마커의 `referenced_extras()` 결과.
- 기존 동작(문자열화, 비교, 해시, 평가)은 바뀌면 안 된다.
