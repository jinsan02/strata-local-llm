### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return all extra names referenced in this marker.

        Scans the marker expression for every occurrence of the ``extra``
        variable (e.g. ``extra == "foo"``) and the ``extras`` set-membership
        variable (e.g. ``"foo" in extras``), and returns the canonicalized
        extra names as a ``frozenset``.

        >>> from packaging.markers import Marker
        >>> Marker('extra == "foo" and "bar" in extras').referenced_extras()
        frozenset({'bar', 'foo'})
        >>> Marker('sys_platform == "linux"').referenced_extras()
        frozenset()
        """
        return _referenced_extras(self._markers)


def _referenced_extras(markers: MarkerList) -> frozenset[str]:
    """Collect all extra names referenced in a marker tree.

    Scans the parsed marker tree for comparisons involving the ``extra``
    variable (e.g. ``extra == "foo"``) and membership tests against the
    ``extras`` set variable (e.g. ``"foo" in extras``). Returns the
    canonicalized extra names as a ``frozenset``.
    """
    extras: set[str] = set()
    _collect_referenced_extras(markers, extras)
    return frozenset(extras)


def _collect_referenced_extras(
    item: MarkerAtom | MarkerLogical, extras: set[str]
) -> None:
    """Recursively collect extra names from a marker tree."""
    if isinstance(item, str):
        # "and", "or" — skip
        return
    if isinstance(item, list):
        for elem in item:
            _collect_referenced_extras(elem, extras)
        return
    # It's a tuple: (lhs, op, rhs)
    lhs, op, rhs = item
    # Check if this comparison involves the "extra" variable
    if isinstance(lhs, Variable) and lhs.value == "extra":
        # extra == "foo" or extra != "foo" etc.
        if isinstance(rhs, Value):
            extras.add(canonicalize_name(rhs.value))
    elif isinstance(rhs, Variable) and rhs.value == "extra":
        # "foo" == extra or "foo" != extra
        if isinstance(lhs, Value):
            extras.add(canonicalize_name(lhs.value))
    elif isinstance(rhs, Variable) and rhs.value == "extras":
        # "foo" in extras or "foo" not in extras
        if isinstance(lhs, Value):
            extras.add(canonicalize_name(lhs.value))
    elif isinstance(lhs, Variable) and lhs.value == "extras":
        # extras contains "foo" — but PEP 508 doesn't define a "contains"
        # operator; only "in" and "not in" are valid, where the string literal
        # is on the left. So this case shouldn't occur in valid markers, but
        # we handle it for robustness.
        if isinstance(rhs, Value):
            extras.add(canonicalize_name(rhs.value))


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
            and self.marker == other.marker
        )
=======
            and self.marker == other.marker
        )

    @property
    def marker_extras(self) -> frozenset[str]:
        """Extra names referenced by this requirement's marker.

        Returns the result of :meth:`~packaging.markers.Marker.referenced_extras`
        if a marker is present, otherwise an empty ``frozenset``.

        >>> from packaging.requirements import Requirement
        >>> Requirement("foo ; extra == 'dev'").marker_extras
        frozenset({'dev'})
        >>> Requirement("foo").marker_extras
        frozenset()
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE

### 요약
- `packaging.markers.Marker`: `referenced_extras()` 메서드 추가. `_referenced_extras`, `_collect_referenced_extras` 헬퍼 함수를 통해 파싱된 마커 트리를 재귀 탐색하며 `extra` 변수 비교 및 `extras` 집합 멤버십 연산에 쓰인 정규화 이름을 `frozenset`으로 수집함.
- `packaging.requirements.Requirement`: `marker_extras` 속성(property) 추가. 마커가 없으면 빈 `frozenset`, 있으면 해당 마커의 `referenced_extras()` 결과를 반환함.
- 기존 문자열화, 비교, 해시, 평가 로직은 손대지 않았으며, 타입 힌트와 도큐먼트스트링만 보완함.