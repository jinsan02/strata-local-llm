### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return the extra names referenced in this marker.

        Collects all extra names used in comparisons and membership tests
        within the marker expression (e.g. ``extra == "dev"`` or
        ``"test" in extras``). Returns them as a :class:`frozenset` of
        normalized names.

        >>> from packaging.markers import Marker
        >>> Marker('extra == "dev"').referenced_extras()
        frozenset({'dev'})
        >>> Marker('"foo" in extras and extra != "bar"').referenced_extras()
        frozenset({'foo', 'bar'})

        .. versionadded:: 26.5
        """

        def _collect(
            items: MarkerList | MarkerAtom, extras: set[str]
        ) -> None:
            if isinstance(items, list):
                for item in items:
                    _collect(item, extras)
            elif isinstance(items, tuple):
                lhs, op, rhs = items
                # Check for extra comparisons (extra == "x", "x" == extra)
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extras.add(rhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extras.add(lhs.value)
                # Check for membership tests ("x" in extras, etc.)
                elif (
                    isinstance(rhs, Variable)
                    and rhs.value in MARKERS_ALLOWING_SET
                    and isinstance(lhs, Value)
                ):
                    extras.add(lhs.value)

        referenced: set[str] = set()
        _collect(self._markers, referenced)
        return frozenset(referenced)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
            self.marker._serialized = None

    def __replace__(
=======
            self.marker._serialized = None

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the extra names referenced in the marker.

        Returns an empty :class:`frozenset` if the requirement has no marker,
        otherwise returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        return self.marker.referenced_extras() if self.marker is not None else frozenset()

    def __replace__(
>>>>>>> REPLACE