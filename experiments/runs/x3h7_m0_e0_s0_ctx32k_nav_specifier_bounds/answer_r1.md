EDIT: src/packaging/specifiers.py
<<<<<<< SEARCH
class SpecifierSet(BaseSpecifier):
=======
def _specifier_bounds(
    spec: Specifier,
) -> tuple[Version | None, bool | None, Version | None, bool | None]:
    op, ver_str = spec._spec
    v = spec._require_spec_version()
    
    if op == ">=":
        return (v, True, None, None)
    if op == ">":
        return (v, False, None, None)
    if op == "<=":
        return (None, None, v, True)
    if op == "<":
        return (None, None, v, False)
    if op == "==":
        if ver_str.endswith(".*"):
            release = list(v._release)
            release[-1] += 1
            next_v = Version(f"{v.epoch}{'.'.join(str(x) for x in release)}")
            return (v, True, next_v, False)
        return (v, True, v, True)
    if op == "~=":
        release = list(v._release)
        if len(release) > 1:
            release = release[:-1]
        release[-1] += 1
        next_v = Version(f"{v.epoch}{'.'.join(str(x) for x in release)}")
        return (v, True, next_v, False)
    return (None, None, None, None)


class SpecifierSet(BaseSpecifier):
>>>>>>> REPLACE