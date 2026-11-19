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


def _pep440_python_full_version(python_full_version: str) -> str:
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
        """Return a frozenset of extra names referenced in the marker.

        Scans all comparisons for ``extra == "x"``, ``"x" == extra``, and
        ``"x" in extras`` forms, extracting and normalizing every extra name.
        Nested markers via ``&``/``|`` are handled recursively.

        .. versionadded:: NEXT_VERSION
        """
        extracted: set[str] = set()
        self._extract_extras(self._markers, extracted)
        return frozenset(canonicalize_name(n) for n in extracted)

    @staticmethod
    def _extract_extras(markers: MarkerList, extras: set[str]) -> None:
        """Recursively collect extra names from a parsed marker tree."""
        for part in markers:
            if isinstance(part, list):
                Marker._extract_extras(part, extras)
            elif isinstance(part, tuple):
                lhs, _op, rhs = part
                # extra == "x"  OR  "x" == extra
                if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                    extras.add(rhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                    extras.add(lhs.value)
            # 'and', 'or', and other non-comparison items are ignored


def _pep440_python_full_version(python_full_version: str) -> str:
>>>>>>> REPLACE