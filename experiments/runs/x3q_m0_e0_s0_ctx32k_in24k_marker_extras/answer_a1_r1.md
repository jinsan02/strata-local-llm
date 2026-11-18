### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
    def evaluate_prepared(
        self, environment: Mapping[str, str | AbstractSet[str]]
    ) -> bool:
        """Evaluate a marker against the supplied environment.

        ``environment`` is read as given: unlike :meth:`evaluate`, no detected
        values are filled in, no context keys are added, ``extra`` is not
        canonicalized and ``python_full_version`` is not repaired. The mapping
        may come from :func:`prepare_environment` or be supplied by the caller.
        If changing ``extra`` between evaluations, normalize its value with
        :func:`packaging.utils.canonicalize_name` first.

        :param environment: The environment to evaluate against, normally from
            :func:`prepare_environment`.
        :raises UndefinedComparison: If the marker uses a comparison on values
            that are not valid versions per the :ref:`specification of version
            specifiers <pypug:dependency-specifiers>`, or ``extra`` holds
            something other than a string or a set, or a set of extras is used
            with an operator other than ``==`` or ``!=``, or a set-valued marker
            is given a string or used on the left-hand side of a comparison.
        :raises UndefinedEnvironmentName: If the marker references a value that
            is missing from ``environment``.
        :returns: ``True`` if the marker matches, otherwise ``False``.

        >>> from packaging.markers import Marker, prepare_environment
        >>> environment = prepare_environment({"sys_platform": "linux"})
        >>> Marker("sys_platform == 'linux'").evaluate_prepared(environment)
        True

        .. versionadded:: 26.4
        """
        return _evaluate_markers(self._markers, environment)
=======
    def evaluate_prepared(
        self, environment: Mapping[str, str | AbstractSet[str]]
    ) -> bool:
        """Evaluate a marker against the supplied environment.

        ``environment`` is read as given: unlike :meth:`evaluate`, no detected
        values are filled in, no context keys are added, ``extra`` is not
        canonicalized and ``python_full_version`` is not repaired. The mapping
        may come from :func:`prepare_environment` or be supplied by the caller.
        If changing ``extra`` between evaluations, normalize its value with
        :func:`packaging.utils.canonicalize_name` first.

        :param environment: The environment to evaluate against, normally from
            :func:`prepare_environment`.
        :raises UndefinedComparison: If the marker uses a comparison on values
            that are not valid versions per the :ref:`specification of version
            specifiers <pypug:dependency-specifiers>`, or ``extra`` holds
            something other than a string or a set, or a set of extras is used
            with an operator other than ``==`` or ``!=``, or a set-valued marker
            is given a string or used on the left-hand side of a comparison.
        :raises UndefinedEnvironmentName: If the marker references a value that
            is missing from ``environment``.
        :returns: ``True`` if the marker matches, otherwise ``False``.

        >>> from packaging.markers import Marker, prepare_environment
        >>> environment = prepare_environment({"sys_platform": "linux"})
        >>> Marker("sys_platform == 'linux'").evaluate_prepared(environment)
        True

        .. versionadded:: 26.4
        """
        return _evaluate_markers(self._markers, environment)

    def referenced_extras(self) -> frozenset[str]:
        """Return a frozenset of normalized extra names referenced in this marker.

        Extracts all extra names from comparisons with ``extra`` (e.g. ``extra == "x"``)
        or set membership checks (e.g. ``"x" in extras``). Returns an empty frozenset
        if no extras are used. The result is always canonicalized per PEP 685.
        """
        extras: set[str] = set()

        def _collect(markers: list) -> None:
            for item in markers:
                if isinstance(item, tuple):
                    lhs, op, rhs = item
                    candidate: object | None = None
                    if isinstance(lhs, Variable) and lhs.value in ("extra", "extras"):
                        candidate = rhs
                    elif isinstance(rhs, Variable) and rhs.value in ("extra", "extras"):
                        candidate = lhs
                    
                    if candidate is not None:
                        name = getattr(candidate, 'value', None)
                        if isinstance(name, str):
                            extras.add(canonicalize_name(name))
                elif isinstance(item, list):
                    _collect(item)

        _collect(self._markers)
        return frozenset(extras)
>>>>>>> REPLACE
```

### EDIT: src/packaging/requirements.py
<<<<<<< SEARCH
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Requirement):
            return NotImplemented

        # Extras must be normalized before comparison as per PEP 685.
        self_extras = frozenset(canonicalize_name(e) for e in self.extras)
        other_extras = frozenset(canonicalize_name(e) for e in other.extras)
        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self_extras == other_extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )
=======
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Requirement):
            return NotImplemented

        # Extras must be normalized before comparison as per PEP 685.
        self_extras = frozenset(canonicalize_name(e) for e in self.extras)
        other_extras = frozenset(canonicalize_name(e) for e in other.extras)
        return (
            canonicalize_name(self.name) == canonicalize_name(other.name)
            and self_extras == other_extras
            and self.specifier == other.specifier
            and self.url == other.url
            and self.marker == other.marker
        )

    @property
    def marker_extras(self) -> frozenset[str]:
        """Return normalized extra names referenced in this requirement's marker."""
        if self.marker is None:
            return frozenset()
        return self.marker.referenced_extras()
>>>>>>> REPLACE