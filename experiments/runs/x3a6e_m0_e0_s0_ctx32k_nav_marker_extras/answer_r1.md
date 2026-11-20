### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def __replace__(
        self,
        *,
        name: str = _UNSET,
=======
    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return extra names referenced in the requirement's marker, if any.

        Equivalent to ``marker.referenced_extras()`` when a marker is present,
        otherwise an empty :class:`frozenset`.

        .. versionadded:: 26.5
        """
        return self.marker.referenced_extras() if self.marker else frozenset()

    def __replace__(
        self,
        *,
        name: str = _UNSET,
>>>>>>> REPLACE