### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Requirement):
            return NotImplemented
=======
    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in this requirement's marker.

        Equivalent to calling :meth:`Marker.referenced_extras` on
        :attr:`marker`, or an empty :class:`frozenset` if no marker is set.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Requirement):
            return NotImplemented
>>>>>>> REPLACE