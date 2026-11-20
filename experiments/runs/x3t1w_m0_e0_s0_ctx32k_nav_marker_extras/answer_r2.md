### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

<<<<<<< SEARCH
      def evaluate_prepared(
          self, environment: Mapping[str, str | AbstractSet[str]]
      ) -> bool:
=======
      def referenced_extras(self) -> frozenset["NormalizedName"]:
          """Return a :class:`frozenset` of extra names referenced in this marker.

          Collects all extra names from comparisons with the ``extra`` variable,
          and from PEP 685 membership checks like ``"foo" in extras``. Names are
          returned in their canonical form.
          """
          extras: set[str] = set()

          def _collect(tree):
              for node in tree:
                  if isinstance(node, list):
                      _collect(node)
                  elif isinstance(node, tuple):
                      lhs, _, rhs = node
                      if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                          extras.add(canonicalize_name(rhs.value))
                      elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                          extras.add(canonicalize_name(lhs.value))
                      elif isinstance(lhs, Variable) and lhs.value == "extras" and isinstance(rhs, Value):
                          extras.add(canonicalize_name(rhs.value))
                      elif isinstance(rhs, Variable) and rhs.value == "extras" and isinstance(lhs, Value):
                          extras.add(canonicalize_name(lhs.value))

          _collect(self._markers)
          return frozenset(extras)

      def evaluate_prepared(
          self, environment: Mapping[str, str | AbstractSet[str]]
      ) -> bool:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

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
    def marker_extras(self) -> frozenset["NormalizedName"]:
        """Return the extra names referenced in this requirement's marker, if any."""
        return self.marker.referenced_extras() if self.marker is not None else frozenset()
>>>>>>> REPLACE