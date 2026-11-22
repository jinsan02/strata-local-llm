### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from ._parser import ParsedRequirement, parse_marker, parse_requirement
=======
from ._parser import ParsedRequirement, parse_marker, parse_requirement, Variable, Value
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
class _Validator(Generic[T]):
=======
def _get_extra_names(markers: list) -> set[str]:
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            extras.update(_get_extra_names(item))
        elif isinstance(item, tuple) and len(item) == 3:
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extras.add(lhs.value)
    return extras


class _Validator(Generic[T]):
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
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
        seen = set()
        try:
            for name in value:
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(
                        f"duplicate extra name {name!r}"
                    )
                seen.add(canonical)
                normalized_names.append(canonical)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check undeclared extras in requires-dist markers
            provides_extra = ins.__dict__.get("provides_extra")
            requires_dist = ins.__dict__.get("requires_dist")
            if provides_extra is not None and requires_dist is not None:
                declared = set(provides_extra)
                for req in requires_dist:
                    if req.marker is not None:
                        for extra in _get_extra_names(req.marker._markers):
                            if extra not in declared:
                                collector.error(InvalidMetadata(
                                    "requires-dist",
                                    f"extra {extra!r} in marker is not declared in Provides-Extra"
                                ))

            collector.finalize("invalid metadata")
>>>>>>> REPLACE