### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
class SpecifierSet(BaseSpecifier):
=======
def _combine_bounds(
    current: tuple[Version, bool] | None,
    new: tuple[Version, bool],
    is_lower: bool,
) -> tuple[Version, bool]:
    """Combine two bounds, keeping the tighter one."""
    if current is None:
        return new
    cur_ver, cur_inc = current
    new_ver, new_inc = new
    if cur_ver < new_ver:
        return new
    if cur_ver > new_ver:
        return current
    # cur_ver == new_ver
    # For lower bounds, inclusive=True is tighter
    # For upper bounds, inclusive=False is tighter
    if is_lower:
        return (cur_ver, cur_inc or new_inc)
    else:
        return (cur_ver, cur_inc and new_inc)


class SpecifierSet(BaseSpecifier):
>>>>>>> REPLACE

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def bounds(
        self,
    ) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the lower and upper bounds of this specifier set.

        Returns a ``(lower, upper)`` tuple where each element is ``None``
        (no limit) or a ``(Version, inclusive)`` tuple.

        The bounds are derived from the individual specifiers as follows:

        +----------+---------------------+---------------------+
        | Operator | Lower bound         | Upper bound         |
        +==========+=====================+=====================+
        | ``>=V``  | ``(V, True)``       | —                   |
        +----------+---------------------+---------------------+
        | ``>V``   | ``(V, False)``      | —                   |
        +----------+---------------------+---------------------+
        | ``<=V``  | —                   | ``(V, True)``       |
        +----------+---------------------+---------------------+
        | ``<V``   | —                   | ``(V, False)``      |
        +----------+---------------------+---------------------+
        | ``==V``  | ``(V, True)``       | ``(V, True)``       |
        | (not     |                     |                     |
        |  wildcard)                     |                     |
        +----------+---------------------+---------------------+
        | ``==V.*``| ``(V, True)``       | ``(next, False)``   |
        +----------+---------------------+---------------------+
        | ``~=V``  | ``(V, True)``       | ``(next, False)``   |
        +----------+---------------------+---------------------+
        | ``!=V``  | —                   | —                   |
        +----------+---------------------+---------------------+

        For wildcards and ``~=`` the upper bound is computed by incrementing
        the last release digit (epoch is preserved; no pre/post/dev/local).

        Multiple specifiers are merged: the lower bound is the largest lower,
        the upper bound is the smallest upper.  When versions are equal
        (e.g. ``2`` vs ``2.0``), ``inclusive=False`` wins (tighter bound).

        An empty ``SpecifierSet`` returns ``(None, None)``.

        :raises ValueError:
            If any specifier uses ``===`` (arbitrary equality).

        .. versionadded:: 26.5
        """
        if self._has_arbitrary:
            raise ValueError("bounds() does not support === specifiers")

        if not self._specs:
            return (None, None)

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op = spec.operator
            ver = spec._require_spec_version()
            ver_str = spec.version

            if op == ">=":
                lower = _combine_bounds(lower, (ver, True), is_lower=True)
            elif op == ">":
                lower = _combine_bounds(lower, (ver, False), is_lower=True)
            elif op == "<=":
                upper = _combine_bounds(upper, (ver, True), is_lower=False)
            elif op == "<":
                upper = _combine_bounds(upper, (ver, False), is_lower=False)
            elif op == "==":
                if ver_str.endswith(".*"):
                    lower = _combine_bounds(lower, (ver, True), is_lower=True)
                    release = (*ver.release[:-1], ver.release[-1] + 1)
                    upper_ver = Version.from_parts(
                        epoch=ver.epoch, release=release
                    )
                    upper = _combine_bounds(upper, (upper_ver, False), is_lower=False)
                else:
                    lower = _combine_bounds(lower, (ver, True), is_lower=True)
                    upper = _combine_bounds(upper, (ver, True), is_lower=False)
            elif op == "~=":
                lower = _combine_bounds(lower, (ver, True), is_lower=True)
                release = (*ver.release[:-1], ver.release[-1] + 1)
                upper_ver = Version.from_parts(
                    epoch=ver.epoch, release=release
                )
                upper = _combine_bounds(upper, (upper_ver, False), is_lower=False)
            # "!=" contributes no bounds; "===" is rejected above

        return (lower, upper)
=======
    def bounds(
        self,
    ) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the lower and upper bounds of this specifier set.

        Returns a ``(lower, upper)`` tuple where each element is ``None``
        (no limit) or a ``(Version, inclusive)`` tuple.

        The bounds are derived from the individual specifiers as follows:

        +----------+---------------------+---------------------+
        | Operator | Lower bound         | Upper bound         |
        +==========+=====================+=====================+
        | ``>=V``  | ``(V, True)``       | —                   |
        +----------+---------------------+---------------------+
        | ``>V``   | ``(V, False)``      | —                   |
        +----------+---------------------+---------------------+
        | ``<=V``  | —                   | ``(V, True)``       |
        +----------+---------------------+---------------------+
        | ``<V``   | —                   | ``(V, False)``      |
        +----------+---------------------+---------------------+
        | ``==V``  | ``(V, True)``       | ``(V, True)``       |
        | (not     |                     |                     |
        |  wildcard)                     |                     |
        +----------+---------------------+---------------------+
        | ``==V.*``| ``(V, True)``       | ``(next, False)``   |
        +----------+---------------------+---------------------+
        | ``~=V``  | ``(V, True)``       | ``(next, False)``   |
        +----------+---------------------+---------------------+
        | ``!=V``  | —                   | —                   |
        +----------+---------------------+---------------------+

        For ``==V.*`` the upper bound increments the last release digit.
        For ``~=V`` the upper bound drops the last release digit and
        increments the new last digit. Epoch is preserved; no pre/post/dev/local.

        Multiple specifiers are merged: the lower bound is the largest lower,
        the upper bound is the smallest upper.  When versions are equal
        (e.g. ``2`` vs ``2.0``), ``inclusive=False`` wins (tighter bound).

        An empty ``SpecifierSet`` returns ``(None, None)``.

        :raises ValueError:
            If any specifier uses ``===`` (arbitrary equality).

        .. versionadded:: 26.5
        """
        if self._has_arbitrary:
            raise ValueError("bounds() does not support === specifiers")

        if not self._specs:
            return (None, None)

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op = spec.operator
            ver = spec._require_spec_version()
            ver_str = spec.version

            if op == ">=":
                lower = _combine_bounds(lower, (ver, True), is_lower=True)
            elif op == ">":
                lower = _combine_bounds(lower, (ver, False), is_lower=True)
            elif op == "<=":
                upper = _combine_bounds(upper, (ver, True), is_lower=False)
            elif op == "<":
                upper = _combine_bounds(upper, (ver, False), is_lower=False)
            elif op == "==":
                if ver_str.endswith(".*"):
                    lower = _combine_bounds(lower, (ver, True), is_lower=True)