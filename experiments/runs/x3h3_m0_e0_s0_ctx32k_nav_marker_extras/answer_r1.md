### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return the set of all extra names referenced by this marker.

        This method traverses the entire marker expression and returns a
        :class:`frozenset` containing the normalized names of every ``extra``
        used in comparisons (e.g., ``extra == "foo"``) or membership checks
        (e.g., ``"foo" in extras``).

        If the marker does not reference any extras, an empty frozenset is
        returned.

        .. versionadded:: 26.4
        """

        def _extract_extra_names(markers: MarkerList) -> set[str]:
            result: set[str] = set()
            for marker in markers:
                if isinstance(marker, list):
                    result |= _extract_extra_names(marker)
                elif isinstance(marker, tuple):
                    lhs, op, rhs = marker
                    # Check if 'extra' is the key being evaluated against a literal value
                    if (
                        isinstance(lhs, Variable) and lhs.value == "extra"
                    ) or (
                        isinstance(rhs, Variable) and rhs.value == "extra"
                    ):
                        if isinstance(rhs, Value):
                            result.add(rhs.value)
                        elif isinstance(lhs, Value):
                            result.add(lhs.value)
                    # Check for set membership: "<value>" in extras
                    elif (
                        isinstance(rhs, Variable)
                        and rhs.value == "extras"
                        and isinstance(lhs, Value)
                    ):
                        result.add(lhs.value)
                elif marker == "or":
                    continue  # 'or' doesn't add names itself
                elif marker == "and":
                    continue  # 'and' doesn't add names itself
            return result

        return frozenset(_extract_extra_names(self._markers))


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
        if parsed.marker is not None:
            self.marker = Marker.__new__(Marker)
            self.marker._markers = _normalize_extra_values(parsed.marker)
            self.marker._serialized = None

    def __replace__(
=======
        if parsed.marker is not None:
            self.marker = Marker.__new__(Marker)
            self.marker._markers = _normalize_extra_values(parsed.marker)
            self.marker._serialized = None

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """The extra names referenced by the requirement's marker.

        Returns an empty set if there is no marker, or if the marker does not
        reference any extras.

        .. versionadded:: 26.4
        """
        return self.marker.referenced_extras() if self.marker else frozenset()

    def __replace__(
>>>>>>> REPLACE