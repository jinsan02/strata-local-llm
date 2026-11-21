### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
from .utils import canonicalize_name
=======
from .utils import NormalizedName, canonicalize_name
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _format_full_version(info: sys._version_info) -> str:
=======
def _collect_referenced_extras(markers: MarkerList) -> set[NormalizedName]:
    found: set[NormalizedName] = set()
    for item in markers:
        if isinstance(item, list):
            found.update(_collect_referenced_extras(item))
        elif isinstance(item, tuple):
            lhs, _op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                found.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                found.add(lhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extras" and isinstance(lhs, Value):
                found.add(lhs.value)
            elif isinstance(lhs, Variable) and lhs.value == "extras" and isinstance(rhs, Value):
                found.add(rhs.value)
    return found


def _format_full_version(info: sys._version_info) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return a frozenset of all extra names referenced in this marker."""
        return frozenset(_collect_referenced_extras(self._markers))


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
    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
        # Only primitives, for stability: the requirement string, then the
        # prereleases overrides that the string cannot hold, for the
        # SpecifierSet and for each specifier in canonical order. Re-parsed
        # on load to reconstruct all other fields.
        specs = self.specifier._canonical_specs()
        return (
            str(self),
            self.specifier._prereleases,
            tuple(s._prereleases for s in specs),
        )

    def __setstate__(self, state: object) -> None:
        inner: object = None
        prereleases: bool | None = None
        if isinstance(state, str):
            # Format (26.2): just the requirement string.
            requirement_string: str = state
        elif (
            isinstance(state, tuple)
            and len(state) in {2, 3}
            and isinstance(state[0], str)
            and (state[1] is None or isinstance(state[1], bool))
        ):
            # Format (26.3): (requirement string, specifier prereleases).
            # Format (26.4+): the same, then a tuple with the prereleases of
            # each specifier in canonical order.
            requirement_string, prereleases = state[:2]
            if len(state) == 3:
                inner = state[2]
        elif isinstance(state, dict) and state.keys() >= set(self.__slots__):
            # Old format (packaging <= 26.1, no __slots__): plain __dict__.
            for key in self.__slots__:
                setattr(self, key, state[key])
            return
        else:
            raise TypeError(f"Cannot restore Requirement from {state!r}")

        try:
            tmp = Requirement(requirement_string)
        except InvalidRequirement as exc:
            raise TypeError(f"Cannot restore Requirement from {state!r}") from exc
        if inner is not None:
            specs = tmp.specifier._canonical_specs()
            if (
                not isinstance(inner, tuple)
                or len(inner) != len(specs)
                or not all(p is None or isinstance(p, bool) for p in inner)
            ):
                raise TypeError(f"Cannot restore Requirement from {state!r}")
            for spec, spec_prereleases in zip(specs, inner, strict=True):
                sp
=======
    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
        # Only primitives, for stability: the requirement string, then the
        # prereleases overrides that the string cannot hold, for the
        # SpecifierSet and for each specifier in canonical order. Re-parsed
        # on load to reconstruct all other fields.
        specs = self.specifier._canonical_specs()
        return (
            str(self),
            self.specifier._prereleases,
            tuple(s._prereleases for s in specs),
        )

    def __setstate__(self, state: object) -> None:
        inner: object = None
        prereleases: bool | None = None
        if isinstance(state, str):
            # Format (26.2): just the requirement string.
            requirement_string: str = state
        elif (
            isinstance(state, tuple)
            and len(state) in {2, 3}
            and isinstance(state[0], str)
            and (state[1] is None or isinstance(state[1], bool))
        ):
            # Format (26.3): (requirement string, specifier prereleases).
            # Format (26.4+): the same, then a tuple with the prereleases of
            # each specifier in canonical order.
            requirement_string, prereleases = state[:2]
            if len(state) == 3:
                inner = state[2]
        elif isinstance(state, dict) and state.keys() >= set(self.__slots__):
            # Old format (packaging <= 26.1, no __slots__): plain __dict__.
            for key in self.__slots__:
                setattr(self, key, state[key])
            return
        else:
            raise TypeError(f"Cannot restore Requirement from {state!r}")

        try:
            tmp = Requirement(requirement_string)
        except InvalidRequirement as exc:
            raise TypeError(f"Cannot restore Requirement from {state!r}") from exc
        if inner is not None:
            specs = tmp.specifier._canonical_specs()
            if (
                not isinstance(inner, tuple)
                or len(inner) != len(specs)
                or not all(p is None or isinstance(p, bool) for p in inner)
            ):
                raise TypeError(f"Cannot restore Requirement from {state!r}")
            for spec, spec_prereleases in zip(specs, inner, strict=True):
                spec._prereleases = spec_prereleases

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """Return a frozenset of all extra names referenced in the marker, if any."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE