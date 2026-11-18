### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _collect_extras(markers: MarkerList) -> set[str]:
    """Collect all extra names referenced in a marker list."""
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, list):
            extras.update(_collect_extras(item))
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra":
                extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                extras.add(lhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extras":
                extras.add(lhs.value)
    return extras
=======
def _collect_extras(markers: MarkerList) -> set[str]:
    """Collect all normalized extra names referenced in a marker list."""
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, list):
            extras.update(_collect_extras(item))
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra":
                extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extras":
                extras.add(canonicalize_name(lhs.value))
    return extras
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self_extras == other_extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )
=======
        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self_extras == other_extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return a frozen set of normalized extra names referenced in the marker.
        
        If there is no marker, returns an empty frozenset. Otherwise, delegates to
        :meth:`Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE