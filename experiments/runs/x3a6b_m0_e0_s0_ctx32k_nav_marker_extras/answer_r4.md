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

          return str(self) == str(other)

      def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
=======
      def __eq__(self, other: object) -> bool:
          if not isinstance(other, Requirement):
              return NotImplemented

          return str(self) == str(other)

      @property
      def marker_extras(self) -> frozenset[NormalizedName]:
          """Return the extra names referenced in this requirement's marker.

          Returns an empty :class:`frozenset` if there is no marker, otherwise
          returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.
          """
          if self.marker is None:
              return frozenset()
          return self.marker.referenced_extras()

      def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
>>>>>>> REPLACE