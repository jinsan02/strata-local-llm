### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
from ._ranges import (
    FULL_RANGE,
    _base_dev0,
    _next_prefix_dev0,
    bounds_for_spec,
    coerce_version,
    filter_by_ranges,
    intersect_specifier_bounds,
    matches_bounds_only,
    ranges_are_prerelease_only,
    resolve_prereleases,
)
=======
from ._ranges import (
    FULL_RANGE,
    bounds_for_spec,
    coerce_version,
    filter_by_ranges,
    intersect_specifier_bounds,
    matches_bounds_only,
    ranges_are_prerelease_only,
    resolve_prereleases,
)
>>>>>>> REPLACE

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def bounds(
        self,
    ) -> tuple[
        tuple[Version, bool] | None,
        tuple[Version, bool] | None,
    ]:
        """Return the effective (lower, upper) bounds of this specifier set.

        Each bound is either ``None`` (unbounded) or a ``(Version, inclusive)``
        tuple where *inclusive* is ``True`` for ``<=``/``>=``/``==`` and
        ``False`` for ``<``/``>``/``~=`` upper / ``==.*`` upper.

        >>> SpecifierSet(">=1.0,<2.0").bounds()
        ((Version('1.0'), True), (Version('2.0'), False))
        >>> SpecifierSet(">=1.0").bounds()
        ((Version('1.0'), True), None)
        >>> SpecifierSet("<2.0").bounds()
        (None, (Version('2.0.dev0'), False))
        >>> SpecifierSet("==1.2.3").bounds()
        ((Version('1.2.3'), True), (Version('1.2.3'), True))
        >>> SpecifierSet("==1.2.*").bounds()
        ((Version('1.2.dev0'), True), (Version('1.3.dev0'), False))
        >>> SpecifierSet("~=1.4.5").bounds()
        ((Version('1.4.5'), True), (Version('1.5.dev0'), False))
        >>> SpecifierSet("").bounds()
        (None, None)

        .. versionadded:: 26.5
        """
        if not self._specs:
            return (None, None)

        if self._has_arbitrary:
            raise ValueError("bounds() does not support === specifiers")

        lower: Version | None = None
        lower_inclusive: bool = False
        upper: Version | None = None
        upper_inclusive: bool = False

        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version
            version = spec._require_spec_version()

            # Determine the lower bound contribution of this specifier
            new_lower: Version | None = None
            new_lower_inclusive: bool = False

            # Determine the upper bound contribution of this specifier
            new_upper: Version | None = None
            new_upper_inclusive: bool = False

            if ver_str.endswith(".*"):
                # Wildcard: ==V.* or !=V.*
                if op == "==":
                    # ==V.* -> [V.dev0, next_prefix.dev0)
                    new_lower = _base_dev0(version)
                    new_lower_inclusive = True
                    new_upper = _next_prefix_dev0(version)
                    new_upper_inclusive = False
                # !=V.* doesn't constrain bounds (it's the complement)
                continue

            if op == ">=":
                new_lower = version
                new_lower_inclusive = True
            elif op == ">":
                # >V: lower bound is AFTER_POSTS(V), but we report it as V
                # with inclusive=False for the bounds() API.
                new_lower = version
                new_lower_inclusive = False
            elif op == "<=":
                # <=V: upper bound is AFTER_LOCALS(V), report as V inclusive
                new_upper = version
                new_upper_inclusive = True
            elif op == "<":
                # <V: upper bound is V.dev0 (or V if prerelease)
                bound = (
                    version if version.is_prerelease else version.__replace__(dev=0, local=None)
                )
                new_upper = bound
                new_upper_inclusive = False
            elif op == "==":
                # ==V (non-wildcard): exact match
                new_lower = version
                new_lower_inclusive = True
                new_upper = version
                new_upper_inclusive = True
            elif op == "!=":
                # !=V doesn't constrain bounds
                continue
            elif op == "~=":
                # ~=V: [V, next_prefix.dev0)
                new_lower = version
                new_lower_inclusive = True
                prefix = version.__replace__(release=version.release[:-1])
                new_upper = _next_prefix_dev0(prefix)
                new_upper_inclusive = False
            # === is already checked above
            else:
                continue

            # Merge lower bound: take the larger one
            if new_lower is not None:
                if lower is None:
                    lower = new_lower
                    lower_inclusive = new_lower_inclusive
                else:
                    if new_lower > lower:
                        lower = new_lower
                        lower_inclusive = new_lower_inclusive
                    elif new_lower == lower:
                        # Same version: exclusive (False) wins
                        lower_inclusive = lower_inclusive and new_lower_inclusive

            # Merge upper bound: take the smaller one
            if new_upper is not None:
                if upper is None:
                    upper = new_upper
                    upper_inclusive = new_upper_inclusive
                else:
                    if new_upper < upper:
                        upper = new_upper
                        upper_inclusive = new_upper_inclusive
                    elif new_upper == upper:
                        # Same version: exclusive (False) wins
                        upper_inclusive = upper_inclusive and new_upper_inclusive

        return ((lower, lower_inclusive) if lower is not None else None,
                (upper, upper_inclusive) if upper is not None else None)
=======
    def bounds(
        self,
    ) -> tuple[
        tuple[Version, bool] | None,
        tuple[Version, bool] | None,
    ]:
        """Return the effective (lower, upper) bounds of this specifier set.

        Each bound is either ``None`` (unbounded) or a ``(Version, inclusive)``
        tuple where *inclusive* is ``True`` for ``<=``/``>=``/``==`` and
        ``False`` for ``<``/``>``/``~=`` upper / ``==.*`` upper.

        >>> SpecifierSet(">=1.0,<2.0").bounds()
        ((Version('1.0'), True), (Version('2.0'), False))
        >>> SpecifierSet(">=1.0").bounds()
        ((Version('1.0'), True), None)
        >>> SpecifierSet("<2.0").bounds()
        (None, (Version('2.0'), False))
        >>> SpecifierSet("==1.2.3").bounds()
        ((Version('1.2.3'), True), (Version('1.2.3'), True))
        >>> SpecifierSet("==1.2.*").bounds()
        ((Version('1.2'), True), (Version('1.3'), False))
        >>> SpecifierSet("~=1.4.5").bounds()
        ((Version('1.4.5'), True), (Version('1.5'), False))
        >>> SpecifierSet("").bounds()
        (None, None)

        .. versionadded:: 26.5
        """
        if not self._specs:
            return (None, None)

        if self._has_arbitrary:
            raise ValueError("bounds() does not support === specifiers")

        lower: Version | None = None
        lower_inclusive: bool = False
        upper: Version | None = None
        upper_inclusive: bool = False

        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version
            version = spec._require_spec_version()

            new_lower: Version | None = None
            new_lower_inclusive: bool = False
            new_upper: Version | None = None
            new_upper_inclusive: bool = False

            if ver_str.endswith(".*"):
                if op == "==":
                    new_lower = version
                    new_lower_inclusive = True
                    new_upper = Version.from_parts(
                        epoch=version.epoch,
                        release=(*version.release[:-1], version.release[-1] + 1)
                    )
                    new_upper_inclusive = False
                continue

            if op == ">=":
                new_lower = version
                new_lower_inclusive = True
            elif op == ">":
                new_lower = version
                new_lower_inclusive = False
            elif op == "<