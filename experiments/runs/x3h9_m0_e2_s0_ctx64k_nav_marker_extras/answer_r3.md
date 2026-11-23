### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    def _collect_referenced_extras(
        self,
        markers: MarkerList,
        extras: list[str],
    ) -> None:
        for item in markers:
            if isinstance(item, list):
                self._collect_referenced_extras(item, extras)
            elif isinstance(item, tuple):
                lhs, _op, rhs = item
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extras.append(rhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extras.append(lhs.value)
=======
    def _collect_referenced_extras(
        self,
        markers: MarkerList,
        extras: list[str],
    ) -> None:
        for item in markers:
            if isinstance(item, list):
                self._collect_referenced_extras(item, extras)
            elif isinstance(item, tuple):
                lhs, _op, rhs = item
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extras.append(rhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extras.append(lhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extras":
                    if isinstance(lhs, Value):
                        extras.append(lhs.value)
>>>>>>> REPLACE

### 설명
- `src/packaging/markers.py`:
  - `Marker.referenced_extras()` 메서드를 추가했습니다.
  - `_collect_referenced_extras()` 보조 메서드를 추가하여 마커 트리를 순회하며 `extra` 변수와 비교되는 이름(`extra == "x"`, `"x" == extra` 등)과 `extras` 집합 멤버십(`"x" in extras`)에 쓰인 이름을 수집합니다.
  - `TYPE_CHECKING` 블록에 `NormalizedName` 타입을 import했습니다.
- `src/packaging/requirements.py`:
  - `Requirement.marker_extras` 속성을 추가했습니다. 마커가 없으면 빈 `frozenset`을, 있으면 `marker.referenced_extras()`의 결과를 반환합니다.