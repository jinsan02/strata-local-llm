### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return all extra names referenced in this marker."""
        result: set[str] = set()

        def _traverse(markers: MarkerList) -> None:
            for item in markers:
                if isinstance(item, str):
                    continue
                if isinstance(item, list):
                    _traverse(item)
                elif isinstance(item, tuple):
                    lhs, op, rhs = item
                    extra_name: str | None = None
                    if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                        extra_name = rhs.value
                    elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                        extra_name = lhs.value
                    elif isinstance(rhs, Variable) and rhs.value in ("extras",) and isinstance(lhs, Value):
                        extra_name = lhs.value

                    if extra_name is not None:
                        result.add(canonicalize_name(extra_name))

        _traverse(self._markers)
        return frozenset(result)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        return result

    def _iter_parts(self, name: str) -> Iterator[str]:
=======
        return result

    @property
    def marker_extras(self) -> frozenset[str]:
        """Extra names referenced by this requirement's marker."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def _iter_parts(self, name: str) -> Iterator[str]:
>>>>>>> REPLACE