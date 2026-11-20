EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def __eq__(self, other: object) -> bool:
        """Whether or not the two SpecifierSet-like objects are equal.
=======
    def bounds(self) -> tuple[None | tuple[Version, bool], None | tuple[Version, bool]]:
        """Return the overall lower and upper bounds of the specifier set.
        
        Returns a tuple `(lower, upper)` where each is `None` or `(Version, inclusive)`.
        Raises `ValueError` if any specifier uses `===`.
        """
        if self._has_arbitrary:
            raise ValueError("bounds() does not support === specifiers")
            
        lower: None | tuple[Version, bool] = None
        upper: None | tuple[Version, bool] = None
        
        for spec in self._specs:
            op = spec.operator
            ver = spec._spec_version
            if ver is None:
                continue
                
            spec_lower: None | tuple[Version, bool] = None
            spec_upper: None | tuple[Version, bool] = None
            
            if op == ">=":
                spec_lower = (ver, True)
            elif op == ">":
                spec_lower = (ver, False)
            elif op == "<=":
                spec_upper = (ver, True)
            elif op == "<":
                spec_upper = (ver, False)
            elif op == "==":
                if spec.version.endswith(".*"):
                    spec_lower = (ver, True)
                    rel = ver.release
                    new_rel = rel[:-1] + (rel[-1] + 1,)
                    spec_upper = (Version(epoch=ver.epoch, release=new_rel), False)
                else:
                    spec_lower = (ver, True)
                    spec_upper = (ver, True)
            elif op == "~=":
                spec_lower = (ver, True)
                rel = ver.release
                if len(rel) == 1:
                    new_rel = (rel[0] + 1,)
                else:
                    new_rel = rel[:-1]
                    new_rel = new_rel[:-1] + (new_rel[-1] + 1,)
                spec_upper = (Version(epoch=ver.epoch, release=new_rel), False)
            elif op == "!=":
                pass
            else:
                raise ValueError("bounds() does not support === specifiers")
                
            if spec_lower is not None:
                if lower is None:
                    lower = spec_lower
                else:
                    v1, inc1 = lower
                    v2, inc2 = spec_lower
                    if v2 > v1:
                        lower = spec_lower
                    elif v1 == v2:
                        lower = (v1, inc1 and inc2)
                        
            if spec_upper is not None:
                if upper is None:
                    upper = spec_upper
                else:
                    v1, inc1 = upper
                    v2, inc2 = spec_upper
                    if v2 < v1:
                        upper = spec_upper
                    elif v1 == v2:
                        upper = (v1, inc1 and inc2)
                        
        return (lower, upper)

    def __eq__(self, other: object) -> bool:
        """Whether or not the two SpecifierSet-like objects are equal.
>>>>>>> REPLACE