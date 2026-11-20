### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
              and self.marker == other.marker
          )
=======
              and self.marker == other.marker
          )

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in the requirement's marker.
        
        If the requirement has no marker, returns an empty frozenset.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE