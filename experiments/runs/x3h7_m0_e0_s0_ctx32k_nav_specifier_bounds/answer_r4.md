EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
          # Empty SpecifierSet.
          return _apply_prereleases_filter(iterable, key, prereleases)
=======
          # Empty SpecifierSet.
          return _apply_prereleases_filter(iterable, key, prereleases)

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the lower and upper bounds of this specifier set.

        Returns a tuple ``(lower, upper)``, where each bound is either ``None``
        (no limit) or a ``(version, inclusive)`` tuple.

        Raises :exc:`ValueError` if any specifier uses the identity operator
        (``===``).
        """
        if self._has_arbitrary:
            raise ValueError("bounds() does not support === specifiers")

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op, ver_str = spec._spec

            try:
                if ver_str.endswith(".*"):
                    v = Version(ver_str.removesuffix(".*"))
                else:
                    v = Version(ver_str)
            except Exception:
                continue

            if op == ">=":
                lower = self._update_lower(lower, (v, True))
            elif op == ">":
                lower = self._update_lower(lower, (v, False))
            elif op == "<=":
                upper = self._update_upper(upper, (v, True))
            elif op == "<":
                upper = self._update_upper(upper, (v, False))
            elif op == "==":
                if ver_str.endswith(".*"):
                    lower = self._update_lower(lower, (v, True))
                    upper_v = self._compute_wildcard_upper(v)
                    upper = self._update_upper(upper, (upper_v, False))
                else:
                    lower = self._update_lower(lower, (v, True))
                    upper = self._update_upper(upper, (v, True))
            elif op == "~=":
                lower = self._update_lower(lower, (v, True))
                upper_v = self._compute_compatible_upper(v)
                upper = self._update_upper(upper, (upper_v, False))
            elif op == "!=":
                pass
            elif op == "===":
                raise ValueError("bounds() does not support === specifiers")

        return (lower, upper)

    def _update_lower(
        self, current: tuple[Version, bool] | None, new: tuple[Version, bool]
    ) -> tuple[Version, bool] | None:
        if current is None:
            return new
        cv, ci = current
        nv, ni = new
        if nv > cv:
            return new
        if nv < cv:
            return current
        # Equal versions: exclusive (False) is a stricter (higher) lower bound
        if not ni:
            return new
        return current

    def _update_upper(
        self, current: tuple[Version, bool] | None, new: tuple[Version, bool]
    ) -> tuple[Version, bool] | None:
        if current is None:
            return new
        cv, ci = current
        nv, ni = new
        if nv < cv:
            return new
        if nv > cv:
            return current
        # Equal versions: exclusive (False) is a stricter (lower) upper bound
        if not ni:
            return new
        return current

    def _compute_wildcard_upper(self, v: Version) -> Version:
        release = v.release
        if not release:
            return Version(f"{v.epoch}!1")

        new_release = list(release[:-1])
        if new_release:
            new_release[-1] += 1
        else:
            new_release = [1]

        epoch = v.epoch
        rel_str = ".".join(map(str, new_release))
        ver_str = f"{epoch}!{rel_str}" if epoch else rel_str
        return Version(ver_str)

    def _compute_compatible_upper(self, v: Version) -> Version:
        release = v.release
        if len(release) < 2:
            # ~=1 is invalid per PEP 440, but fallback to <2 if encountered
            return Version(f"{v.epoch}!1")

        new_release = list(release[:-1])
        new_release[-1] += 1

        epoch = v.epoch
        rel_str = ".".join(map(str, new_release))
        ver_str = f"{epoch}!{rel_str}" if epoch else rel_str
        return Version(ver_str)
>>>>>>> REPLACE