### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _normalize_extra_values(results: MarkerList) -> MarkerList:
    """
    Normalize extra values.
    """

    return [_normalize_extras(r) for r in results]


_GROUP_TYPES: Final = (list, tuple)
=======
def _normalize_extra_values(results: MarkerList) -> MarkerList:
    """
    Normalize extra values.
    """

    return [_normalize_extras(r) for r in results]


def _collect_referenced_extras(markers: MarkerList) -> set[str]:
    extras: set[str] = set()
    for part in markers:
        if isinstance(part, list):
            extras |= _collect_referenced_extras(part)
        elif isinstance(part, tuple):
            lhs, op, rhs = part
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extras.add(lhs.value)
            elif isinstance(lhs, Value) and isinstance(rhs, Variable):
                if rhs.value in ("extras", "dependency_groups") and op.serialize() in ("in", "not in"):
                    extras.add(lhs.value)
    return extras


_GROUP_TYPES: Final = (list, tuple)
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

      def referenced_extras(self) -> frozenset[str]:
          """Return all extra names referenced by this marker, normalized."""
          return frozenset(_collect_referenced_extras(self._markers))

      def evaluate(
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
              self.marker._markers = _normalize_extra_values(parsed.marker)
              self.marker._serialized = None

      def __replace__(
=======
              self.marker._markers = _normalize_extra_values(parsed.marker)
              self.marker._serialized = None

      @property
      def marker_extras(self) -> frozenset[str]:
          """Return all extra names referenced by this requirement's marker."""
          return self.marker.referenced_extras() if self.marker else frozenset()

      def __replace__(
>>>>>>> REPLACE