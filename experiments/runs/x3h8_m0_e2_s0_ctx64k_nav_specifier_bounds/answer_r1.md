### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    )


class SpecifierSet(BaseSpecifier):
=======
    )


def _next_release(version: Version) -> Version:
    """Return the version with the last release component incremented.

    Preserves epoch; drops pre / post / dev / local.
    """
    release = (*version.release[:-1], version.release[-1] + 1)
    return Version.from_parts(epoch=version.epoch, release=release)


def _merge_lower(
    current: tuple[Version, bool] | None, version: Version, inclusive: bool
) -> tuple[Version, bool] | None:
    if current is None:
        return (version, inclusive)
    cur_ver, cur_inc = current
    if version > cur_ver:
        return (version, inclusive)
    if version == cur_ver and not inclusive:
        return (version, False)
    return current


def _merge_upper(
    current: tuple[Version, bool] | None, version: Version, inclusive: bool
) -> tuple[Version, bool] | None:
    if current is None:
        return (version, inclusive)
    cur_ver, cur_inc = current
    if version < cur_ver:
        return (version, inclusive)
    if version == cur_ver and not inclusive:
        return (version, False)
    return current


class SpecifierSet(BaseSpecifier):
>>>>>>> REPLACE

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
        self._check_relation_operand(other)
        return self.to_range().is_disjoint(other.to_range())

    def __contains__(self, item: UnparsedVersion) -> bool:
=======
        self._check_relation_operand(other)
        return self.to_range().is_disjoint(other.to_range())

    def bounds(self) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the combined lower and upper bounds of this specifier set.

        Returns a tuple ``(lower, upper)``, where each is ``None`` (unbounded)
        or a ``(Version, inclusive: bool)`` tuple.
        """
        if self._has_arbitrary:
            raise ValueError("bounds() does not support === specifiers")

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op = spec.operator
            ver = spec._require_spec_version()

            if op == ">=":
                lower = _merge_lower(lower, ver, True)
            elif op == ">":
                lower = _merge_lower(lower, ver, False)
            elif op == "<=":
                upper = _merge_upper(upper, ver, True)
            elif op == "<":
                upper = _merge_upper(upper, ver, False)
            elif op == "==":
                if spec.version.endswith(".*"):
                    lower = _merge_lower(lower, ver, True)
                    upper = _merge_upper(upper, _next_release(ver), False)
                else:
                    lower = _merge_lower(lower, ver, True)
                    upper = _merge_upper(upper, ver, True)
            elif op == "~=":
                lower = _merge_lower(lower, ver, True)
                prefix = ver.__replace__(release=ver.release[:-1])
                upper = _merge_upper(upper, _next_release(prefix), False)
            # !=V -> no bounds

        return (lower, upper)

    def __contains__(self, item: UnparsedVersion) -> bool:
>>>>>>> REPLACE