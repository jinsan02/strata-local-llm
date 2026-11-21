### EDIT: src/packaging/specifiers.py
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
        """Return the effective lower and upper bounds of this specifier set.

        Returns a tuple of ``(lower, upper)``, where each is either ``None``
        (no limit) or a ``(Version, inclusive)`` tuple.
        """
        if self._has_arbitrary:
            raise ValueError("SpecifierSet contains === operator")

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version
            v = spec._get_spec_version()
            if v is None:
                continue

            if op == ">=":
                new_lower = (v, True)
            elif op == ">":
                new_lower = (v, False)
            elif op == "<=":
                new_upper = (v, True)
            elif op == "<":
                new_upper = (v, False)
            elif op == "==":
                if ver_str.endswith(".*"):
                    new_lower = (v, True)
                    rel = list(v._release)
                    rel[-1] += 1
                    epoch_str = f"{v._epoch}!" if v._epoch else ""
                    new_upper = (Version(f"{epoch_str}{'.'.join(map(str, rel))}"), False)
                else:
                    new_lower = (v, True)
                    new_upper = (v, True)
            elif op == "~=":
                new_lower = (v, True)
                rel = list(v._release)
                if len(rel) == 1:
                    new_rel = [rel[0] + 1]
                else:
                    new_rel = rel[:-1]
                    new_rel[-1] += 1
                epoch_str = f"{v._epoch}!" if v._epoch else ""
                new_upper = (Version(f"{epoch_str}{'.'.join(map(str, new_rel))}"), False)
            else:
                new_lower = None
                new_upper = None

            if new_lower is not None:
                if lower is None or new_lower[0] > lower[0] or (
                    new_lower[0] == lower[0] and not new_lower[1]
                ):
                    lower = new_lower

            if new_upper is not None:
                if upper is None or new_upper[0] < upper[0] or (
                    new_upper[0] == upper[0] and not new_upper[1]
                ):
                    upper = new_upper

        return lower, upper
>>>>>>> REPLACE