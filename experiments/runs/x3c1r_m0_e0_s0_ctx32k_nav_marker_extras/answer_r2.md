### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
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


def _referenced_extras(markers: MarkerList) -> frozenset[NormalizedName]:
    result: set[NormalizedName] = set()
    for marker in markers:
        if isinstance(marker, list):
            result |= _referenced_extras(marker)
        elif isinstance(marker, tuple):
            lhs, op, rhs = marker
            if isinstance(lhs, Variable):
                if lhs.value == "extra" and isinstance(rhs, Value):
                    result.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable):
                if rhs.value == "extra" and isinstance(lhs, Value):
                    result.add(canonicalize_name(lhs.value))
                elif rhs.value == "extras" and isinstance(lhs, Value):
                    result.add(canonicalize_name(lhs.value))
    return frozenset(result)


_GROUP_TYPES: Final = (list, tuple)
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: object) -> bool:
=======
    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Extra names referenced in this requirement's marker, if any."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __eq__(self, other: object) -> bool:
>>>>>>> REPLACE