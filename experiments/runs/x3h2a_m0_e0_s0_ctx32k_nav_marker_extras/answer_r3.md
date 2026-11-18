### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
        return self._from_markers(_join_markers(self._markers, "or", other._markers))

    def evaluate(
=======
        return self._from_markers(_join_markers(self._markers, "or", other._markers))

    def referenced_extras(self) -> frozenset[str]:
        """Return a frozenset of normalized extra names referenced in the marker.
        
        Scans the marker expression for comparisons involving the ``extra`` or
        ``extras`` variables (e.g., ``extra == "foo"``, ``"foo" in extras``) and
        returns the canonicalized extra names found.
        """
        refs: set[str] = set()

        def _visit(node):
            if isinstance(node, list):
                for item in node:
                    _visit(item)
            elif isinstance(node, tuple):
                lhs, op, rhs = node
                var_side = None
                val_side = None

                if isinstance(lhs, Variable):
                    if lhs.value in ("extra", "extras"):
                        var_side = lhs
                        val_side = rhs
                elif isinstance(rhs, Variable):
                    if rhs.value in ("extra", "extras"):
                        var_side = rhs
                        val_side = lhs

                if var_side is not None and isinstance(val_side, Value):
                    refs.add(canonicalize_name(val_side.value))

        _visit(self._markers)
        return frozenset(refs)

    def evaluate(
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
        """Return a frozenset of normalized extra names referenced in the marker.
        
        Returns an empty frozenset if there is no marker.
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE