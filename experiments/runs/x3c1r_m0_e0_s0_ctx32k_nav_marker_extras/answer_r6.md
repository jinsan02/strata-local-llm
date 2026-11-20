### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    def __or__(self, other: Marker) -> Marker:
        """Combine this marker with another using ``or``.

        .. versionadded:: 26.1
        """
        if not isinstance(other, Marker):
            return NotImplemented
        return self._from_markers(_join_markers(self._markers, "or", other._markers))

    def evaluate(
=======
    def __or__(self, other: Marker) -> Marker:
        """Combine this marker with another using ``or``.

        .. versionadded:: 26.1
        """
        if not isinstance(other, Marker):
            return NotImplemented
        return self._from_markers(_join_markers(self._markers, "or", other._markers))

    def referenced_extras(self) -> frozenset[str]:
        """Return all extra names referenced in this marker."""
        def _collect(markers: MarkerList) -> set[str]:
            result: set[str] = set()
            for m in markers:
                if isinstance(m, list):
                    result |= _collect(m)
                elif isinstance(m, tuple):
                    lhs, op, rhs = m
                    # extra == "x" or "x" == extra
                    if isinstance(lhs, Variable) and lhs.value == "extra":
                        result.add(rhs.value)
                    elif isinstance(rhs, Variable) and rhs.value == "extra":
                        result.add(lhs.value)
                    # "x" in extras / "x" in dependency_groups
                    elif isinstance(rhs, Variable) and rhs.value in ("extras", "dependency_groups"):
                        result.add(lhs.value)
            return result
        
        return frozenset(_collect(self._markers))

    def evaluate(
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Requirement):
            return NotImplemented

        # Extras must be normalized before comparison as per PEP 685.
        self_extras = frozenset(canonicalize_name(e) for e in self.extras)
        other_extras = frozenset(canonicalize_name(e) for e in other.extras)
        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self_extras == other_extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )
=======
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Requirement):
            return NotImplemented

        # Extras must be normalized before comparison as per PEP 685.
        self_extras = frozenset(canonicalize_name(e) for e in self.extras)
        other_extras = frozenset(canonicalize_name(e) for e in other.extras)
        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self_extras == other_extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return all extra names referenced by the requirement's marker."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE

수정 내용 요약:
- `src/packaging/markers.py`: `Marker` 클래스에 `_markers` 트리를 순회하며 `extra == "x"`, `"x" == extra`, `"x" in extras`/`dependency_groups` 형태에서 추출한 정규화된 extra 이름들을 집합으로 모아 `frozenset[str]`을 반환하는 `referenced_extras()` 메서드를 추가했습니다. 기존 마커 정규화 과정에서 값이 이미 정규화되므로 별도의 캐니컬라이제이션 없이 직접 반환합니다.
- `src/packaging/requirements.py`: `Requirement` 클래스에 `marker`가 없으면 빈 `frozenset`, 있으면 해당 마커의 `referenced_extras()` 결과를 돌려주는 `marker_extras` 속성(property)을 추가했습니다. 기존 동작에는 영향을 주지 않습니다.