EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def __contains__(self, item: object) -> bool:
        """Whether or not the ``item`` is contained within this specifier set."""
=======
    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Compute the lower and upper bounds implied by the specifiers.

        Returns a ``(lower, upper)`` tuple where each element is ``None``
        (unbounded) or ``tuple[Version, bool]`` (version, inclusive).
        """
        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None
        
        for spec in self._specs:
            op, ver_str = spec._spec
            
            if op == "===":
                raise ValueError("Cannot compute bounds with arbitrary specifiers (===).")
            
            if op == "!=":
                continue
                
            clean_ver_str = ver_str
            if op in ("==", "!=") and ver_str.endswith(".*"):
                clean_ver_str = ver_str[:-2]
                
            ver = Version(clean_ver_str)

            new_lower: tuple[Version, bool] | None = None
            new_upper: tuple[Version, bool] | None = None
            
            if op == ">=":
                new_lower = (ver, True)
            elif op == ">":
                new_lower = (ver, False)
            elif op == "<=":
                new_upper = (ver, True)
            elif op == "<":
                new_upper = (ver, False)
            elif op == "==":
                if ver_str.endswith(".*"):
                    new_lower = (ver, True)
                    rel = list(ver.release)
                    if not rel: rel = [0]
                    rel[-1] += 1
                    new_upper = (Version.from_parts(epoch=ver.epoch, release=tuple(rel)), False)
                else:
                    new_lower = (ver, True)
                    new_upper = (ver, True)
            elif op == "~=":
                new_lower = (ver, True)
                rel = list(ver.release)
                if len(rel) < 2:
                     raise ValueError(f"Compatible specifier ~= requires at least two release segments, got {ver}")
                upper_rel = rel[:-1]
                upper_rel[-1] += 1
                new_upper = (Version.from_parts(epoch=ver.epoch, release=tuple(upper_rel)), False)
            
            # Merge lower bound: keep the larger version. 
            # If equal versions, exclusive (inclusive=False) is stricter.
            if lower is None:
                lower = new_lower
            else:
                curr_v, curr_inc = lower
                new_v, new_inc = new_lower
                if new_v > curr_v:
                    lower = new_lower
                elif new_v == curr_v and not new_inc:
                    lower = new_lower
            
            # Merge upper bound: keep the smaller version. 
            # If equal versions, exclusive (inclusive=False) ends earlier.
            if upper is None:
                upper = new_upper
            else:
                curr_v, curr_inc = upper
                new_v, new_inc = new_upper
                if new_v < curr_v:
                    upper = new_upper
                elif new_v == curr_v and not new_inc:
                    upper = new_upper

        return (lower, upper)

    def __contains__(self, item: object) -> bool:
        """Whether or not the ``item`` is contained within this specifier set."""
>>>>>>> REPLACE