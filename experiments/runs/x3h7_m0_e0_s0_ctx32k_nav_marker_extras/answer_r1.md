### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
            result.specifier = copy.deepcopy(tmp.specifier)
            return result

        def _iter_parts(self, name: str) -> Iterator[str]:
=======
            result.specifier = copy.deepcopy(tmp.specifier)
            return result

        @property
        def marker_extras(self) -> frozenset[NormalizedName]:
            """Return a frozenset of all extra names referenced in the marker.

            Returns an empty frozenset if the requirement has no marker.

            .. versionadded:: 26.5
            """
            if self.marker is None:
                return frozenset()
            return self.marker.referenced_extras()

        def _iter_parts(self, name: str) -> Iterator[str]:
>>>>>>> REPLACE