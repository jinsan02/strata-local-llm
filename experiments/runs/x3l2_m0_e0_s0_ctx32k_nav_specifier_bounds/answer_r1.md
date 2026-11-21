EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def to_range(self) -> ranges.VersionRange:
        """Return the :class:`~packaging.ranges.VersionRange` this set accepts.

        An empty set yields the full range; an unsatisfiable set yields the
        empty range. ``===`` specifiers contribute literal-string admission.

        >>> SpecifierSet(">=1.0,<2.0").to_range()
        <VersionRange '[1.0, 2.0.dev0)'>

        .. versionadded:: 26.3
        """
        from .ranges import VersionRange  # noqa: PLC0415

        return VersionRange._from_specifier_set(self)
=======
    def to_range(self) -> ranges.VersionRange:
        """Return the :class:`~packaging.ranges.VersionRange` this set accepts.

        An empty set yields the full range; an unsatisfiable set yields the
        empty range. ``===`` specifiers contribute literal-string admission.

        >>> SpecifierSet(">=1.0,<2.0").to_range()
        <VersionRange '[1.0, 2.0.dev0)'>

        .. versionadded:: 26.3
        """
        from .ranges import VersionRange  # noqa: PLC0415

        return VersionRange._from_specifier_set(self)

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the lower and upper bounds of the specifier set.

        Returns a tuple (lower, upper), where each element is either None
        or a tuple (version, inclusive).
        """
        if any(s.operator == "===" for s in self._specs):
            raise ValueError("=== specifier is not supported for bounds()")

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version
            v = coerce_version(ver_str)
            if v is None:
                continue

            if op in (">=", ">"):
                new_lower = (v, op == ">=")
                if lower is None or v > lower[0] or (v == lower[0] and not new_lower[1]):
                    lower = new_lower
            elif op in ("<=", "<"):
                new_upper = (v, op == "<=")
                if upper is None or v < upper[0] or (v == upper[0] and not new_upper[1]):
                    upper = new_upper
            elif op == "==":
                if ver_str.endswith(".*"):
                    new_lower = (v, True)
                    if lower is None or v > lower[0] or (v == lower[0] and not new_lower[1]):
                        lower = new_lower

                    rel = v.release
                    new_rel = rel[:-1] + (rel[-1] + 1,)
                    new_ver_str = f"{v.epoch}!{'.'.join(map(str, new_rel))}"
                    new_upper_v = Version(new_ver_str)
                    new_upper = (new_upper_v, False)
                    if upper is None or new_upper_v < upper[0] or (new_upper_v == upper[0] and not new_upper[1]):
                        upper = new_upper
                else:
                    new_lower = (v, True)
                    if lower is None or v > lower[0] or (v == lower[0] and not new_lower[1]):
                        lower = new_lower
                    new_upper = (v, True)
                    if upper is None or v < upper[0] or (v == upper[0] and not new_upper[1]):
                        upper = new_upper
            elif op == "~=":
                new_lower = (v, True)
                if lower is None or v > lower[0] or (v == lower[0] and not new_lower[1]):
                    lower = new_lower

                rel = v.release
                if len(rel) > 1:
                    new_rel = rel[:-2] + (rel[-2] + 1,)
                else:
                    new_rel = (rel[-1] + 1,)
                new_ver_str = f"{v.epoch}!{'.'.join(map(str, new_rel))}"
                new_upper_v = Version(new_ver_str)
                new_upper = (new_upper_v, False)
                if upper is None or new_upper_v < upper[0] or (new_upper_v == upper[0] and not new_upper[1]):
                    upper = new_upper
            elif op == "!=":
                pass
            # === is already checked at the start

        return (lower, upper)
>>>>>>> REPLACE