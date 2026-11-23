EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from .errors import ExceptionGroup, _ErrorCollector
=======
from ._parser import Variable, Value
from .errors import ExceptionGroup, _ErrorCollector
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
def _extract_extra_names(
    markers: markers.MarkerAtom | markers.MarkerLogical,
    extras: set[str] | None = None,
) -> set[str]:
    """Extract all extra names referenced in a marker expression.

    Only extracts extra names from direct comparisons like ``extra == "foo"``
    or ``"foo" == extra``.  Does not recurse into ``in extras`` comparisons
    or evaluate ``and`` / ``or`` branches selectively — all branches are
    traversed.

    Returns a set of *un-normalized* extra name strings found in the marker.
    """
    if extras is None:
        extras = set()

    if isinstance(markers, str):
        # "and" or "or" — recurse into children
        return extras

    if isinstance(markers, list):
        for item in markers:
            _extract_extra_names(item, extras)
        return extras

    # It's a tuple: (lhs, op, rhs)
    lhs, op, rhs = markers  # type: ignore[misc]

    extra_name: str | None = None
    if isinstance(lhs, markers.Variable) and lhs.value == "extra":
        if isinstance(rhs, markers.Value):
            extra_name = rhs.value
    elif isinstance(rhs, markers.Variable) and rhs.value == "extra":
        if isinstance(lhs, markers.Value):
            extra_name = lhs.value

    if extra_name is not None:
        extras.add(extra_name)

    return extras
=======
def _extract_extra_names(markers: list[object]) -> set[str]:
    """Extract all extra names referenced in a marker expression."""
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            extras.update(_extract_extra_names(item))
        elif isinstance(item, tuple) and len(item) == 3:
            lhs, op, rhs = item
            extra_name: str | None = None
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extra_name = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extra_name = lhs.value
            if extra_name is not None:
                extras.add(extra_name)
    return extras
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            if "provides_extra" in fields_to_check and "requires_dist" in fields_to_check:
                provides_extra_err = any(
                    isinstance(e, InvalidMetadata) and e.field == "provides-extra"
                    for e in collector.errors
                )
                requires_dist_err = any(
                    isinstance(e, InvalidMetadata) and e.field == "requires-dist"
                    for e in collector.errors
                )
                if not provides_extra_err and not requires_dist_err:
                    provided_extras = set(ins.provides_extra) if ins.provides_extra else set()
                    if provided_extras:
                        for req in ins.requires_dist:
                            if req.marker is not None:
                                for extra_name in _extract_extra_names(req.marker._markers):
                                    if utils.canonicalize_name(extra_name) not in provided_extras:
                                        collector.error(
                                            InvalidMetadata(
                                                "requires-dist",
                                                f"extra {extra_name!r} in {req!r} is not declared in provides-extra",
                                            )
                                        )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE