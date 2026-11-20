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
          """Extract all extra names referenced in the marker.

          Returns a ``frozenset`` of normalized extra names compared using
          ``extra == ...``, ``... == extra``, or ``... in extras``.
          """
          extras: set[str] = set()

          def _collect(nodes):
              for node in nodes:
                  if isinstance(node, list):
                      _collect(node)
                  elif isinstance(node, tuple):
                      lhs, op, rhs = node
                      if isinstance(lhs, Variable) and lhs.value == "extra":
                          if isinstance(rhs, Value):
                              extras.add(canonicalize_name(rhs.value))
                      elif isinstance(rhs, Variable) and rhs.value == "extra":
                          if isinstance(lhs, Value):
                              extras.add(canonicalize_name(lhs.value))
                      elif isinstance(rhs, Variable) and rhs.value == "extras":
                          if isinstance(lhs, Value):
                              extras.add(canonicalize_name(lhs.value))

          _collect(self._markers)
          return frozenset(extras)

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
      def __eq__(self, other: object) -> bool:
          if not isinstance(other, Requirement):
              return NotImplemented

          # Extras must be normalized before comparison as per PEP 685.
          self_extras = frozenset(canonicalize_name(e) for e in self.extras)
          other_extras = frozenset(canonicalize_name(e) for e in other.extras)
          return (
              canonicalize_name(self.name) == canonicalize_name(other.name)
              and self_extras == other_extras
              and self.specifier == other.specifier
              and self.url == other.url
              and self.marker == other.marker
          )
=======
      def __eq__(self, other: object) -> bool:
          if not isinstance(other, Requirement):
              return NotImplemented

          # Extras must be normalized before comparison as per PEP 685.
          self_extras = frozenset(canonicalize_name(e) for e in self.extras)
          other_extras = frozenset(canonicalize_name(e) for e in other.extras)
          return (
              canonicalize_name(self.name) == canonicalize_name(other.name)
              and self_extras == other_extras
              and self.specifier == other.specifier
              and self.url == other.url
              and self.marker == other.marker
          )

      @property
      def marker_extras(self) -> frozenset[NormalizedName]:
          """Extras referenced in the marker, or an empty frozenset if none."""
          if self.marker is None:
              return frozenset()
          return self.marker.referenced_extras()
>>>>>>> REPLACE