### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
class SpecifierSet(BaseSpecifier):
=======
def _is_greater_lower(a: tuple[Version, bool], b: tuple[Version, bool]) -> bool:
    if a[0] != b[0]:
        return a[0] > b[0]
    return not a[1] and b[1]


def _is_smaller_upper(a: tuple[Version, bool], b: tuple[Version, bool]) -> bool:
    if a[0] != b[0]:
        return a[0] < b[0]
    return not a[1] and b[1]


def _wildcard_upper(v: Version) -> tuple[Version, bool]:
    epoch = v.epoch
    release = v.release
    new_release = list(release)
    new_release[-1] += 1
    ver_str = f"{epoch}!{'.'.join(map(str, new_release))}" if epoch is not None else '.'.join(map(str, new_release))
    return Version(ver_str), False


def _compatible_upper(v: Version) -> tuple[Version, bool]:
    epoch = v.epoch
    release = v.release
    if len(release) < 2:
        new_release = list(release)
        new_release[-1] += 1
    else:
        new_release = list(release[:-1])
        new_release[-1] += 1
    ver_str = f"{epoch}!{'.'.join(map(str, new_release))}" if epoch is not None else '.'.join(map(str, new_release))
    return Version(ver_str), False


class SpecifierSet(BaseSpecifier):
>>>>>>> REPLACE
<<<<<<< SEARCH
    def to_range(self) -> ranges.VersionRange:
=======
    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the (lower, upper) bounds of this specifier set.
        
        Returns a tuple of (lower, upper) where each is either None or 
        (Version, inclusive: bool).
        """
        if self._has_arbitrary:
            raise ValueError("Specifiers with '===' are not supported for bounds()")
        
        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None
        
        for spec in self._specs:
            op, ver_str = spec._spec
            v = spec._require_spec_version()
            
            if op == ">=":
                cand = (v, True)
                if lower is None or _is_greater_lower(cand, lower):
                    lower = cand
            elif op == ">":
                cand = (v, False)
                if lower is None or _is_greater_lower(cand, lower):
                    lower = cand
            elif op == "<=":
                cand = (v, True)
                if upper is None or _is_smaller_upper(cand, upper):
                    upper = cand
            elif op == "<":
                cand = (v, False)
                if upper is None or _is_smaller_upper(cand, upper):
                    upper = cand
            elif op == "==":
                if ver_str.endswith(".*"):
                    cand_lower = (v, True)
                    if lower is None or _is_greater_lower(cand_lower, lower):
                        lower = cand_lower
                    cand_upper = _wildcard_upper(v)
                    if upper is None or _is_smaller_upper(cand_upper, upper):
                        upper = cand_upper
                else:
                    cand_lower = (v, True)
                    cand_upper = (v, True)
                    if lower is None or _is_greater_lower(cand_lower, lower):
                        lower = cand_lower
                    if upper is None or _is_smaller_upper(cand_upper, upper):
                        upper = cand_upper
            elif op == "~=":
                cand_lower = (v, True)
                if lower is None or _is_greater_lower(cand_lower, lower):
                    lower = cand_lower
                cand_upper = _compatible_upper(v)
                if upper is None or _is_smaller_upper(cand_upper, upper):
                    upper = cand_upper
            # != and === (checked) do not affect bounds
            
        return (lower, upper)

    def to_range(self) -> ranges.VersionRange:
>>>>>>> REPLACE