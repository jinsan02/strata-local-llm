### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    return _repair_python_full_version(current_environment)


class Marker:
=======
    return _repair_python_full_version(current_environment)


def _get_referenced_extras(markers: MarkerList) -> frozenset[str]:
    extras: set[str] = set()
    for marker in markers:
        if isinstance(marker, list):
            extras.update(_get_referenced_extras(marker))
        elif isinstance(marker, tuple):
            lhs, op, rhs = marker
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extras.add(canonicalize_name(lhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extras":
                if isinstance(lhs, Value):
                    extras.add(canonicalize_name(lhs.value))
    return frozenset(extras)


class Marker:
>>>>>>> REPLACE
<<<<<<< SEARCH
    def evaluate_prepared(
        self, environment: Mapping[str, str | AbstractSet[str]]
    ) -> bool:
=======
    def referenced_extras(self) -> frozenset[str]:
        """Return the set of normalized extra names referenced in the marker.
        
        This includes extras compared with ``extra`` (e.g. ``extra == "foo"``)
        and extras checked for membership in ``extras`` (e.g. ``"foo" in extras``).
        """
        return _get_referenced_extras(self._markers)

    def evaluate_prepared(
        self, environment: Mapping[str, str | AbstractSet[str]]
    ) -> bool:
>>>>>>> REPLACE
```

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def __replace__(
=======
    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the set of normalized extra names referenced in the marker.
        
        Returns an empty set if the requirement has no marker.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __replace__(
>>>>>>> REPLACE