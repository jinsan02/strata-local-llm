EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
class SpecifierSet(BaseSpecifier):
=======
def _max_lower(
    a: tuple[Version, bool] | None, b: tuple[Version, bool] | None
) -> tuple[Version, bool] | None:
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0]:
        return a if not a[1] else b
    return a if a[0] > b[0] else b


def _min_upper(
    a: tuple[Version, bool] | None, b: tuple[Version, bool] | None
) -> tuple[Version, bool] | None:
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0]:
        return a if not a[1] else b
    return a if a[0] < b[0] else b


def _make_upper_version(version: Version) -> Version:
    if len(version.release) == 1:
        release = (version.release[0] + 1,)
    else:
        release = version.release[:-1] + (version.release[-1] + 1,)
    return version.__replace__(release=release, pre=None, post=None, dev=None, local=None)


class SpecifierSet(BaseSpecifier):
>>>>>>> REPLACE