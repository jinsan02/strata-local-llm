### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
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
def _combine_lower(
    existing: tuple[Version, bool], new: tuple[Version, bool]
) -> tuple[Version, bool]:
    """Return the greater of two lower bounds.

    If versions are equal, the exclusive (inclusive=False) bound wins
    because it is stricter.
    """
    ev, ei = existing
    nv, ni = new
    if nv > ev:
        return new
    if nv < ev:
        return existing
    # Same version: exclusive wins (stricter)
    return (nv, ni) if not ni else existing


def _combine_upper(
    existing: tuple[Version, bool], new: tuple[Version, bool]
) -> tuple[Version, bool]:
    """Return the lesser of two upper bounds.

    If versions are equal, the exclusive (inclusive=False) bound wins
    because it is stricter.
    """
    ev, ei = existing
    nv, ni = new
    if nv < ev:
        return new
    if nv > ev:
        return existing
    # Same version: exclusive wins (stricter)
    return (nv, ni) if not ni else existing


def _pep440_filter_prereleases(
=======
def _pep440_filter_prereleases(
>>>>>>> REPLACE