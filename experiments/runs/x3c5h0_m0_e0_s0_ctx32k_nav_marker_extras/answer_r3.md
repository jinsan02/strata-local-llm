### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
          .. versionadded:: 26.4
          """
          return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
          .. versionadded:: 26.4
          """
          return _evaluate_markers(self._markers, environment)

      def referenced_extras(self) -> frozenset[NormalizedName]:
          """Return the set of extra names referenced in this marker.

          Looks at all ``extra`` comparisons (e.g. ``extra == "Foo"``),
          and ``"x" in extras`` / ``"x" not in extras`` membership checks,
          and returns their values as a :class:`frozenset` of
          :class:`~packaging.utils.NormalizedName`.

          .. versionadded:: 26.5
          """
          return frozenset(
              canonicalize_name(name) for name in _extract_referenced_extras(self._markers)
          )


def _pep440_python_full_version(python_full_version: str) -> str:
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
          """The set of extra names referenced in the requirement's marker."""
          if self.marker is None:
              return frozenset()
          return self.marker.referenced_extras()
>>>>>>> REPLACE