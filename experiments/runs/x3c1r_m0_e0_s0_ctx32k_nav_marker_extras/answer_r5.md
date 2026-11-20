### EDIT: src/packaging/markers.py
<<<<<<< SEARCH
def _extract_referenced_extras(
    markers: MarkerList, result: set[str] | None = None,
) -> set[str]:
    """Walk a marker tree and collect all extra names referenced in comparisons."""
    if result is None:
        result = set()

    for item in markers:
        if isinstance(item, list):
            _extract_referenced_extras(item, result)
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            extra_name: str | None = None

            # Case 1: variable == "extra" or "extra" == value
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extra_name = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extra_name = lhs.value

            # Case 2: "value" in extras or "value" not in extras (PEP 685)
            # The variable on the right side is "extras"
            elif isinstance(rhs, Variable) and rhs.value == "extras":
                if isinstance(lhs, Value):
                    extra_name = lhs.value

            if extra_name is not None:
                result.add(canonicalize_name(extra_name))

    return result


class InvalidMarker(ValueError):
=======
def _extract_referenced_extras(
    markers: MarkerList, extras_set: set[str] | None = None,
) -> set[str]:
    """Walk a marker tree and collect all extra names referenced in comparisons."""
    if extras_set is None:
        extras_set = set()

    for item in markers:
        if isinstance(item, list):
            _extract_referenced_extras(item, extras_set)
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            extra_name: str | None = None

            # Case 1: variable == "extra" or "extra" == value
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extra_name = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extra_name = lhs.value

            # Case 2: "value" in extras or "value" not in extras (PEP 685)
            # The variable on the right side is "extras"
            elif isinstance(rhs, Variable) and rhs.value == "extras":
                if isinstance(lhs, Value):
                    extra_name = lhs.value

            if extra_name is not None:
                extras_set.add(canonicalize_name(extra_name))

    return extras_set


class InvalidMarker(ValueError):
>>>>>>> REPLACE