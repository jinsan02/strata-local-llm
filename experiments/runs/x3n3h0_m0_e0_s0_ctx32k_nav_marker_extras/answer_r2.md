### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _format_full_version(info: sys._version_info) -> str:
=======
def _referenced_extras(markers: MarkerList) -> set[str]:
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, str):  # "and" or "or"
            continue
        if isinstance(item, list):
            extras.update(_referenced_extras(item))
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            candidate: str | None = None
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    candidate = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    candidate = lhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extras":
                # PEP 685: "x" in extras / "x" not in extras
                if isinstance(lhs, Value):
                    candidate = lhs.value
            
            if candidate is not None:
                extras.add(candidate)
    return extras


def _format_full_version(info: sys._version_info) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in this marker.
        
        This includes names compared against ``extra`` (e.g., ``extra == "foo"``)
        and names checked for membership in the ``extras`` set 
        (e.g., ``"foo" in extras``). Names are canonicalized.
        """
        return frozenset(canonicalize_name(n) for n in _referenced_extras(self._markers))


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
    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
=======
    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Extra names referenced in this requirement's marker.
        
        Returns an empty :class:`frozenset` if the requirement has no marker,
        otherwise returns the result of :meth:`Marker.referenced_extras`.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
>>>>>>> REPLACE