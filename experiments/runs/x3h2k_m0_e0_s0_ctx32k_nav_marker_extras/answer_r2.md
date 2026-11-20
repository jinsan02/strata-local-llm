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
        """Return the set of extras referenced in this marker.

        This includes all extra names used in comparisons like
        ``extra == "x"``, ``"x" == extra``, ``"x" in extras``, etc.
        The names are returned in their normalized form.
        """
        extras: set[NormalizedName] = set()

        def _visit(node: MarkerAtom | MarkerLogical) -> None:
            if isinstance(node, list):
                for item in node:
                    _visit(item)
            elif isinstance(node, str):
                return
            elif isinstance(node, tuple):
                lhs, op, rhs = node
                # Check for extra comparisons
                # Case 1: extra == "name" or extra != "name"
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extras.add(rhs.value)
                # Case 2: "name" == extra or "name" != extra
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extras.add(lhs.value)
                # Case 3: "name" in extras or "name" not in extras
                elif isinstance(rhs, Variable) and rhs.value == "extras":
                    if isinstance(lhs, Value):
                        extras.add(lhs.value)
                # Case 4: extras == "name" (rare but possible)
                elif isinstance(lhs, Variable) and lhs.value == "extras":
                    if isinstance(rhs, Value):
                        extras.add(rhs.value)

        _visit(self._markers)
        return frozenset(extras)


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
            raise TypeError(f"Cannot restore Requirement from {state!r}")

    def _iter_parts(self, name: str) -> Iterator[str]:
=======
            raise TypeError(f"Cannot restore Requirement from {state!r}")

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """The set of extras referenced in the requirement's marker.

        Returns an empty frozenset if the marker is ``None``.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def _iter_parts(self, name: str) -> Iterator[str]:
>>>>>>> REPLACE