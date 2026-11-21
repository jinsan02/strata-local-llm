### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE
<<<<<<< SEARCH
    return any(all(item) for item in groups)


def _format_full_version(info: sys._version_info) -> str:
=======
    return any(all(item) for item in groups)


def _marker_extras(markers: MarkerList) -> frozenset[NormalizedName]:
    result: set[NormalizedName] = set()
    for m in markers:
        if isinstance(m, list):
            result.update(_marker_extras(m))
        elif isinstance(m, tuple):
            lhs, _op, rhs = m
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                result.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                result.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extras" and isinstance(lhs, Value):
                result.add(canonicalize_name(lhs.value))
            elif isinstance(lhs, Variable) and lhs.value == "extras" and isinstance(rhs, Value):
                result.add(canonicalize_name(rhs.value))
    return frozenset(result)


def _format_full_version(info: sys._version_info) -> str:
>>>>>>> REPLACE
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in this marker.
        
        Collects names from ``extra == "name"``, ``"name" == extra``,
        ``extra != "name"``, ``"name" in extras``, etc.
        Returns a frozenset of normalized names.
        """
        return _marker_extras(self._markers)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE
<<<<<<< SEARCH
        and self.marker == other.marker
        )
=======
        and self.marker == other.marker
        )

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in the requirement's marker."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE