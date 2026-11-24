`SpecifierSet.bounds()` 메서드를 `src/packaging/specifiers.py`에 추가했습니다. `_next_prefix_dev0` 함수를 import 하도록 수정했습니다.

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
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
=======
from ._ranges import (
    FULL_RANGE,
    _next_prefix_dev0,
    bounds_for_spec,
    coerce_version,
    filter_by_ranges,
    intersect_specifier_bounds,
    matches_bounds_only,
    ranges_are_prerelease_only,
    resolve_prereleases,
)
>>>>>>> REPLACE
<<<<<<< SEARCH
        # Empty SpecifierSet.
        return _apply_prereleases_filter(iterable, key, prereleases)


def _pep440_filter_prereleases(
=======
        # Empty SpecifierSet.
        return _apply_prereleases_filter(iterable, key, prereleases)

    def bounds(
        self,
    ) -> tuple[
        tuple[Version, bool] | None, tuple[Version, bool] | None
    ]:
        """Return the effective lower and upper bounds of the specifier set.

        Returns a tuple ``(lower, upper)`` where each element is either
        ``None`` (unbounded) or a ``(version, inclusive)`` tuple.

        - ``lower`` is the most restrictive lower bound (highest version,
          exclusive wins on ties).
        - ``upper`` is the most restrictive upper bound (lowest version,
          exclusive wins on ties).

        Raises ``ValueError`` if the set contains any ``===`` specifiers.
        """
        if self._has_arbitrary:
            raise ValueError("bounds() does not support === specifiers")

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version
            ver = spec._get_spec_version()
            if ver is None:
                continue

            if op == ">=":
                new_lower = (ver, True)
                if lower is None or ver > lower[0] or (ver == lower[0] and not new_lower[1]):
                    lower = new_lower
            elif op == ">":
                new_lower = (ver, False)
                if lower is None or ver > lower[0] or (ver == lower[0] and not new_lower[1]):
                    lower = new_lower
            elif op == "<=":
                new_upper = (ver, True)
                if upper is None or ver < upper[0] or (ver == upper[0] and not new_upper[1]):
                    upper = new_upper
            elif op == "<":
                new_upper = (ver, False)
                if upper is None or ver < upper[0] or (ver == upper[0] and not new_upper[1]):
                    upper = new_upper
            elif op == "==":
                if ver_str.endswith(".*"):
                    new_lower = (ver, True)
                    new_upper = (_next_prefix_dev0(ver), False)
                else:
                    new_lower = (ver, True)
                    new_upper = (ver, True)
                
                if lower is None or ver > lower[0] or (ver == lower[0] and not new_lower[1]):
                    lower = new_lower
                if upper is None or ver < upper[0] or (ver == upper[0] and not new_upper[1]):
                    upper = new_upper
            elif op == "~=":
                new_lower = (ver, True)
                new_upper = (_next_prefix_dev0(ver), False)
                
                if lower is None or ver > lower[0] or (ver == lower[0] and not new_lower[1]):
                    lower = new_lower
                if upper is None or ver < upper[0] or (ver == upper[0] and not new_upper[1]):
                    upper = new_upper
            elif op == "!=":
                pass
            elif op == "===":
                raise ValueError("bounds() does not support === specifiers")

        return (lower, upper)


def _pep440_filter_prereleases(
>>>>>>> REPLACE