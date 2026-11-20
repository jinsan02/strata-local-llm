### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
            raise TypeError(f"Cannot restore Marker from {state!r}")

    def __and__(self, other: Marker) -> Marker:
=======
            raise TypeError(f"Cannot restore Marker from {state!r}")

    def referenced_extras(self) -> frozenset["NormalizedName"]:
        """Return a ``frozenset`` of extra names mentioned in this marker."""

        def _collect(markers: MarkerList) -> set[str]:
            result: set[str] = set()
            for item in markers:
                if isinstance(item, list):
                    result.update(_collect(item))
                elif isinstance(item, tuple):
                    lhs, _op, rhs = item
                    extra_value: str | None = None
                    if (
                        isinstance(lhs, Variable)
                        and lhs.value == "extra"
                        and isinstance(rhs, Value)
                    ):
                        extra_value = rhs.value
                    elif (
                        isinstance(rhs, Variable)
                        and rhs.value == "extra"
                        and isinstance(lhs, Value)
                    ):
                        extra_value = lhs.value
                    elif (
                        isinstance(lhs, Variable)
                        and lhs.value == "extras"
                        and isinstance(rhs, Value)
                    ):
                        extra_value = rhs.value
                    elif (
                        isinstance(rhs, Variable)
                        and rhs.value == "extras"
                        and isinstance(lhs, Value)
                    ):
                        extra_value = lhs.value
                    if extra_value is not None:
                        result.add(canonicalize_name(extra_value))
                # ignore "and"/"or" strings in the list

            return result

        from .utils import NormalizedName

        return frozenset(_collect(self._markers) if self._markers else ())

    def __and__(self, other: Marker) -> Marker:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    @property
    def markers(self) -> list[str]:
        """The environment markers defined in this requirement."""
        return self._markers.split(";") if self.marker else []

    @property
=======
    @property
    def markers(self) -> list[str]:
        """The environment markers defined in this requirement."""
        return self._markers.split(";") if self.marker else []

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the extra names referenced by this requirement's marker."""
        return self.marker.referenced_extras() if self.marker else frozenset()

    @property
>>>>>>> REPLACE