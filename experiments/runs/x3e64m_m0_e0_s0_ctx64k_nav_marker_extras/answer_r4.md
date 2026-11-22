### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

<<<<<<< SEARCH
def _normalize_extra_values(results: MarkerList) -> MarkerList:
    """
    Normalize extra values.
    """

    return [_normalize_extras(r) for r in results]


_GROUP_TYPES: Final = (list, tuple)
=======
def _normalize_extra_values(results: MarkerList) -> MarkerList:
    """
    Normalize extra values.
    """

    return [_normalize_extras(r) for r in results]


def _extract_extras(markers: MarkerList) -> set[str]:
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, list):
            extras |= _extract_extras(item)
        elif isinstance(item, tuple):
            lhs, _op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extras":
                if isinstance(lhs, Value):
                    extras.add(canonicalize_name(lhs.value))
    return extras


_GROUP_TYPES: Final = (list, tuple)
>>>>>>> REPLACE

<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return a frozenset of normalized extra names referenced in this marker."""
        return frozenset(_extract_extras(self._markers))


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

<<<<<<< SEARCH
            yield f"; {self.marker}"

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
=======
            yield f"; {self.marker}"

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return the extra names referenced in the marker, or an empty frozenset."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
>>>>>>> REPLACE