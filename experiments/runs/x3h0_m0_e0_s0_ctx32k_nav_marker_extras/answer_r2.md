### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return all extra names referenced in the marker.

        Collects extra names from comparisons with ``extra`` (e.g.,
        ``extra == "foo"``) and membership checks against ``extras``
        (e.g., ``"foo" in extras``). Returns a frozenset of
        :class:`~packaging.utils.NormalizedName`.
        """
        extra_names: set[NormalizedName] = set()

        def _collect(items: MarkerList) -> None:
            for item in items:
                if isinstance(item, list):
                    _collect(item)
                elif isinstance(item, tuple):
                    lhs, _, rhs = item
                    if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                        extra_names.add(canonicalize_name(rhs.value))
                    elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                        extra_names.add(canonicalize_name(lhs.value))
                    elif (
                        isinstance(lhs, Value)
                        and isinstance(rhs, Variable)
                        and rhs.value == "extras"
                    ):
                        extra_names.add(canonicalize_name(lhs.value))

        _collect(self._markers)
        return frozenset(extra_names)


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
              and self.marker == other.marker
          )
>>>>>>> REPLACE