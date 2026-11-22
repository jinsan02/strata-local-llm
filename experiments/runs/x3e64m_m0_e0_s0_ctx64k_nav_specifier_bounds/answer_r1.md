EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
from .version import Version, _adapt_possessive
=======
from .version import InvalidVersion, Version, _adapt_possessive
>>>>>>> REPLACE

EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
        return bool(list(self.filter([check_item], prereleases=prereleases)))

    @typing.overload
    def filter(
=======
        return bool(list(self.filter([check_item], prereleases=prereleases)))

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the lower and upper bounds of the specifier set.
        
        Returns a tuple (lower, upper) where each is None or a (Version, inclusive) tuple.
        Raises ValueError if the set contains '===' specifiers.
        """
        if self._has_arbitrary:
            raise ValueError("Bounds cannot be determined for specifiers containing '==='")
        
        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None
        
        for spec in self._specs:
            op, ver_str = spec._spec
            clean_ver_str = ver_str.removesuffix(".*")
            try:
                v = Version(clean_ver_str)
            except InvalidVersion:
                continue
                
            spec_lower: tuple[Version, bool] | None = None
            spec_upper: tuple[Version, bool] | None = None
            
            if op == ">=":
                spec_lower = (v, True)
            elif op == ">":
                spec_lower = (v, False)
            elif op == "<=":
                spec_upper = (v, True)
            elif op == "<":
                spec_upper = (v, False)
            elif op == "==":
                if ver_str.endswith(".*"):
                    spec_lower = (v, True)
                    new_rel = list(v.release)
                    new_rel[-1] += 1
                    epoch_str = f"{v.epoch}!" if v.epoch else ""
                    spec_upper = (Version(f"{epoch_str}{'.'.join(map(str, new_rel))}"), False)
                else:
                    spec_lower = (v, True)
                    spec_upper = (v, True)
            elif op == "~=":
                spec_lower = (v, True)
                rel = v.release
                if len(rel) >= 2:
                    new_rel = rel[:-1] + (rel[-2] + 1,)
                    epoch_str = f"{v.epoch}!" if v.epoch else ""
                    spec_upper = (Version(f"{epoch_str}{'.'.join(map(str, new_rel))}"), False)
            elif op == "!=":
                pass
                
            if spec_lower is not None:
                if lower is None:
                    lower = spec_lower
                elif v > lower[0]:
                    lower = spec_lower
                elif v == lower[0] and not spec_lower[1]:
                    lower = spec_lower
                    
            if spec_upper is not None:
                v_u = spec_upper[0]
                if upper is None:
                    upper = spec_upper
                elif v_u < upper[0]:
                    upper = spec_upper
                elif v_u == upper[0] and not spec_upper[1]:
                    upper = spec_upper
                    
        return (lower, upper)

    @typing.overload
    def filter(
>>>>>>> REPLACE