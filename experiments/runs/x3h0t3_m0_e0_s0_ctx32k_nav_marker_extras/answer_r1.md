### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
          return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
          return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return a frozenset of normalized extra names referenced in the marker."""
        extras: set[str] = set()

        def _walk(tree: MarkerList) -> None:
            for node in tree:
                if isinstance(node, list):
                    _walk(node)
                elif isinstance(node, tuple):
                    lhs, _, rhs = node
                    # Extra comparisons: extra == "x", "x" == extra
                    if isinstance(lhs, Variable) and lhs.value == "extra":
                        if isinstance(rhs, Value):
                            extras.add(rhs.value)
                    elif isinstance(rhs, Variable) and rhs.value == "extra":
                        if isinstance(lhs, Value):
                            extras.add(lhs.value)
                    # Set membership: "x" in extras, "x" not in extras
                    elif isinstance(rhs, Variable) and rhs.value == "extras":
                        if isinstance(lhs, Value):
                            extras.add(lhs.value)
                    elif isinstance(lhs, Variable) and lhs.value == "extras":
                        if isinstance(rhs, Value):
                            extras.add(rhs.value)

        _walk(self._markers)
        return frozenset(extras)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
              and self.url == other.url
              and self.marker == other.marker
          )
=======
              and self.url == other.url
              and self.marker == other.marker
          )

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return the normalized extra names referenced in the requirement's marker."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE