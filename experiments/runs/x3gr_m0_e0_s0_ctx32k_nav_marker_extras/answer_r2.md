### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
class Marker:
=======
def _extract_extras_from_markers(
    markers: MarkerList,
) -> set[str]:
    """Recursively extract all extra names referenced in a marker tree."""
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, list):
            extras |= _extract_extras_from_markers(item)
        elif isinstance(item, tuple):
            lhs, _op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))
            elif isinstance(lhs, Value) and isinstance(rhs, Variable) and rhs.value == "extras":
                extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Value) and isinstance(lhs, Variable) and lhs.value == "extras":
                extras.add(canonicalize_name(rhs.value))
    return extras


class Marker:
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return the set of extra names referenced in this marker.

        This includes extras compared against the ``extra`` variable (e.g.
        ``extra == "foo"``) and extras checked for membership in the ``extras``
        variable (e.g. ``"foo" in extras``).  The names are returned in their
        canonicalized form.

        .. versionadded:: 26.5
        """
        return frozenset(_extract_extras_from_markers(self._markers))


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        return result

    def _iter_parts(self, name: str) -> Iterator[str]:
=======
        return result

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return the set of extra names referenced in the marker.

        If the requirement has no marker, returns an empty frozenset.
        Otherwise, returns the result of :meth:`Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def _iter_parts(self, name: str) -> Iterator[str]:
>>>>>>> REPLACE

`packaging.markers.Marker` 클래스에 `referenced_extras()` 메서드를, `packaging.requirements.Requirement` 클래스에 `marker_extras` 속성을 추가했습니다.

- `Marker.referenced_extras()`: 마커 트리를 재귀적으로 순회하여 `extra` 변수와의 비교(`==`, `!=` 등) 및 `extras` 변수에 대한 멤버십 검사(`in`, `not in`)에 등장하는 extra 이름을 정규화하여 `frozenset`으로 반환합니다.
- `Requirement.marker_extras`: 마커가 없으면 빈 `frozenset`을, 있으면 해당 마커의 `referenced_extras()` 결과를 반환하는 property입니다.