### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _format_full_version(info: sys._version_info) -> str:
=======
def _collect_referenced_extras(marker_list: list) -> set[str]:
    """Collect all canonicalized extra names referenced in a marker tree."""
    extras: set[str] = set()
    for item in marker_list:
        if isinstance(item, list):
            extras |= _collect_referenced_extras(item)
        elif isinstance(item, tuple):
            lhs, _, rhs = item
            # Look for 'extra' or 'extras' variable and extract the literal Value
            if isinstance(lhs, Variable):
                if lhs.value == "extra" and isinstance(rhs, Value):
                    extras.add(rhs.value)
                elif lhs.value == "extras" and isinstance(rhs, Value):
                    extras.add(rhs.value)
            if isinstance(rhs, Variable):
                if rhs.value == "extra" and isinstance(lhs, Value):
                    extras.add(lhs.value)
                elif rhs.value == "extras" and isinstance(lhs, Value):
                    extras.add(lhs.value)
    return extras


def _format_full_version(info: sys._version_info) -> str:
>>>>>>> REPLACE
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return the set of extra names referenced by this marker."""
        return frozenset(_collect_referenced_extras(self._markers))


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
        """The extra names referenced by the requirement's marker, if any."""
        return self.marker.referenced_extras() if self.marker else frozenset()

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
>>>>>>> REPLACE