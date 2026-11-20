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
        """Return all extra names referenced by the requirement's marker.

        If the requirement has no marker, returns an empty :py:class:`frozenset`.
        Otherwise, delegates to :meth:`~packaging.markers.Marker.referenced_extras()`.

        .. versionadded:: 26.4
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE