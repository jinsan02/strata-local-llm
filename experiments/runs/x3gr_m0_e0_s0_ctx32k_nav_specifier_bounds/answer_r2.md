EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
def _apply_prereleases_filter(
    matches: Iterable[Any],
    key: Callable[[Any], UnparsedVersion] | None,
    prereleases: bool | None,
) -> Iterator[Any]:
    """Apply ``prereleases=`` handling to an already-matched iterable.

    ``None`` means PEP 440 default (buffer pre-releases until a final
    appears); ``True`` yields everything; ``False`` drops pre-releases.
    """
    if prereleases is None:
        return _pep440_filter_prereleases(matches, key)
    if prereleases:
        return iter(matches)
    return (
        item
        for item in matches
        if (parsed := coerce_version(item if key is None else key(item))) is None
        or not parsed.is_prerelease
    )


class SpecifierSet(BaseSpecifier):
=======
def _apply_prereleases_filter(
    matches: Iterable[Any],
    key: Callable[[Any], UnparsedVersion] | None,
    prereleases: bool | None,
) -> Iterator[Any]:
    """Apply ``prereleases=`` handling to an already-matched iterable.

    ``None`` means PEP 440 default (buffer pre-releases until a final
    appears); ``True`` yields everything; ``False`` drops pre-releases.
    """
    if prereleases is None:
        return _pep440_filter_prereleases(matches, key)
    if prereleases:
        return iter(matches)
    return (
        item
        for item in matches
        if (parsed := coerce_version(item if key is None else key(item))) is None
        or not parsed.is_prerelease
    )


def _specifier_bounds(
    spec: Specifier,
) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
    """Return ``(lower, upper)`` bounds for a single specifier.

    Each bound is ``None`` (unbounded) or ``(Version, inclusive: bool)``.
    Raises ``ValueError`` for ``===``.
    """
    op, ver_str = spec._spec
    if op == "===":
        raise ValueError("=== operator is not supported in bounds()")

    ver = spec._require_spec_version()

    if op == ">=":
        return ((ver, True), None)
    if op == ">":
        return ((ver, False), None)
    if op == "<=":
        return (None, (ver, True))
    if op == "<":
        return (None, (ver, False))
    if op == "==":
        if ver_str.endswith(".*"):
            # Wildcard: lower (ver, True), upper (next_release(ver), False)
            new_rel = ver.release[:-1] + (ver.release[-1] + 1,)
            upper_ver = Version(f"{ver.epoch}." + ".".join(str(x) for x in new_rel))
            return ((ver, True), (upper_ver, False))
        else:
            return ((ver, True), (ver, True))
    if op == "~=":
        # Compatible: lower (ver, True), upper (next_release(ver), False)
        rel = ver.release
        if len(rel) == 1:
            new_rel = (rel[0] + 1,)
        else:
            new_rel = rel[:-1] + (rel[-2] + 1,)
        upper_ver = Version(f"{ver.epoch}." + ".".join(str(x) for x in new_rel))
        return ((ver, True), (upper_ver, False))
    if op == "!=":
        return (None, None)
    return (None, None)


class SpecifierSet(BaseSpecifier):
>>>>>>> REPLACE

EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def __iter__(self) -> Iterator[Specifier]:
        """
        Returns an iterator over all the underlying :class:`Specifier` instances
        in this specifier set.

        >>> sorted(SpecifierSet(">=1.0.0,!=1.0.1"), key=str)
        [<Specifier('!=1.0.1')>, <Specifier('>=1.0.0')>]
        """
        return iter(self._specs)

    def _get_ranges(self) -> Sequence[Interval]:
=======
    def __iter__(self) -> Iterator[Specifier]:
        """
        Returns an iterator over all the underlying :class:`Specifier` instances
        in this specifier set.

        >>> sorted(SpecifierSet(">=1.0.0,!=1.0.1"), key=str)
        [<Specifier('!=1.0.1')>, <Specifier('>=1.0.0')>]
        """
        return iter(self._specs)

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the ``(lower, upper)`` bounds of this specifier set.

        Each bound is ``None`` (unbounded) or ``(Version, inclusive: bool)``.
        Raises ``ValueError`` if any specifier uses ``===``.
        Prerelease settings do not affect the result.
        """
        if self._has_arbitrary:
            raise ValueError("=== operator is not supported in bounds()")

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            l, u = _specifier_bounds(spec)

            if l is not None:
                if lower is None:
                    lower = l
                elif (l[0], 0 if l[1] else 1) > (lower[0], 0 if lower[1] else 1):
                    lower = l

            if u is not None:
                if upper is None:
                    upper = u
                elif (u[0], 1 if u[1] else 0) < (upper[0], 1 if upper[1] else 0):
                    upper = u

        return lower, upper

    def _get_ranges(self) -> Sequence[Interval]:
>>>>>>> REPLACE