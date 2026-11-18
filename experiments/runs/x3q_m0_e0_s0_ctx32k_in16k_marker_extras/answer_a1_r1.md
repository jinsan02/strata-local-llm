<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(python_full_version: str) -> str:
=======
    def referenced_extras(self) -> frozenset[str]:
        """Return a frozenset of normalized extra names referenced in this marker."""
        collected: set[str] = set()

        def _walk(nodes: MarkerList) -> None:
            for node in nodes:
                if isinstance(node, list):
                    _walk(node)
                elif isinstance(node, tuple):
                    lhs, _, rhs = node
                    if isinstance(lhs, Variable) and lhs.value in ("extra", "extras"):
                        if isinstance(rhs, Value):
                            collected.add(canonicalize_name(rhs.value))
                    elif isinstance(rhs, Variable) and rhs.value in ("extra", "extras"):
                        if isinstance(lhs, Value):
                            collected.add(canonicalize_name(lhs.value))

        _walk(self._markers)
        return frozenset(collected)


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE

<<<<<<< SEARCH
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Requirement):
            return NotImplemented

        # Extras must be normalized before comparison as per PEP 685.
=======
    @property
    def marker_extras(self) -> frozenset[str]:
        """Extra names referenced by the requirement's marker."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __eq__(self, other: object) -> bool:
>>>>>>> REPLACE