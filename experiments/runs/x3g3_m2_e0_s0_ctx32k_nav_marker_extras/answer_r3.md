### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    return any(all(item) for item in groups)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
    return any(all(item) for item in groups)


def _extract_extras(markers: MarkerList) -> frozenset[str]:
    extras: set[str] = set()

    def _walk(item: MarkerAtom | MarkerLogical) -> None:
        if isinstance(item, list):
            for m in item:
                _walk(m)
        elif isinstance(item, tuple):
            lhs, _op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extras.add(canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extras.add(canonicalize_name(lhs.value))

    _walk(markers)
    return frozenset(extras)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        result.specifier = copy.deepcopy(tmp.specifier)
        return result

    def _iter_parts(self, name: str) -> Iterator[str]:
=======
        result.specifier = copy.deepcopy(tmp.specifier)
        return result

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return all extra names referenced in the requirement's marker.

        Returns an empty :py:class:`frozenset` if the requirement has no marker.
        Otherwise, returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def _iter_parts(self, name: str) -> Iterator[str]:
>>>>>>> REPLACE