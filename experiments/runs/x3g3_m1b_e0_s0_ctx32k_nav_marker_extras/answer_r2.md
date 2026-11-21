### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _pep440_python_full_version(python_full_version: str) -> str:
=======
def _extract_referenced_extras(markers: MarkerList) -> frozenset[str]:
    extras: set[str] = set()
    for item in markers:
        if item == "and" or item == "or":
            continue
        if isinstance(item, list):
            extras |= _extract_referenced_extras(item)
        elif isinstance(item, tuple):
            lhs, op, rhs = item
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
        self.__dict__.update(tmp.__dict__)
=======
        self.__dict__.update(tmp.__dict__)

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the set of extra names referenced in this requirement's marker.
        
        Equivalent to ``self.marker.referenced_extras()`` if ``self.marker`` is 
        not ``None``, otherwise an empty ``frozenset``.
        
        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE