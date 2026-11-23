<tool_call>
<function=edit_file>
<parameter=new_string>
_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


def _extract_extras_from_markers(
    markers_list: markers.markers.MarkerList,
) -> set[utils.NormalizedName]:
    """Extract extra names from marker comparisons.

    Returns canonicalized extra names found in comparisons like
    ``extra == "docs"`` or ``"docs" == extra``.
    """
    extras: set[utils.NormalizedName] = set()
    for item in markers_list:
        if isinstance(item, str):
            # "and" or "or" operator - skip
            continue
        if isinstance(item, tuple):
            # MarkerItem: (lhs, op, rhs)
            lhs, op, rhs = item
            if isinstance(lhs, markers.markers.Variable) and lhs.value == "extra":
                if isinstance(rhs, markers.markers.Value):
                    extras.add(utils.canonicalize_name(rhs.value))
            elif isinstance(rhs, markers.markers.Variable) and rhs.value == "extra":
                if isinstance(lhs, markers.markers.Value):
                    extras.add(utils.canonicalize_name(lhs.value))
        else:
            # Nested MarkerList (inside parentheses)
            extras.update(_extract_extras_from_markers(item))
    return extras


# Keep the two values in sync.
</parameter>
<parameter=old_string>
_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


# Keep the two values in sync.
</parameter>
<parameter=path>
src/packaging/metadata.py
</parameter>
</function>
</tool_call>