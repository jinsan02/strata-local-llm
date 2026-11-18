### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return _evaluate_markers(self._markers, environment)


def _pep440_python_full_version(info: sys._version_info) -> str:
=======
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return a frozenset of canonical extra names referenced in this marker."""
        extras: set[str] = set()
        
        def _collect(markers: MarkerList) -> None:
            for node in markers:
                if isinstance(node, list):
                    _collect(node)
                elif isinstance(node, tuple):
                    lhs, op, rhs = node
                    
                    # Check for 'extra' comparisons (e.g., extra == "foo", "foo" == extra)
                    if isinstance(lhs, Variable) and lhs.value == "extra":
                        if isinstance(rhs, Value):
                            extras.add(rhs.value)
                    elif isinstance(rhs, Variable) and rhs.value == "extra":
                        if isinstance(lhs, Value):
                            extras.add(lhs.value)
                            
                    # Check for 'extras' membership (e.g., "foo" in extras, "foo" not in extras)
                    op_str = op.serialize()
                    if op_str in ("in", "not in"):
                        if isinstance(rhs, Variable) and rhs.value == "extras":
                            if isinstance(lhs, Value):
                                extras.add(lhs.value)

        _collect(self._markers)
        return frozenset(canonicalize_name(e) for e in extras)


def _pep440_python_full_version(info: sys._version_info) -> str:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
            and self.marker == other.marker
        )
=======
            and self.marker == other.marker
        )

    @property
    def marker_extras(self) -> frozenset[str]:
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE