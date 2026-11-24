EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, markers, requirements, specifiers, utils
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
def _parse_keywords(data: str) -> list[str]:
=======
def _extract_extra_names_from_markers(
    markers: markers.MarkerList | None,
) -> set[utils.NormalizedName]:
    """Extract normalized extra names from a marker AST."""
    if markers is None:
        return set()
    
    extras: set[utils.NormalizedName] = set()
    
    def _visit(node: Any) -> None:
        if isinstance(node, list):
            for item in node:
                _visit(item)
        elif isinstance(node, tuple):
            lhs, op, rhs = node
            if isinstance(lhs, markers.Variable) and lhs.value == "extra":
                if isinstance(rhs, markers.Value) and op.serialize() in ("==", "!="):
                    extras.add(utils.canonicalize_name(rhs.value))
            elif isinstance(rhs, markers.Variable) and rhs.value == "extra":
                if isinstance(lhs, markers.Value) and op.serialize() in ("==", "!="):
                    extras.add(utils.canonicalize_name(lhs.value))
    
    _visit(markers)
    return extras


def _parse_keywords(data: str) -> list[str]:
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
            collector.finalize("invalid metadata")

        return ins
=======
            # Check for unregistered extras in requires_dist markers
            has_provides_extra_error = any(
                isinstance(e, InvalidMetadata) and e.field == "provides-extra"
                for e in collector.errors
            )
            has_requires_dist_error = any(
                isinstance(e, InvalidMetadata) and e.field == "requires-dist"
                for e in collector.errors
            )
            
            if not has_provides_extra_error and not has_requires_dist_error:
                provides_extra = ins.__dict__.get("provides_extra")
                if provides_extra is not None:
                    declared_extras = set(provides_extra)
                    requires_dist = ins.__dict__.get("requires_dist")
                    if requires_dist:
                        for req in requires_dist:
                            if req.marker is not None:
                                extra_names = _extract_extra_names_from_markers(req.marker._markers)
                                for extra_name in extra_names:
                                    if extra_name not in declared_extras:
                                        collector.error(
                                            InvalidMetadata(
                                                "requires-dist",
                                                f"extra {extra_name!r} in {req.name!r} is not declared in provides_extra"
                                            )
                                        )

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE