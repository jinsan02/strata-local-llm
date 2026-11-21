EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def __contains__(self, item: UnparsedVersion) -> bool:
=======
    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the effective lower and upper bounds of the specifier set.
        
        Returns a tuple ``(lower, upper)`` where each is either ``None`` (unbounded)
        or a ``(version, inclusive)`` tuple.
        """
        from ._ranges import LowerBound, UpperBound  # noqa: PLC0415
        
        if self._has_arbitrary:
            raise ValueError("Bounds are not defined for sets with === specifiers")
            
        if not self._specs:
            return (None, None)
            
        min_lower: LowerBound | None = None
        max_upper: UpperBound | None = None
        
        for spec in self._specs:
            op = spec.operator
            ver = spec._require_spec_version()
            
            if op in (">=", ">"):
                lb = LowerBound(ver, op == ">=")
                if min_lower is None or lb > min_lower:
                    min_lower = lb
            elif op in ("<=", "<"):
                ub = UpperBound(ver, op == "<=")
                if max_upper is None or ub < max_upper:
                    max_upper = ub
            elif op == "==":
                if spec.version.endswith(".*"):
                    lb = LowerBound(ver, True)
                    if min_lower is None or lb > min_lower:
                        min_lower = lb
                    upper_ver = Version.from_parts(
                        epoch=ver.epoch, 
                        release=(*ver.release[:-1], ver.release[-1] + 1)
                    )
                    ub = UpperBound(upper_ver, False)
                    if max_upper is None or ub < max_upper:
                        max_upper = ub
                else:
                    lb = LowerBound(ver, True)
                    if min_lower is None or lb > min_lower:
                        min_lower = lb
                    ub = UpperBound(ver, True)
                    if max_upper is None or ub < max_upper:
                        max_upper = ub
            elif op == "~=":
                lb = LowerBound(ver, True)
                if min_lower is None or lb > min_lower:
                    min_lower = lb
                upper_ver = Version.from_parts(
                    epoch=ver.epoch, 
                    release=(*ver.release[:-2], ver.release[-2] + 1)
                )
                ub = UpperBound(upper_ver, False)
                if max_upper is None or ub < max_upper:
                    max_upper = ub
            # != contributes no bounds
            
        lower = (min_lower.version, min_lower.inclusive) if min_lower is not None else None
        upper = (max_upper.version, max_upper.inclusive) if max_upper is not None else None
        return lower, upper

    def __contains__(self, item: UnparsedVersion) -> bool:
>>>>>>> REPLACE