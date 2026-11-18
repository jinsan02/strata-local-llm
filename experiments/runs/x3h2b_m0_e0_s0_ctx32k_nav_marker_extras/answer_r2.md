### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
      return any(all(item) for item in groups)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
      return any(all(item) for item in groups)


def _referenced_extras(markers: MarkerList) -> frozenset[str]:
    """Recursively collect all normalized extra names from a marker list."""
    extras: set[str] = set()
    for part in markers:
        if isinstance(part, list):
            extras |= _referenced_extras(part)
        elif isinstance(part, tuple):
            lhs, op, rhs = part
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extras.add(lhs.value)
    return frozenset(extras)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        if self.marker:
            yield f"; {self.marker}"

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
=======
        if self.marker:
            yield f"; {self.marker}"

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return all extra names referenced in this requirement's marker.

        Returns an empty :class:`~typing.FrozenSet` if there is no marker.
        """
        return self.marker.referenced_extras() if self.marker else frozenset()

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
>>>>>>> REPLACE