### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, markers, requirements, specifiers, utils
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
class Metadata:
=======
def _extract_extra_names(marker: Any) -> set[str]:
    """Extract canonicalized extra names from a marker AST."""
    extras: set[str] = set()
    if isinstance(marker, tuple):
        lhs, op, rhs = marker
        if op.serialize() == "==":
            if isinstance(lhs, markers.Variable) and lhs.value == "extra":
                if isinstance(rhs, markers.Value):
                    extras.add(utils.canonicalize_name(rhs.value))
            elif isinstance(rhs, markers.Variable) and rhs.value == "extra":
                if isinstance(lhs, markers.Value):
                    extras.add(utils.canonicalize_name(lhs.value))
    elif isinstance(marker, list):
        for item in marker:
            extras.update(_extract_extra_names(item))
    return extras


class Metadata:
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
        try:
            for name in value:
                normalized_names.append(utils.canonicalize_name(name, validate=True))
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            seen: set[utils.NormalizedName] = set()
            for norm_name in normalized_names:
                if norm_name in seen:
                    raise self._invalid_metadata(
                        f"duplicate extra: {norm_name!r}"
                    )
                seen.add(norm_name)
            return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
            for key in fields_to_check:
                try:
                    if metadata_version:
                        # Can't use getattr() as that triggers descriptor protocol which
                        # will fail due to no value for the instance argument.
                        try:
                            field_metadata_version = Metadata.__dict__[key].added
                        except KeyError:
                            exc = InvalidMetadata(key, f"unrecognized field: {key!r}")
                            collector.error(exc)
                            continue
                        field_age = _VALID_METADATA_VERSIONS.index(
                            field_metadata_version
                        )
                        if field_age > metadata_age:
                            field = _RAW_TO_EMAIL_MAPPING[key]
                            exc = InvalidMetadata(
                                field,
                                f"{field} introduced in metadata version "
                                f"{field_metadata_version}, not {metadata_version}",
                            )
                            collector.error(exc)
                            continue
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
            for key in fields_to_check:
                try:
                    if metadata_version:
                        # Can't use getattr() as that triggers descriptor protocol which
                        # will fail due to no value for the instance argument.
                        try:
                            field_metadata_version = Metadata.__dict__[key].added
                        except KeyError:
                            exc = InvalidMetadata(key, f"unrecognized field: {key!r}")
                            collector.error(exc)
                            continue
                        field_age = _VALID_METADATA_VERSIONS.index(
                            field_metadata_version
                        )
                        if field_age > metadata_age:
                            field = _RAW_TO_EMAIL_MAPPING[key]
                            exc = InvalidMetadata(
                                field,
                                f"{field} introduced in metadata version "
                                f"{field_metadata_version}, not {metadata_version}",
                            )
                            collector.error(exc)
                            continue
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            if ins.provides_extra is not None and ins.requires_dist is not None:
                # Skip if either field had validation errors
                field_errors = {e.field for e in collector.errors}
                if "provides-extra" not in field_errors and "requires-dist" not in field_errors:
                    provided = set(ins.provides_extra)
                    for req in ins.requires_dist:
                        if req.marker is not None:
                            marker_extras = _extract_extra_names(req.marker._markers)
                            for extra in marker_extras:
                                if extra not in provided:
                                    collector.error(InvalidMetadata(
                                        "requires-dist",
                                        f"extra {extra!r} not declared in provides-extra"
                                    ))

            collector.finalize("invalid metadata")
>>>>>>> REPLACE