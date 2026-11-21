### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def _check_relation_operand(self, other: object) -> None:
        if not isinstance(other, SpecifierSet):
            raise TypeError("expected a SpecifierSet")
        if self._has_arbitrary or other._has_arbitrary:
            raise ValueError("set relations do not support === specifiers")
=======
    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the effective lower and upper bounds of the specifier set.
        
        Returns a tuple (lower, upper) where each is None or a (Version, inclusive) tuple.
        Raises ValueError if the set contains === specifiers.
        """
        if self._has_arbitrary:
            raise ValueError("SpecifierSet with === operator does not support bounds()")
            
        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None
        
        for spec in self._specs:
            op, ver_str = spec._spec
            ver = spec._require_spec_version()
            
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
                    new_release = ver.release[:-1] + (ver.release[-1] + 1,)
                    upper_ver_str = f"{ver.epoch}!{'.'.join(map(str, new_release))}" if ver.epoch else '.'.join(map(str, new_release))
                    new_upper = (Version(upper_ver_str), False)
                    
                    if lower is None or ver > lower[0] or (ver == lower[0] and not new_lower[1]):
                        lower = new_lower
                    if upper is None or new_upper[0] < upper[0] or (new_upper[0] == upper[0] and not new_upper[1]):
                        upper = new_upper
                else:
                    new_lower = (ver, True)
                    new_upper = (ver, True)
                    if lower is None or ver > lower[0] or (ver == lower[0] and not new_lower[1]):
                        lower = new_lower
                    if upper is None or ver < upper[0] or (ver == upper[0] and not new_upper[1]):
                        upper = new_upper
            elif op == "~=":
                new_lower = (ver, True)
                new_release = ver.release[:-1] + (ver.release[-1] + 1,)
                upper_ver_str = f"{ver.epoch}!{'.'.join(map(str, new_release))}" if ver.epoch else '.'.join(map(str, new_release))
                new_upper = (Version(upper_ver_str), False)
                
                if lower is None or ver > lower[0] or (ver == lower[0] and not new_lower[1]):
                    lower = new_lower
                if upper is None or new_upper[0] < upper[0] or (new_upper[0] == upper[0] and not new_upper[1]):
                    upper = new_upper
            # != and === are handled separately or ignored for bounds
            
        return lower, upper

    def _check_relation_operand(self, other: object) -> None:
        if not isinstance(other, SpecifierSet):
            raise TypeError("expected a SpecifierSet")
        if self._has_arbitrary or other._has_arbitrary:
            raise ValueError("set relations do not support === specifiers")
>>>>>>> REPLACE