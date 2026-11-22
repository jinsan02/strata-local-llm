### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from ._parser import MarkerAtom, MarkerList, MarkerLogical, Op, Value, Variable
from ._parser import parse_marker as _parse_marker
from ._tokenizer import ParserSyntaxError
from .specifiers import InvalidSpecifier, Specifier
from .utils import canonicalize_name
=======
from ._parser import MarkerAtom, MarkerList, MarkerLogical, Op, Value, Variable
from ._parser import parse_marker as _parse_marker
from ._tokenizer import ParserSyntaxError
from .specifiers import InvalidSpecifier, Specifier
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _evaluate_markers(markers, environment)
=======
def _evaluate_markers(markers, environment)
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _evaluate_markers(markers, environment)
=======
def _evaluate_markers(markers, environment)
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _evaluate_markers(markers, environment) -> bool:
=======
def _extract_referenced_extras(markers: MarkerList) -> set[str]:
    extras: set[str] = set()
    for m in markers:
        if isinstance(m, str):
            continue
        if isinstance(m, tuple):
            lhs, _, rhs = m
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extras" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))
        elif isinstance(m, list):
            extras.update(_extract_referenced_extras(m))
    return extras


def _evaluate_markers(markers, environment) -> bool:
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return a frozenset of extra names referenced in the marker."""
        return frozenset(_extract_referenced_extras(self._markers))
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        self.marker: Marker | None = None
        """A :class:`~.Marker` for the requirement, or ``None``."""
        if parsed.marker is not None:
=======
        self.marker: Marker | None = None
        """A :class:`~.Marker` for the requirement, or ``None``."""
        if parsed.marker is not None:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        self.marker: Marker | None = None
        """A :class:`~.Marker` for the requirement, or ``None``."""
        if parsed.marker is not None:
            self.marker = Marker.__new__(Marker)
            self.marker._markers = _normalize_extra_values(parsed.marker)
            self.marker._serialized = None
=======
        self.marker: Marker | None = None
        """A :class:`~.Marker` for the requirement, or ``None``."""
        if parsed.marker is not None:
            self.marker = Marker.__new__(Marker)
            self.marker._markers = _normalize_extra_values(parsed.marker)
            self.marker._serialized = None

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return a frozenset of extra names referenced in the marker, or empty if no marker."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE