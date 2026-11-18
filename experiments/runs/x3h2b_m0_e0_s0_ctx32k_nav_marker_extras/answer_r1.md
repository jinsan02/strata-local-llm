### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    def __str__(self) -> str:
        # The parsed tree is private, so its formatted text can be reused.
        if self._serialized is None:
            self._serialized = _format_marker(self._markers)
        return self._serialized
=======
    def referenced_extras(self) -> frozenset["utils.NormalizedName"]:
        """Return a frozenset of extra names referenced in this marker."""
        from .utils import canonicalize_name

        extras: set[str] = set()

        def _collect(markers):
            for marker in markers:
                if isinstance(marker, tuple):
                    lhs, _, rhs = marker

                    # PEP 685: extra comparison (e.g. extra == "foo", "foo" == extra)
                    if isinstance(lhs, Variable) and lhs.value == "extra":
                        if isinstance(rhs, Value):
                            extras.add(rhs.value)
                    elif isinstance(rhs, Variable) and rhs.value == "extra":
                        if isinstance(lhs, Value):
                            extras.add(lhs.value)

                    # PEP 685: membership in extras set (e.g. "foo" in extras)
                    elif isinstance(rhs, Variable) and rhs.value == "extras":
                        if isinstance(lhs, Value):
                            extras.add(lhs.value)
                elif isinstance(marker, list):
                    _collect(marker)

        _collect(self._markers)
        return frozenset(canonicalize_name(name) for name in extras)

    def __str__(self) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        if self.marker:
            yield f"; {self.marker}"

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
=======
    @property
    def marker_extras(self) -> frozenset["utils.NormalizedName"]:
        """Return a frozenset of extra names referenced in this requirement's marker.

        .. versionadded:: 26.4
        """
        from .utils import canonicalize_name

        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __getstate__(self) -> tuple[str, bool | None, tuple[bool | None, ...]]:
>>>>>>> REPLACE