### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return all extras referenced in this marker as a frozen set of normalized names.

        Scans the entire marker expression (including nested ``and``/``or`` and
        parenthesized groups) for comparisons against the ``extra`` variable or
        membership tests like ``"foo" in extras`` / ``"foo" not in extras``.
        """
        result: set[str] = set()

        def _collect(markers: MarkerList) -> None:
            for m in markers:
                if isinstance(m, list):
                    _collect(m)
                elif isinstance(m, tuple):
                    lhs, op, rhs = m
                    # extra == "value" or "value" == extra
                    if isinstance(lhs, Variable) and lhs.value == "extra":
                        if isinstance(rhs, Value):
                            result.add(canonicalize_name(rhs.value))
                    elif isinstance(rhs, Variable) and rhs.value == "extra":
                        if isinstance(lhs, Value):
                            result.add(canonicalize_name(lhs.value))
                    # "value" in extras
                    elif isinstance(lhs, Value) and rhs.value == "extras":
                        result.add(canonicalize_name(lhs.value))
                # 'and', 'or' are ignored

        _collect(self._markers)
        return frozenset(result)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
from .markers import Marker, _normalize_extra_values
=======
from .markers import Marker, _normalize_extra_values
from .utils import NormalizedName
>>>>>>> REPLACE

<<<<<<< SEARCH
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Requirement):
            return NotImplemented

        # Extras must be normalized before comparison as per PEP 685.
        self_extras = frozenset(canonicalize_name(e) for e in self.extras)
        other_extras = frozenset(canonicalize_name(e) for e in other.extras)
        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self_extras == other_extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )
=======
    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Extras referenced in the marker.

        Returns an empty frozenset if there is no marker, otherwise
        returns the result of :meth:`~packaging.markers.Marker.referenced_extras`.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Requirement):
            return NotImplemented

        # Extras must be normalized before comparison as per PEP 685.
        self_extras = frozenset(canonicalize_name(e) for e in self.extras)
        other_extras = frozenset(canonicalize_name(e) for e in other.extras)
        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self_extras == other_extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )
>>>>>>> REPLACE