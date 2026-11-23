### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
          return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
          return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return the set of extra names referenced in this marker.

        Walks the entire marker expression (including ``and`` / ``or``
        sub-expressions and parentheses) and collects every extra name that
        appears in a comparison with the ``extra`` variable, returning them as
        a ``frozenset`` of normalised names.

        >>> from packaging.markers import Marker
        >>> Marker('extra == "foo"').referenced_extras()
        frozenset({'foo'})
        >>> Marker('extra == "foo" or extra == "bar"').referenced_extras()
        frozenset({'bar', 'foo'})
        >>> Marker('os_name == "nt"').referenced_extras()
        frozenset()

        .. versionadded:: 26.5
        """
        extras: set[NormalizedName] = set()
        self._collect_referenced_extras(self._markers, extras)
        return frozenset(extras)

    def _collect_referenced_extras(
        self,
        item: MarkerAtom | MarkerLogical,
        extras: set[NormalizedName],
    ) -> None:
        """Recursively collect extra names from a marker tree."""
        if isinstance(item, str):
            return
        if isinstance(item, list):
            for child in item:
                self._collect_referenced_extras(child, extras)
            return
        lhs, op, rhs = item
        lhs_is_extra = isinstance(lhs, Variable) and lhs.value == "extra"
        rhs_is_extra = isinstance(rhs, Variable) and rhs.value == "extra"
        if lhs_is_extra or rhs_is_extra:
            literal = rhs.value if lhs_is_extra else lhs.value
            if isinstance(literal, str):
                extras.add(canonicalize_name(literal))


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        raise TypeError(f"Cannot restore Requirement from {state!r}")
=======
        raise TypeError(f"Cannot restore Requirement from {state!r}")

    @property
    def marker_extras(self) -> frozenset[str]:
        """The set of extra names referenced in this requirement's marker.

        Returns an empty :class:`frozenset` if there is no marker, otherwise
        returns the result of :meth:`Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE