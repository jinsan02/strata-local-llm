### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    return _repair_python_full_version(current_environment)


class Marker:
=======
    return _repair_python_full_version(current_environment)


def _collect_extra_names(markers: MarkerList) -> frozenset[NormalizedName]:
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, list):
            extras |= _collect_extra_names(item)
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            # Extra comparisons: extra == "x" or "x" == extra
            if isinstance(lhs, Variable) and lhs.value == "extra":
                extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                extras.add(lhs.value)
            # Membership tests: "x" in extras / "x" not in extras
            elif isinstance(lhs, Value) and isinstance(rhs, Variable) and rhs.value == "extras":
                extras.add(lhs.value)
    return frozenset(cast(NormalizedName, name) for name in extras)


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

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in the marker expression.

        This method looks at all comparisons involving the ``extra`` variable and all
        membership tests on the ``extras`` set (e.g., ``"x" in extras``, ``"x" not in extras``).
        Names are returned in their canonicalized form. If the marker does not reference
        any extras, an empty :py:class:`frozenset` is returned.

        .. versionadded:: 26.5
        """
        return _collect_extra_names(self._markers)

    def evaluate(
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def _iter_parts(self, name: str) -> Iterator[str]:
        yield name
=======
    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in the marker.

        Returns an empty :py:class:`frozenset` if no marker is set, otherwise
        delegates to :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def _iter_parts(self, name: str) -> Iterator[str]:
        yield name
>>>>>>> REPLACE