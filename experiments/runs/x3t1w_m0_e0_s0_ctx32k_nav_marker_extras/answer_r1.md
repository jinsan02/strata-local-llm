### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
class Marker:
=======
def _extract_extras(markers: MarkerList) -> set[str]:
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, list):
            extras |= _extract_extras(item)
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extras" and isinstance(lhs, Value):
                if op.serialize() in ("in", "not in"):
                    extras.add(canonicalize_name(lhs.value))
    return extras


class Marker:
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
        """Return a frozen set of normalized extra names referenced by this marker.

        Collects extras from all comparison forms: ``extra == "x"``,
        ``"x" == extra``, ``extra != "x"``, and membership tests like
        ``"x" in extras`` or ``"x" not in extras``. Returns an empty frozenset
        if no extras are referenced.
        """
        return frozenset(_extract_extras(self._markers))

    def evaluate(
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
            spec._prereleases = spec_prereleases
        self.specifier = tmp.specifier


=======
            spec._prereleases = spec_prereleases
        self.specifier = tmp.specifier

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return a frozen set of extra names referenced by the marker, or empty if none."""
        return self.marker.referenced_extras() if self.marker is not None else frozenset()


>>>>>>> REPLACE