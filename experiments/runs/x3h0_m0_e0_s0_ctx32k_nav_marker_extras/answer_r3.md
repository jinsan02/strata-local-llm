### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    return any(all(item) for item in groups)


def _format_full_version(info: sys._version_info) -> str:
=======
    return any(all(item) for item in groups)


def _referenced_extras(markers: MarkerList) -> list[str]:
    extras_names: set[str] = set()
    for marker in markers:
        if isinstance(marker, list):
            extras_names.update(_referenced_extras(marker))
        elif isinstance(marker, tuple):
            lhs, _op, rhs = marker
            if isinstance(lhs, Variable) and lhs.value == "extra":
                extras_names.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                extras_names.add(lhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extras" and isinstance(lhs, Value):
                extras_names.add(lhs.value)
    return list(extras_names)


def _format_full_version(info: sys._version_info) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in this marker.

        Scans the entire marker tree (including nested ``and`` / ``or`` and
        parenthesised sub-expressions) for every comparison or membership test
        that involves an *extra*.  The returned set contains the *normalised*
        (PEP 503 / PEP 685 canonical) names.

        Returns
        -------
        frozenset[NormalizedName]
            A frozen set of normalised extra name strings.  If the marker does
            not reference any extras, an empty frozenset is returned.

        .. versionadded:: 26.4
        """
        return frozenset(_referenced_extras(self._markers))


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
            and self.url == other.url
            and self.marker == other.marker
        )
=======
            and self.url == other.url
            and self.marker == other.marker
        )

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in this requirement's marker.

        Equivalent to calling :meth:`packaging.markers.Marker.referenced_extras`
        on :attr:`marker`, or an empty :class:`frozenset` if no marker is set.

        .. versionadded:: 26.4
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE