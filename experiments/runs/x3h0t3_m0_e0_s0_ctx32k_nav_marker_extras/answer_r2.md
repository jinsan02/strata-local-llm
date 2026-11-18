### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        if self.marker:
            yield f"; {self.marker}"

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
=======
        if self.marker:
            yield f"; {self.marker}"

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in the requirement's marker.
        
        If the requirement has no marker, returns an empty :py:class:`frozenset`.
        Otherwise, returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.
        """
        return self.marker.referenced_extras() if self.marker else frozenset()

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
>>>>>>> REPLACE