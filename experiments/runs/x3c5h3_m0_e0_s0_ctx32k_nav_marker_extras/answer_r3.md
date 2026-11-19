### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _evaluate_markers(
    markers: MarkerList, environment: Mapping[str, str | AbstractSet[str]]
) -> bool:
=======
def _extract_referenced_extras(markers: MarkerList) -> frozenset[str]:
    """Collect all extra names referenced in a parsed marker tree."""
    extras: set[str] = set()

    def _recurse(items: list[object]) -> None:
        for item in items:
            if isinstance(item, list):
                _recurse(item)
            elif isinstance(item, tuple):
                lhs, op, rhs = item
                # Check extra == "name" or "name" == extra
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    extras.add(rhs.value)  # type: ignore[arg-type]
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    extras.add(lhs.value)  # type: ignore[arg-type]
                # Check "name" in extras / "name" not in extras
                elif isinstance(rhs, Variable) and rhs.value == "extras":
                    extras.add(lhs.value)  # type: ignore[arg-type]

    _recurse(markers)
    return frozenset(extras)


def _evaluate_markers(
    markers: MarkerList, environment: Mapping[str, str | AbstractSet[str]]
) -> bool:
>>>>>>> REPLACE

### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        .. versionadded:: 26.4
        """
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(info: sys._version_info) -> str:
=======
        .. versionadded:: 26.4
        """
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset["NormalizedName"]:
        """Return a frozenset of extra names referenced in this marker."""
        from .utils import NormalizedName

        return frozenset(
            NormalizedName(name) for name in _extract_referenced_extras(self._markers)
        )


def _pep440_python_full_version(info: sys._version_info) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
              canonicalize_name(self.name) == canonicalize_name(other.name)
              and self_extras == other_extras
              and self.specifier == other.specifier
              and self.url == other.url
              and self.marker == other.marker
          )
=======
              canonicalize_name(self.name) == canonicalize_name(other.name)
              and self_extras == other_extras
              and self.specifier == other.specifier
              and self.url == other.url
              and self.marker == other.marker
          )

    @property
    def marker_extras(self) -> frozenset["NormalizedName"]:
        """Return referenced extras from this requirement's marker, or an empty set if no marker."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE