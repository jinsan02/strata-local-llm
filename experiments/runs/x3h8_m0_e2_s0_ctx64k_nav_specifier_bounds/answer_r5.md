<tool_call>
<function=edit_file>
<parameter=path>
src/packaging/specifiers.py
</parameter>
<parameter=operation>
add
</parameter>
<parameter=position>
before_line
</parameter>
<parameter=line_number>
842
</parameter>
<parameter=new_code>

def _specifier_bounds(
    spec: Specifier,
) -> tuple[tuple[Version, bool] | None, tuple[Version, bool] | None]:
    """Compute the (lower, upper) bounds for a single specifier.

    Returns (lower, upper) where each is None (unbounded) or
    a tuple (Version, inclusive).
    """
    op = spec.operator
    ver = spec._get_spec_version()
    if ver is None:
        return (None, None)

    if op == ">=":
        return ((ver, True), None)
    elif op == ">":
        return ((ver, False), None)
    elif op == "<=":
        return (None, (ver, True))
    elif op == "<":
        return (None, (ver, False))
    elif op == "==":
        if spec.version.endswith(".*"):
            release = ver.release
            new_release = (*release[:-1], release[-1] + 1)
            upper = Version.from_parts(epoch=ver.epoch, release=new_release)
            return ((ver, True), (upper, False))
        else:
            return ((ver, True), (ver, True))
    elif op == "!=":
        return (None, None)
    elif op == "~=":
        release = ver.release
        if len(release) == 1:
            new_release = (release[0] + 1,)
        else:
            new_release = (*release[:-1], release[-1] + 1)
        upper = Version.from_parts(epoch=ver.epoch, release=new_release)
        return ((ver, True), (upper, False))
    elif op == "===":
        return (None, None)
    else:
        raise ValueError(f"Unknown operator: {op!r}")
</parameter>
</function>
</tool_call>