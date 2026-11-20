### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _splice_operand(markers: MarkerList, op: MarkerLogical) -> MarkerList:
=======
def _collect_extras(markers: MarkerList) -> frozenset[NormalizedName]:
    result: set[NormalizedName] = set()
    for item in markers:
        if isinstance(item, list):
            result |= _collect_extras(item)
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            is_extra_lhs = isinstance(lhs, Variable) and lhs.value == "extra"
            is_extra_rhs = isinstance(rhs, Variable) and rhs.value == "extra"
            is_extras_lhs = isinstance(lhs, Variable) and lhs.value == "extras"
            is_extras_rhs = isinstance(rhs, Variable) and rhs.value == "extras"

            if is_extra_lhs or is_extra_rhs:
                value_node = rhs if is_extra_lhs else lhs
                if isinstance(value_node, Value):
                    result.add(canonicalize_name(value_node.value))
            elif (is_extras_lhs or is_extras_rhs) and op.serialize() in ("in", "not in"):
                value_node = lhs if is_extras_rhs else rhs
                if isinstance(value_node, Value):
                    result.add(canonicalize_name(value_node.value))
    return frozenset(result)


def _splice_operand(markers: MarkerList, op: MarkerLogical) -> MarkerList:
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in this marker.

        Walks the parsed marker tree and collects every extra name that appears
        in any comparison involving ``extra`` or ``extras`` membership checks.
        Returns a frozen set of canonicalized names.

        .. versionadded:: 26.5
        """
        return _collect_extras(self._markers)


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
            self.marker._serialized = None

    def __replace__(
=======
            self.marker._serialized = None

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in the requirement's marker.

        If the requirement has no marker, returns an empty ``frozenset``.
        Otherwise delegates to :meth:`~packaging.markers.Marker.referenced_extras`.

        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __replace__(
>>>>>>> REPLACE