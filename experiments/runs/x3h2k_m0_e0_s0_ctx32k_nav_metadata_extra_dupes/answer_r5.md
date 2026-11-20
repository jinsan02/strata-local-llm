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
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in seen:
                    raise self._invalid_metadata(
                        f"Duplicate extra name {name!r}"
                    )
                seen.add(normalized)
                normalized_names.append(normalized)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import _parser, licenses, requirements, specifiers, utils
from ._parser import Variable, Value
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    collector.finalize("invalid metadata")

        return ins
=======
    # Check for undeclared extras in requires_dist markers
            provides_extra = ins.__dict__.get("provides_extra")
            requires_dist = ins.__dict__.get("requires_dist")

            if provides_extra is not None and requires_dist is not None:
                declared = set(provides_extra)
                required_extras = set()
                for req in requires_dist:
                    if req.marker is not None:
                        required_extras.update(_extract_extra_comparisons(req.marker._markers))
                
                undeclared = required_extras - declared
                if undeclared:
                    collector.error(InvalidMetadata(
                        "requires-dist",
                        f"Undeclared extra(s): {', '.join(sorted(undeclared))}"
                    ))

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
class Metadata:
=======
def _extract_extra_comparisons(markers_list: list) -> set[str]:
    extras = set()
    for item in markers_list:
        if isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                if op.serialize() == "==":
                    extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                if op.serialize() == "==":
                    extras.add(lhs.value)
        elif isinstance(item, list):
            extras.update(_extract_extra_comparisons(item))
    return extras


class Metadata:
>>>>>>> REPLACE