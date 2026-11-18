### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
              canonicalize_name(self.name) == canonicalize_name(other.name)
              and self_extras == other_extras
              and self.specifier == other.specifier
              and self.url == other.url
              and self.marker == other.marker
          )
=======
              canonicalize_name(self.name) == canonicalize_name(other.name)
              and self_extras == other_extras
              and self.specifier == other.specifier
              and self.url == other.url
              and self.marker == other.marker
          )

      @property
      def marker_extras(self) -> frozenset[NormalizedName]:
          """Return extra names referenced by this requirement's marker.

          Returns an empty :class:`frozenset` if there is no marker.

          .. versionadded:: NEXT_VERSION
          """
          if self.marker is None:
              return frozenset()
          return self.marker.referenced_extras()
>>>>>>> REPLACE