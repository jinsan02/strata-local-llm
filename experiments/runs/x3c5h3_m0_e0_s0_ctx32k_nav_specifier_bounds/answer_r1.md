### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def __contains__(self, item: UnparsedVersion) -> bool:
=======
    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the combined lower and upper bounds of this specifier set.

        Returns a ``(lower, upper)`` tuple where each element is either
        ``None`` or ``(Version, inclusive: bool)``.  The effective bound is
        the intersection of every specifier's contribution.  If any
        ``===`` operator is present a :exc:`ValueError` is raised.

        .. versionadded:: 26.4
        """
        if self._has_arbitrary:
            raise ValueError(
                "Bounds are not defined for specifier sets with '===' operators."
            )

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            lb, ub = _extract_bounds(spec)

            if lb is not None:
                if lower is None or lb[0] > lower[0]:
                    lower = lb
                elif lb[0] == lower[0]:
                    # When versions are equal the non-inclusive side wins.
                    if not lb[1]:
                        lower = lb

            if ub is not None:
                if upper is None or ub[0] < upper[0]:
                    upper = ub
                elif ub[0] == upper[0]:
                    if not ub[1]:
                        upper = ub

        return (lower, upper)


def _extract_bounds(
    spec: Specifier,
) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
    """Derive ``(lower, upper)`` from a single :class:`Specifier`.

    Each element is ``None`` when the specifier imposes no boundary in that
    direction.  ``==V.*`` and ``~=V`` upper-bounds are constructed purely
    from release numbers (epoch retained; pre / post / dev / local absent).
    """
    op, ver_str = spec._spec

    # --- short-circuit for identity equality ---
    if op == "===":
        return (None, None)  # bounds() caller should have rejected it already.

    v = spec._require_spec_version()

    if op == ">=":
        return ((v, True), None)
    if op == ">":
        return ((v, False), None)
    if op == "<=":
        return (None, (v, True))
    if op == "<":
        return (None, (v, False))
    if op == "!=":
        return (None, None)

    # -- equality variants --
    if ver_str.endswith(".*"):
        # ``==V.*``  -> lower V inclusive; upper next-release exclusive.
        release = v.release
        next_release = release[:-1] + (release[-1] + 1,)
        ubound = v.__replace__(
            release=next_release, pre=None, post=None, dev=None, local=None
        )
        return ((v, True), (ubound, False))

    # ``==V``  -> single point [V, V].
    if op == "==":
        return ((v, True), (v, True))

    if op == "~=":
        # ``~=V``  -> lower V inclusive; upper prefix-increment exclusive.
        release = v.release
        # PEP 440 requires at least two components for ~=.
        prefix = release[:-1]
        next_prefix = prefix[:-1] + (prefix[-1] + 1,)
        ubound = v.__replace__(
            release=next_prefix, pre=None, post=None, dev=None, local=None
        )
        return ((v, True), (ubound, False))

    # Fallback for unexpected operators.
    return (None, None)


    def __contains__(self, item: UnparsedVersion) -> bool:
>>>>>>> REPLACE