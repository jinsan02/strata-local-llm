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
      def marker_extras(self) -> frozenset[utils.NormalizedName]:
          """Return all extra names referenced in this requirement's marker.

          Returns an empty ``frozenset`` if the requirement has no marker, or if
          the marker does not reference any extras.

          .. versionadded:: 26.5
          """
          if self.marker is None:
              return frozenset()
          return self.marker.referenced_extras()
>>>>>>> REPLACE