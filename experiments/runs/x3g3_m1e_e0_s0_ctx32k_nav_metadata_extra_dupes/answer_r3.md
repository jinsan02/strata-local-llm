### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from .errors import ExceptionGroup, _ErrorCollector
=======
from ._parser import Variable, Value
from .errors import ExceptionGroup, _ErrorCollector
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
# Keep the two values in sync.
_VALID_METADATA_VERSIONS = [
=======
def _find_undefined_extras(marker, defined_extras):
    undefined = []
    if isinstance(marker, list):
        for item in marker:
            undefined.extend(_find_undefined_extras(item, defined_extras))
    elif isinstance(marker, tuple):
        lhs, op, rhs = marker
        if op.serialize() == "==":
            extra_name = None
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extra_name = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extra_name = lhs.value
            
            if extra_name is not None and extra_name not in defined_extras:
                undefined.append(extra_name)
    return undefined


# Keep the two values in sync.
_VALID_METADATA_VERSIONS = [
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
                        f"duplicate extra {canonical!r} in {self.raw_name!r}"
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
            provides_extra_ok = True
            requires_dist_ok = True

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
                    if key == "provides_extra":
                        provides_extra_ok = False
                    elif key == "requires_dist":
                        requires_dist_ok = False

            # Check for undefined extras in requires_dist markers
            if (
                provides_extra_ok
                and requires_dist_ok
                and ins.provides_extra is not None
                and ins.requires_dist is not None
            ):
                defined_extras = set(ins.provides_extra)
                for req in ins.requires_dist:
                    if req.marker is not None:
                        undefined_extras = _find_undefined_extras(
                            req.marker._markers, defined_extras
                        )
                        for extra_name in undefined_extras:
                            collector.error(
                                InvalidMetadata(
                                    "requires-dist",
                                    f"extra {extra_name!r} is not defined in provides-extra",
                                )
                            )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE