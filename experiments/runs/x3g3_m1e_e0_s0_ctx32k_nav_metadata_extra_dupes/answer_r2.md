### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, markers, requirements, specifiers, utils
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
def _parse_keywords(data: str) -> list[str]:
=======
def _extract_extra_names(marker: markers.MarkerList | None) -> set[str]:
    if marker is None:
        return set()
    extras: set[str] = set()
    for item in marker:
        if isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, markers.Variable) and lhs.value == "extra":
                if isinstance(rhs, markers.Value):
                    extras.add(utils.canonicalize_name(rhs.value))
            elif isinstance(rhs, markers.Variable) and rhs.value == "extra":
                if isinstance(lhs, markers.Value):
                    extras.add(utils.canonicalize_name(lhs.value))
        elif isinstance(item, list):
            extras.update(_extract_extra_names(item))
    return extras


def _parse_keywords(data: str) -> list[str]:
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
        normalized_names: list[utils.NormalizedName] = []
        try:
            for name in value:
                normalized_name = utils.canonicalize_name(name, validate=True)
                if normalized_name in normalized_names:
                    raise self._invalid_metadata(
                        f"{name!r} is a duplicate of {normalized_name!r}"
                    )
                normalized_names.append(normalized_name)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
            collector.finalize("invalid metadata")

        return ins
=======
            # Check for undeclared extras
            if "provides_extra" in ins._raw and ins._raw["provides_extra"] is not None:
                try:
                    declared_extras = set(ins.provides_extra)
                except InvalidMetadata:
                    declared_extras = None

                if declared_extras is not None:
                    try:
                        reqs = ins.requires_dist
                    except InvalidMetadata:
                        reqs = None
                    else:
                        if reqs:
                            for req in reqs:
                                if req.marker:
                                    marker_extras = _extract_extra_names(req.marker)
                                    undeclared = marker_extras - declared_extras
                                    if undeclared:
                                        collector.error(
                                            InvalidMetadata(
                                                "requires-dist",
                                                f"extra(s) {', '.join(sorted(undeclared))!r} not declared in provides-extra"
                                            )
                                        )

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE