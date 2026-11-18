### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

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

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in the marker, normalized.
        
        Extracts extras from comparisons (e.g., ``extra == "foo"``) and 
        membership tests (e.g., ``"bar" in extras``). Results are returned as a 
        :class:`frozenset`.
        """
        return frozenset(canonicalize_name(e) for e in _extract_referenced_extras(self._markers))

    def evaluate(
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def _iter_parts(self, name: str) -> Iterator[str]:
=======
    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in the requirement's marker.
        
        Returns a :class:`frozenset` of normalized extra names, or an empty 
        frozenset if no marker is set.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def _iter_parts(self, name: str) -> Iterator[str]:
>>>>>>> REPLACE