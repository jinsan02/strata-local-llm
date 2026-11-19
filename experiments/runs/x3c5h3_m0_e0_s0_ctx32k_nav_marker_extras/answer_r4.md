### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    def evaluate(
        self,
        environment: Mapping[str, str | AbstractSet[str]] | None = None,
        context: EvaluateContext = "metadata",
    ) -> bool:
=======
    def referenced_extras(self) -> frozenset[str]:
        """Return all extra names referenced in this marker.

        Scans the marker expression for comparisons against ``extra`` or the
        ``extras`` list (e.g., ``extra == "foo"`` or ``"bar" in extras``).
        Returns a :class:`frozenset` of normalized extra names, or an empty set
        if no extras are referenced.

        .. versionadded:: 26.5
        """
        found: set[str] = set()

        def _visit(node: MarkerAtom | MarkerLogical) -> None:
            if isinstance(node, list):
                for item in node:
                    _visit(item)
            elif isinstance(node, tuple):
                lhs, op, rhs = node
                # Handle extra == "x" or "x" == extra
                if (isinstance(lhs, Variable) and lhs.value == "extra"
                        and isinstance(rhs, Value)):
                    found.add(canonicalize_name(rhs.value))
                elif (isinstance(rhs, Variable) and rhs.value == "extra"
                        and isinstance(lhs, Value)):
                    found.add(canonicalize_name(lhs.value))
                # Handle "x" in extras (extras is a list/set variable)
                elif isinstance(rhs, Variable) and rhs.value == "extras" and isinstance(lhs, Value):
                    found.add(canonicalize_name(lhs.value))

        _visit(self._markers)
        return frozenset(found)

    def evaluate(
        self,
        environment: Mapping[str, str | AbstractSet[str]] | None = None,
        context: EvaluateContext = "metadata",
    ) -> bool:
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
      and self.marker == other.marker
          )

    def __str__(self) -> str:
=======
    @property
    def marker_extras(self) -> frozenset[str]:
        """Return extra names referenced in this requirement's marker.
        
        If there is no marker, returns an empty :class:`frozenset`.
        
        .. versionadded:: 26.5
        """
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()

    def __str__(self) -> str:
>>>>>>> REPLACE