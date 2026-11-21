### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from ._parser import Variable, Value
from .errors import ExceptionGroup, _ErrorCollector
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
class _Validator(Generic[T]):
=======
def _extract_extra_values(marker) -> set[str]:
    """Extract canonicalized extra values from a marker structure."""
    extras: set[str] = set()
    if not marker:
        return extras
    stack = [marker]
    while stack:
        node = stack.pop()
        if isinstance(node, list):
            stack.extend(node)
        elif isinstance(node, tuple):
            if len(node) == 3:
                lhs, op, rhs = node
                op_str = op.serialize()
                if op_str in ("==", "!="):
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
        try:
            for name in value:
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in normalized_names:
                    raise self._invalid_metadata(
                        f"duplicate extra {normalized!r} in {self.raw_name!r}"
                    )
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
            try:
                provides_extra = ins.provides_extra
                requires_dist = ins.requires_dist
                if provides_extra is not None and requires_dist is not None:
                    declared_extras = set(provides_extra)
                    for req in requires_dist:
                        if req.marker is not None:
                            for extra_val in _extract_extra_values(req.marker._marker):
                                if extra_val not in declared_extras:
                                    collector.error(
                                        InvalidMetadata(
                                            "requires-dist",
                                            f"extra {extra_val!r} is not declared in provides-extra",
                                        )
                                    )
            except InvalidMetadata:
                pass  # Skip if provides_extra or requires_dist validation failed

            collector.finalize("invalid metadata")
>>>>>>> REPLACE