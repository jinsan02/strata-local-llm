### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    def evaluate(self, environment: Mapping[str, str | AbstractSet[str]] | None = None) -> bool:
        """Evaluate the marker against the given environment.
        
        If environment is None, the current environment is used.
        """
        if environment is None:
            environment = default_environment()
        
        environment_key: str
        environment_value: str | AbstractSet[str]
        groups: list[list[bool]] = [[]]
        
        for marker in self._markers:
            if isinstance(marker, tuple):
                lhs, op, rhs = marker
                environment_key = lhs.value if isinstance(lhs, Variable) else rhs.value
                if environment_key not in environment:
                    raise UndefinedEnvironmentName(
                        f"Unknown environment name {environment_key!r}"
                    )
                environment_value = environment[environment_key]
                
                if isinstance(lhs, Variable):
                    lhs_value = environment_value
                    rhs_value = rhs.value if isinstance(rhs, Value) else rhs
                else:
                    lhs_value = lhs.value if isinstance(lhs, Value) else lhs
                    rhs_value = environment_value
                
                if environment_key in MARKERS_ALLOWING_SET:
                    if not isinstance(rhs_value, (list, tuple, set)):
                        raise UndefinedComparison(
                            f"Set-valued marker {environment_key!r} can only be used "
                            f'with the membership form (e.g. "<name>" in '
                            f"{environment_key}); it cannot appear on the left-hand "
                            f"side of {op.serialize()!r}."
                        )
                    lhs_value, rhs_value = _normalize(lhs_value, rhs_value, key=environment_key)
                    groups[-1].append(_eval_op(lhs_value, op, rhs_value, key=environment_key))
                elif marker == "or":
                    groups.append([])
                elif marker == "and":
                    pass
                else:  # pragma: nocover
                    raise TypeError(f"Unexpected marker {marker!r}")
        
        return any(all(item) for item in groups)
=======
    def evaluate(self, environment: Mapping[str, str | AbstractSet[str]] | None = None) -> bool:
        """Evaluate the marker against the given environment.
        
        If environment is None, the current environment is used.
        """
        if environment is None:
            environment = default_environment()
        
        environment_key: str
        environment_value: str | AbstractSet[str]
        groups: list[list[bool]] = [[]]
        
        for marker in self._markers:
            if isinstance(marker, tuple):
                lhs, op, rhs = marker
                environment_key = lhs.value if isinstance(lhs, Variable) else rhs.value
                if environment_key not in environment:
                    raise UndefinedEnvironmentName(
                        f"Unknown environment name {environment_key!r}"
                    )
                environment_value = environment[environment_key]
                
                if isinstance(lhs, Variable):
                    lhs_value = environment_value
                    rhs_value = rhs.value if isinstance(rhs, Value) else rhs
                else:
                    lhs_value = lhs.value if isinstance(lhs, Value) else lhs
                    rhs_value = environment_value
                
                if environment_key in MARKERS_ALLOWING_SET:
                    if not isinstance(rhs_value, (list, tuple, set)):
                        raise UndefinedComparison(
                            f"Set-valued marker {environment_key!r} can only be used "
                            f'with the membership form (e.g. "<name>" in '
                            f"{environment_key}); it cannot appear on the left-hand "
                            f"side of {op.serialize()!r}."
                        )
                    lhs_value, rhs_value = _normalize(lhs_value, rhs_value, key=environment_key)
                    groups[-1].append(_eval_op(lhs_value, op, rhs_value, key=environment_key))
                elif marker == "or":
                    groups.append([])
                elif marker == "and":
                    pass
                else:  # pragma: nocover
                    raise TypeError(f"Unexpected marker {marker!r}")
        
        return any(all(item) for item in groups)

    def referenced_extras(self) -> frozenset[NormalizedName]:
        """Return the set of extra names referenced in this marker.
        
        Returns a frozenset of normalized extra names that are compared against
        the ``extra`` variable or appear in ``"x" in extras`` / ``"x" not in extras``
        expressions within the marker.
        """
        return frozenset(_extract_referenced_extras(self._markers))
>>>>>>> REPLACE

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def marker(self) -> Marker | None:
        """The :class:`Marker` for this requirement, or ``None`` if not provided."""
        return self._marker
=======
    @property
    def marker(self) -> Marker | None:
        """The :class:`Marker` for this requirement, or ``None`` if not provided."""
        return self._marker

    @property
    def marker_extras(self) -> frozenset[NormalizedName]:
        """The extra names referenced in this requirement's marker.
        
        Returns an empty frozenset if there is no marker.
        """
        if self._marker is None:
            return frozenset()
        return self._marker.referenced_extras()
>>>>>>> REPLACE