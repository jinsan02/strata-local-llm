EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
class SpecifierSet(BaseSpecifier):
=======
def _specifier_bounds(spec: Specifier) -> tuple[Version | None, bool, Version | None, bool]:
    op, ver_str = spec._spec
    v = spec._require_spec_version()
    
    if op == ">=":
        return (v, True, None, True)
    if op == ">":
        return (v, False, None, True)
    if op == "<=":
        return (None, True, v, True)
    if op == "<":
        return (None, True, v, False)
    if op == "==":
        if ver_str.endswith(".*"):
            rel = v.release
            new_rel = rel[:-1] + (rel[-1] + 1,)
            upper_v = Version(f"{v.epoch or 0}{'.'.join(map(str, new_rel))}")
            return (v, True, upper_v, False)
        return (v, True, v, True)
    if op == "~=":
        rel = v.release
        base_rel = rel[:-1]
        new_rel = base_rel[:-1] + (base_rel[-1] + 1,)
        upper_v = Version(f"{v.epoch or 0}{'.'.join(map(str, new_rel))}")
        return (v, True, upper_v, False)
    if op == "!=":
        return (None, True, None, True)
    if op == "===":
        raise ValueError("Cannot compute bounds for === specifier")
    return (None, True, None, True)


class SpecifierSet(BaseSpecifier):
>>>>>>> REPLACE

EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def __contains__(self, item: UnparsedVersion) -> bool:
=======
    def bounds(self) -> tuple[Version | None, bool, Version | None, bool]:
        """Return the effective bounds of the specifier set.
        
        Returns a tuple (lower, upper) where each bound is either None or
        a tuple (Version, inclusive: bool).
        """
        if self._has_arbitrary:
            raise ValueError("SpecifierSet contains === operator")
            
        lower: tuple[Version | None, bool] = (None, True)
        upper: tuple[Version | None, bool] = (None, False)
        
        for spec in self._specs:
            l_ver, l_inc, u_ver, u_inc = _specifier_bounds(spec)
            
            if l_ver is not None:
                if lower[0] is None:
                    lower = (l_ver, l_inc)
                else:
                    if l_ver > lower[0]:
                        lower = (l_ver, l_inc)
                    elif l_ver == lower[0]:
                        lower = (l_ver, l_inc and lower[1])
                        
            if u_ver is not None:
                if upper[0] is None:
                    upper = (u_ver, u_inc)
                else:
                    if u_ver < upper[0]:
                        upper = (u_ver, u_inc)
                    elif u_ver == upper[0]:
                        upper = (u_ver, u_inc and upper[1])
                        
        return lower, upper

    def __contains__(self, item: UnparsedVersion) -> bool:
>>>>>>> REPLACE