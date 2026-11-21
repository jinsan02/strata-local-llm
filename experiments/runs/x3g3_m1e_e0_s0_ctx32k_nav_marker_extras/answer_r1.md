### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
class Marker:
=======
def _collect_extras(markers: MarkerList) -> frozenset["NormalizedName"]:
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, list):
            extras.update(_collect_extras(item))
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extras" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))
            elif isinstance(lhs, Variable) and lhs.value == "extras" and isinstance(rhs, Value):
                extras.add(canonicalize_name(rhs.value))
    return frozenset(extras)


class Marker:
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
          return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
          return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset["NormalizedName"]:
        """Return the set of extra names referenced in this marker.

        Scans the marker expression for all comparisons involving the ``extra``
        variable (e.g. ``extra == "x"``, ``"x" == extra``) and all membership
        checks in the ``extras`` set (e.g. ``"x" in extras``, ``"x" not in
        extras``).  Returns the canonicalised extra names as a
        :class:`frozenset`.

        ``and`` / ``or`` combinations and nested parentheses are handled
        transparently.  Markers that do not reference any extra return an
        empty :class:`frozenset`.

        .. versionadded:: 26.5
        """
        return _collect_extras(self._markers)


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
            and self.marker == other.marker
        )
=======
            and self.marker == other.marker
        )

    @property
    def marker_extras(self) -> frozenset["NormalizedName"]:
        """The extra names referenced in the marker, or an empty frozenset if none."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE