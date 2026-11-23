### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
class SpecifierSet(BaseSpecifier):
=======
def _increment_last_release(release: tuple[int, ...]) -> tuple[int, ...]:
    """Increment the last element of a release tuple."""
    return (*release[:-1], release[-1] + 1)


def _combine_bounds(
    current: tuple[Version, bool] | None,
    new: tuple[Version, bool],
    is_lower: bool,
) -> tuple[Version, bool] | None:
    """Combine two bounds of the same side (lower or upper)."""
    if current is None:
        return new

    cur_ver, cur_inc = current
    new_ver, new_inc = new

    if cur_ver != new_ver:
        if is_lower:
            return new if cur_ver < new_ver else current
        else:
            return new if cur_ver > new_ver else current

    # Same version — inclusive=False always wins.
    if cur_inc and not new_inc:
        return new
    if new_inc and not cur_inc:
        return current
    return current


class SpecifierSet(BaseSpecifier):
>>>>>>> REPLACE

### EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
        # Empty SpecifierSet.
        return _apply_prereleases_filter(iterable, key, prereleases)
=======
        # Empty SpecifierSet.
        return _apply_prereleases_filter(iterable, key, prereleases)

    def bounds(
        self,
    ) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
        """Return the (lower, upper) bounds of this SpecifierSet."""
        if self._has_arbitrary:
            raise ValueError("bounds() does not support === specifiers")

        lower: tuple[Version, bool] | None = None
        upper: tuple[Version, bool] | None = None

        for spec in self._specs:
            op = spec.operator
            ver = spec._require_spec_version()
            ver_str = spec.version

            if op == ">=":
                lower = _combine_bounds(lower, (ver, True), is_lower=True)
            elif op == ">":
                lower = _combine_bounds(lower, (ver, False), is_lower=True)
            elif op == "<=":
                upper = _combine_bounds(upper, (ver, True), is_lower=False)
            elif op == "<":
                upper = _combine_bounds(upper, (ver, False), is_lower=False)
            elif op == "==":
                if ver_str.endswith(".*"):
                    lower = _combine_bounds(lower, (ver, True), is_lower=True)
                    new_release = _increment_last_release(ver.release)
                    upper = _combine_bounds(
                        upper,
                        (Version.from_parts(epoch=ver.epoch, release=new_release), False),
                        is_lower=False,
                    )
                else:
                    lower = _combine_bounds(lower, (ver, True), is_lower=True)
                    upper = _combine_bounds(upper, (ver, True), is_lower=False)
            elif op == "~=":
                lower = _combine_bounds(lower, (ver, True), is_lower=True)
                prefix_release = ver.release[:-1]
                new_release = (*prefix_release[:-1], prefix_release[-1] + 1)
                upper = _combine_bounds(
                    upper,
                    (Version.from_parts(epoch=ver.epoch, release=new_release), False),
                    is_lower=False,
                )
            elif op == "!=":
                pass
            else:
                raise ValueError(f"Unknown operator: {op!r}")

        return (lower, upper)
>>>>>>> REPLACE

`SpecifierSet`에 `bounds()` 메서드를 추가하고, 경계 결합 및 버전 인크리먼트를 위한 두 개의 내부 헬퍼 함수(`_combine_bounds`, `_increment_last_release`)를 `class SpecifierSet` 앞에 정의했습니다. `===` 사용 시 `ValueError`를 던지며, 프리리리즈 설정은 무시합니다.