### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _pep440_python_full_version(python_full_version: str) -> str:
=======
def _extract_extras(markers: MarkerList) -> frozenset[str]:
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, list):
            extras |= _extract_extras(item)
        elif isinstance(item, tuple):
            lhs, _, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extras" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))
    return frozenset(extras)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def __replace__(
        self,
        *,
        name: str = _UNSET,
        url: str | None = _UNSET,
        extras: set[str] = _UNSET,
        specifier: SpecifierSet = _UNSET,
        marker: Marker | None = _UNSET,
    ) -> Self:
=======
    @property
    def marker_extras(self) -> frozenset[str]:
        """Return all extra names referenced in the marker.

        Returns an empty :class:`frozenset` if there is no marker.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __replace__(
        self,
        *,
        name: str = _UNSET,
        url: str | None = _UNSET,
        extras: set[str] = _UNSET,
        specifier: SpecifierSet = _UNSET,
        marker: Marker | None = _UNSET,
    ) -> Self:
>>>>>>> REPLACE