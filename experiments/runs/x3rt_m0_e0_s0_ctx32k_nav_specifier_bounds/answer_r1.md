`packaging.specifiers.SpecifierSet` 클래스에 `bounds()` 메서드를 추가하고, 내부적으로 각 specifier 의 경계를 계산하여 합치는 로직을 구현했습니다.

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
    def __contains__(self, item: UnparsedVersion) -> bool:
=======
    def bounds(
        self,
    ) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the overall lower and upper bounds implied by the specifiers.

        Returns a tuple ``(lower, upper)`` where each is either ``None`` or a
        ``(Version, inclusive)`` tuple.  ``lower`` is the greatest lower bound,
        ``upper`` is the smallest upper bound.  If versions are equal, the
        exclusive bound wins.  Empty sets return ``(None, None)``.  Raises
        ``ValueError`` if any ``===`` specifier is present.

        .. versionadded:: 26.5
        """
        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            if spec.operator == "===":
                raise ValueError("=== specifiers are not supported by bounds()")

            s_lower, s_upper = _specifier_bounds(spec)

            if s_lower is not None:
                lower = _compare_lower(lower, s_lower)
            if s_upper is not None:
                upper = _compare_upper(upper, s_upper)

        return (lower, upper)

    def __contains__(self, item: UnparsedVersion) -> bool:
>>>>>>> REPLACE
<<<<<<< SEARCH
  def __iter__(self) -> Iterator[Specifier]:
=======
  def __iter__(self) -> Iterator[Specifier]:
>>>>>>> REPLACE
<<<<<<< SEARCH
        return iter(self._specs)

    def _get_ranges(self) -> Sequence[Interval]:
=======
        return iter(self._specs)


def _compare_lower(
    b1: tuple[Version, bool] | None, b2: tuple[Version, bool] | None
) -> tuple[Version, bool]:
    """Return the greater of two lower bounds."""
    if b1 is None:
        return b2  # type: ignore[return-value]
    if b2 is None:
        return b1
    v1, inc1 = b1
    v2, inc2 = b2
    if v1 > v2:
        return b1
    if v2 > v1:
        return b2
    # Same version: exclusive (False) starts later, so it is greater
    if not inc1:
        return b1
    return b2


def _compare_upper(
    b1: tuple[Version, bool] | None, b2: tuple[Version, bool] | None
) -> tuple[Version, bool]:
    """Return the smaller of two upper bounds."""
    if b1 is None:
        return b2  # type: ignore[return-value]
    if b2 is None:
        return b1
    v1, inc1 = b1
    v2, inc2 = b2
    if v1 < v2:
        return b1
    if v2 < v1:
        return b2
    # Same version: exclusive (False) ends earlier, so it is smaller
    if not inc1:
        return b1
    return b2


def _specifier_bounds(
    spec: Specifier,
) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
    """Compute (lower, upper) bounds for a single specifier."""
    op = spec.operator
    ver_str = spec.version
    ver = spec._require_spec_version()

    if op == ">=":
        return ((ver, True), None)
    if op == ">":
        return ((ver, False), None)
    if op == "<=":
        return (None, (ver, True))
    if op == "<":
        return (None, (ver, False))
    if op == "==":
        if ver_str.endswith(".*"):
            epoch = ver.epoch
            release = ver.release
            if not release:
                upper_ver = Version("0.1" if not epoch else f"{epoch}!0.1")
            else:
                new_release = list(release)
                new_release[-1] += 1
                if epoch:
                    upper_ver = Version(f"{epoch}!{'.'.join(map(str, new_release))}")
                else:
                    upper_ver = Version(".".join(map(str, new_release)))
            return ((ver, True), (upper_ver, False))
        else:
            return ((ver, True), (ver, True))
    if op == "~=":
        epoch = ver.epoch
        release = ver.release
        if len(release) < 2:
            new_release = list(release)
            new_release[-1] += 1
        else:
            new_release = list(release[:-2])
            new_release.append(release[-2] + 1)

        if epoch:
            upper_ver = Version(f"{epoch}!{'.'.join(map(str, new_release))}")
        else:
            upper_ver = Version(".".join(map(str, new_release)))
        return ((ver, True), (upper_ver, False))
    if op == "!=":
        return (None, None)

    return (None, None)

    def _get_ranges(self) -> Sequence[Interval]:
>>>>>>> REPLACE