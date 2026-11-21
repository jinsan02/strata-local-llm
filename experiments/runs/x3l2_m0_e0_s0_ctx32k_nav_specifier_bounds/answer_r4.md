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
    BoundaryVersion,
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
        return matches_bounds_only(self._specs, version)

    def __len__(self) -> int:
=======
        return matches_bounds_only(self._specs, version)

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Returns the bounds of the specifier set.
        
        Returns a tuple (lower, upper) where each is None (unbounded) or
        a tuple (Version, inclusive: bool).
        """
        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            if spec.operator == "===":
                raise ValueError("Cannot use '===' in SpecifierSet bounds()")

            intervals = bounds_for_spec(spec.operator, spec.version, spec._version)
            
            for lb, ub in intervals:
                # Process lower bound
                new_lower = None
                if lb.version is not None:
                    v = lb.version
                    if isinstance(v, BoundaryVersion):
                        v = v.version
                    new_lower = (v, lb.inclusive)
                
                # Process upper bound
                new_upper = None
                if ub.version is not None:
                    v = ub.version
                    if isinstance(v, BoundaryVersion):
                        v = v.version
                    new_upper = (v, ub.inclusive)
                
                # Combine lower
                if new_lower is not None:
                    if lower is None:
                        lower = new_lower
                    else:
                        v1, inc1 = lower
                        v2, inc2 = new_lower
                        if v1 == v2:
                            # equal versions: inclusive=False wins
                            if not inc2:
                                lower = new_lower
                        else:
                            # greater version wins
                            if v2 > v1:
                                lower = new_lower
                
                # Combine upper
                if new_upper is not None:
                    if upper is None:
                        upper = new_upper
                    else:
                        v1, inc1 = upper
                        v2, inc2 = new_upper
                        if v1 == v2:
                            # equal versions: inclusive=False wins
                            if not inc2:
                                upper = new_upper
                        else:
                            # smaller version wins
                            if v2 < v1:
                                upper = new_upper

        return lower, upper

    def __len__(self) -> int:
>>>>>>> REPLACE