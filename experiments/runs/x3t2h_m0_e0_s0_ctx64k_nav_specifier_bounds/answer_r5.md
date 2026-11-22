### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
        return _apply_prereleases_filter(iterable, key, prereleases)


def _pep440_filter_prereleases(
=======
        return _apply_prereleases_filter(iterable, key, prereleases)

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the effective lower and upper bounds of the specifier set.

        Returns a tuple `(lower, upper)`, where each is either ``None`` (unbounded)
        or a ``(version, inclusive)`` tuple.
        """
        if self._has_arbitrary:
            raise ValueError("Arbitrary specifier (===) is not supported in bounds()")

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op = spec.operator
            ver_str = spec.version
            ver = spec._get_spec_version()

            is_wildcard = ver_str.endswith(".*")

            if op == ">=":
                s_lower, s_upper = (ver, True), None
            elif op == ">":
                s_lower, s_upper = (ver, False), None
            elif op == "<=":
                s_lower, s_upper = None, (ver, True)
            elif op == "<":
                s_lower, s_upper = None, (ver, False)
            elif op == "==":
                if is_wildcard:
                    if len(ver.release) > 1:
                        upper_ver = Version.from_parts(
                            epoch=ver.epoch,
                            release=ver.release[:-1] + (ver.release[-1] + 1,),
                        )
                    else:
                        upper_ver = Version.from_parts(
                            epoch=ver.epoch, release=(ver.release[0] + 1,)
                        )
                    s_lower, s_upper = (ver, True), (upper_ver, False)
                else:
                    s_lower, s_upper = (ver, True), (ver, True)
            elif op == "~=":
                prefix_release = ver.release[:-1]
                if len(prefix_release) > 1:
                    upper_release = prefix_release[:-1] + (prefix_release[-1] + 1,)
                else:
                    upper_release = (prefix_release[0] + 1,)
                upper_ver = Version.from_parts(epoch=ver.epoch, release=upper_release)
                s_lower, s_upper = (ver, True), (upper_ver, False)
            elif op == "!=":
                s_lower, s_upper = None, None
            else:
                s_lower, s_upper = None, None

            if s_lower is not None:
                if lower is None:
                    lower = s_lower
                elif s_lower[0] > lower[0]:
                    lower = s_lower
                elif s_lower[0] == lower[0] and not s_lower[1]:
                    lower = s_lower

            if s_upper is not None:
                if upper is None:
                    upper = s_upper
                elif s_upper[0] < upper[0]:
                    upper = s_upper
                elif s_upper[0] == upper[0] and not s_upper[1]:
                    upper = s_upper

        return lower, upper


def _pep440_filter_prereleases(
>>>>>>> REPLACE