### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
class SpecifierSet(BaseSpecifier):
=======
def _specifier_bounds(
    spec: Specifier,
) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
    op, ver_str = spec._spec
    if op == "===":
        raise ValueError("=== operator is not supported in bounds()")

    v = spec._require_spec_version()
    lower: tuple[Version, bool] | None = None
    upper: tuple[Version, bool] | None = None

    if op == ">=":
        lower = (v, True)
    elif op == ">":
        lower = (v, False)
    elif op == "<=":
        upper = (v, True)
    elif op == "<":
        upper = (v, False)
    elif op == "==":
        lower = (v, True)
        if ver_str.endswith(".*"):
            new_release = list(v.release)
            new_release[-1] += 1
            upper = (Version(f"{v.epoch}{'.'.join(map(str, new_release))}"), False)
        else:
            upper = (v, True)
    elif op == "~=":
        lower = (v, True)
        new_release = list(v.release)
        if len(new_release) >= 2:
            new_release[-2] += 1
            new_release = new_release[:-1]
        else:
            new_release[0] += 1
            new_release = new_release[:1]
        upper = (Version(f"{v.epoch}{'.'.join(map(str, new_release))}"), False)

    return lower, upper


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

    def bounds(
        self,
    ) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the combined lower and upper bounds of all specifiers.

        Returns a tuple ``(lower, upper)`` where each is either ``None`` or
        ``(Version, inclusive: bool)``.

        >>> SpecifierSet(">=1.0,<=2.0").bounds()
        ((<Version('1.0')>, True), (<Version('2.0')>, True))
        >>> SpecifierSet(">1.0,<2.0").bounds()
        ((<Version('1.0')>, False), (<Version('2.0')>, False))
        >>> SpecifierSet("==1.2.*").bounds()
        ((<Version('1.2')>, True), (<Version('1.3')>, False))
        >>> SpecifierSet("~=1.4.5").bounds()
        ((<Version('1.4.5')>, True), (<Version('1.5')>, False))
        >>> SpecifierSet("").bounds()
        (None, None)
        """
        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            if spec.operator == "===":
                raise ValueError("=== operator is not supported in bounds()")

            s_lower, s_upper = _specifier_bounds(spec)

            if s_lower is not None:
                if lower is None:
                    lower = s_lower
                else:
                    if s_lower[0] > lower[0] or (s_lower[0] == lower[0] and not s_lower[1]):
                        lower = s_lower

            if s_upper is not None:
                if upper is None:
                    upper = s_upper
                else:
                    if s_upper[0] < upper[0] or (s_upper[0] == upper[0] and not s_upper[1]):
                        upper = s_upper

        return lower, upper

    def __contains__(self, item: UnparsedVersion) -> bool:
>>>>>>> REPLACE