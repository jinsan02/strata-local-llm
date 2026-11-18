<tool_call>
<function=SEARCH>
<parameter=path>
src/packaging/markers.py
</parameter>
<parameter=old_string>
def _repair_python_full_version(
    env: dict[str, str | AbstractSet[str]],
) -> dict[str, str | AbstractSet[str]]:
    """
    Work around platform.python_version() returning something that is not PEP 440
    compliant for non-tagged Python builds.
    """
    python_full_version = cast("str", env["python_full_version"])
    env["python_full_version"] = _pep440_python_full_version(python_full_version)
    return env
</parameter>
<parameter=new_string>
def _repair_python_full_version(
    env: dict[str, str | AbstractSet[str]],
) -> dict[str, str | AbstractSet[str]]:
    """
    Work around platform.python_version() returning something that is not PEP 440
    compliant for non-tagged Python builds.
    """
    python_full_version = cast("str", env["python_full_version"])
    env["python_full_version"] = _pep440_python_full_version(python_full_version)
    return env


def _referenced_extras(markers: MarkerList) -> frozenset[str]:
    """Recursively collect all extra names referenced in a marker tree."""
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, str):
            # "and" / "or" – skip
            continue
        if isinstance(item, list):
            extras |= _referenced_extras(item)
            continue
        if not isinstance(item, tuple):
            continue
        # MarkerAtom is a tuple of (lhs, op, rhs)
        lhs, op, rhs = item
        extra_name: str | None = None

        # Check for comparisons with the 'extra' variable
        if isinstance(lhs, Variable) and lhs.value == "extra":
            if isinstance(rhs, Value):
                extra_name = rhs.value
        elif isinstance(rhs, Variable) and rhs.value == "extra":
            if isinstance(lhs, Value):
                extra_name = lhs.value
        else:
            # Check for membership in the 'extras' variable (e.g. "foo" in extras)
            if isinstance(rhs, Variable) and rhs.value == "extras":
                if isinstance(lhs, Value) and op.serialize() in {"in", "not in"}:
                    extra_name = lhs.value

        if extra_name is not None:
            extras.add(canonicalize_name(extra_name))

    return frozenset(extras)
</parameter>
</function>
</tool_call>