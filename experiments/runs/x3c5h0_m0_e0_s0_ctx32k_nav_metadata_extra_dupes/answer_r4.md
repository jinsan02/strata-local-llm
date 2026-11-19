EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from ._parser import Variable, Value
from . import licenses, requirements, specifiers, utils
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
def _parse_project_urls(data: list[str]) -> dict[str, str]:
    """Parse a list of label/URL string pairings separated by a comma."""
=======
def _extract_extra_literals(markers: list[Any]) -> set[str]:
    """Extract all extra names compared to the 'extra' marker variable."""
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, str):
            continue
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extras.add(lhs.value)
        elif isinstance(item, list):
            extras.update(_extract_extra_literals(item))
    return extras


def _parse_project_urls(data: list[str]) -> dict[str, str]:
    """Parse a list of label/URL string pairings separated by a comma."""
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    def _process_provides_extra(
        self,
        value: list[str],
    ) -> list[utils.NormalizedName]:
        normalized_names = []
        try:
            for name in value:
                normalized_names.append(utils.canonicalize_name(name, validate=True))
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
=======
    def _process_provides_extra(
        self,
        value: list[str],
    ) -> list[utils.NormalizedName]:
        normalized_names = []
        seen: set[utils.NormalizedName] = set()
        try:
            for name in value:
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(f"{name!r} is a duplicate provides-extra")
                seen.add(canonical)
                normalized_names.append(canonical)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                    collector.error(exc)

            # Cross-field validation: undeclared extras
            if validate:
                try:
                    provided = ins.provides_extra
                    reqs = ins.requires_dist or []
                    if provided is not None:
                        provided_set = set(provided)
                        for req in reqs:
                            if req.marker is None:
                                continue
                            extra_names = _extract_extra_literals(req.marker.markers)
                            for name in extra_names:
                                if name not in provided_set:
                                    collector.error(
                                        InvalidMetadata(
                                            "requires-dist",
                                            f"extra {name!r} is not defined in provides-extra",
                                        )
                                    )
                except InvalidMetadata:
                    # Skip check if provides_extra or requires_dist failed validation.
                    pass

            collector.finalize("invalid metadata")
>>>>>>> REPLACE