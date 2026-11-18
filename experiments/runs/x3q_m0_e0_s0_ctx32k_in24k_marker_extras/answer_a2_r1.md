### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return a frozenset of normalized extra names referenced in this marker.

        Returns all extra names used in comparisons with ``extra`` (e.g. ``extra == "x"``)
        or membership checks against ``extras`` (e.g. ``"x" in extras``). The result is
        always canonicalized. If no extras are referenced, returns an empty frozenset.
        """
        found_extras: set[str] = set()

        def _visit(node: MarkerAtom | MarkerLogical) -> None:
            if isinstance(node, list):
                for item in node:
                    _visit(item)
            elif isinstance(node, tuple):
                lhs, op, rhs = node
                if not (isinstance(lhs, Value) or isinstance(rhs, Value)):
                    # Neither side is a literal value string, skip.
                    return

                candidate_var: Variable | None = None
                candidate_val: Value | None = None

                if isinstance(lhs, Variable) and lhs.value in ("extra", "extras"):
                    candidate_var = lhs
                    candidate_val = rhs
                elif isinstance(rhs, Variable) and rhs.value in ("extra", "extras"):
                    candidate_var = rhs
                    candidate_val = lhs

                if candidate_val is not None:
                    found_extras.add(canonicalize_name(candidate_val.value))

        _visit(self._markers)
        return frozenset(found_extras)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
        self.url == other.url
        and self.marker == other.marker
    )
=======
        self.url == other.url
        and self.marker == other.marker
    )

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return normalized extra names referenced in this requirement's marker."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE