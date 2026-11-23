### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, markers, requirements, specifiers, utils
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
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in seen:
                    raise self._invalid_metadata(
                        f"duplicate value {normalized!r} for {self.raw_name!r}"
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
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _validate_extra_markers(
    provides_extra: list[utils.NormalizedName],
    requires_dist: list[requirements.Requirement],
) -> list[InvalidMetadata]:
    errors: list[InvalidMetadata] = []
    provided = set(provides_extra)
    for req in requires_dist:
        if req.marker is not None:
            _check_marker_extras(req.marker, provided, errors)
    return errors


def _check_marker_extras(
    marker: list[Any],
    provided: set[utils.NormalizedName],
    errors: list[InvalidMetadata],
) -> None:
    for item in marker:
        if isinstance(item, tuple):
            lhs, op, rhs = item
            if op.serialize() == "==":
                extra_value: str | None = None
                if isinstance(lhs, markers.Variable) and lhs.value == "extra" and isinstance(rhs, markers.Value):
                    extra_value = rhs.value
                elif isinstance(rhs, markers.Variable) and rhs.value == "extra" and isinstance(lhs, markers.Value):
                    extra_value = lhs.value
                
                if extra_value is not None:
                    normalized_extra = utils.canonicalize_name(extra_value)
                    if normalized_extra not in provided:
                        errors.append(InvalidMetadata("requires-dist", f"extra {extra_value!r} is not declared in provides_extra"))
        elif isinstance(item, list):
            _check_marker_extras(item, provided, errors)


class Metadata:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH

            collector.finalize("invalid metadata")

        return ins
=======
            # Extra validation
            extra_field_errors = [
                e for e in collector.errors
                if isinstance(e, InvalidMetadata) and e.field in {"provides-extra", "requires-dist"}
            ]
            if not extra_field_errors:
                provides_extra = ins._raw.get("provides_extra")
                requires_dist = ins._raw.get("requires_dist")
                if provides_extra is not None:
                    extra_errors = _validate_extra_markers(
                        ins.provides_extra,
                        ins.requires_dist,
                    )
                    for err in extra_errors:
                        collector.error(err)

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE