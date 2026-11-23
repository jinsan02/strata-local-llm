### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from ._parser import MarkerList, Variable, Value
from .errors import ExceptionGroup, _ErrorCollector
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


class _Validator(Generic[T]):
=======
_REQUIRED_ATTRS = frozenset(["metadata_version", "name", "version"])


def _extract_extra_comparisons(
    markers: MarkerList,
) -> set[utils.NormalizedName]:
    """Extract normalized extra names from extra comparisons in a marker tree."""
    extras: set[utils.NormalizedName] = set()
    for marker in markers:
        if isinstance(marker, list):
            extras.update(_extract_extra_comparisons(marker))
        elif isinstance(marker, tuple):
            lhs, op, rhs = marker
            extra_value: str | None = None
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extra_value = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extra_value = lhs.value
            if extra_value is not None:
                extras.add(utils.canonicalize_name(extra_value))
    return extras


class _Validator(Generic[T]):
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    def from_raw(cls, data: RawMetadata, *, validate: bool = True) -> Metadata:
        """Create an instance from :class:`RawMetadata`.

        If *validate* is true, all metadata will be validated and all related
        exceptions will be gathered and raised as an :class:`ExceptionGroup`;
        otherwise, validation happens per attribute when it is accessed.
        """
        ins = cls()
        ins._raw = data.copy()  # Mutations occur due to caching enriched values.

        if validate:
            collector = _ErrorCollector()
            metadata_version = None
            with collector.collect(InvalidMetadata):
                metadata_version = ins.metadata_version
                metadata_age = _VALID_METADATA_VERSIONS.index(metadata_version)

            # Make sure to check for the fields that are present, the required
            # fields (so their absence can be reported).
            fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
            # Remove fields that have already been checked.
            fields_to_check -= {"metadata_version"}

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

        return ins
=======
    def from_raw(cls, data: RawMetadata, *, validate: bool = True) -> Metadata:
        """Create an instance from :class:`RawMetadata`.

        If *validate* is true, all metadata will be validated and all related
        exceptions will be gathered and raised as an :class:`ExceptionGroup`;
        otherwise, validation happens per attribute when it is accessed.
        """
        ins = cls()
        ins._raw = data.copy()  # Mutations occur due to caching enriched values.

        if validate:
            collector = _ErrorCollector()
            metadata_version = None
            with collector.collect(InvalidMetadata):
                metadata_version = ins.metadata_version
                metadata_age = _VALID_METADATA_VERSIONS.index(metadata_version)

            # Make sure to check for the fields that are present, the required
            # fields (so their absence can be reported).
            fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
            # Remove fields that have already been checked.
            fields_to_check -= {"metadata_version"}

            # Validate provides_extra and requires_dist first for extra validation
            provides_extra_valid = False
            requires_dist_valid = False
            provides_extra_value: list[utils.NormalizedName] | None = None
            requires_dist_value: list[requirements.Requirement] | None = None

            if "provides_extra" in fields_to_check:
                try:
                    if metadata_version:
                        try:
                            field_metadata_version = Metadata.__dict__["provides_extra"].added
                        except KeyError:
                            pass
                        else:
                            field_age = _VALID_METADATA_VERSIONS.index(
                                field_metadata_version
                            )
                            if field_age > metadata_age:
                                provides_extra_valid = False
                            else:
                                provides_extra_valid = True
                                provides_extra_value = getattr(ins, "provides_extra")
                    else:
                        provides_extra_valid = True
                        provides_extra_value = getattr(ins, "provides_extra")
                except InvalidMetadata:
                    provides_extra_valid = False

            if "requires_dist" in fields_to_check:
                try:
                    if metadata_version:
                        try:
                            field_metadata_version = Metadata.__dict__["requires_dist"].added
                        except KeyError:
                            pass
                        else:
                            field_age = _VALID_METADATA_VERSIONS.index(
                                field_metadata_version
                            )
                            if field_age > metadata_age:
                                requires_dist_valid = False
                            else:
                                requires_dist_valid = True
                                requires_dist_value = getattr(ins, "requires_dist")
                    else:
                        requires_dist_valid = True
                        requires_dist_value = getattr(ins, "requires_dist")
                except InvalidMetadata:
                    requires_dist_valid = False

            # Perform extra validation if both fields are valid
            if provides_extra_valid and requires_dist_valid:
                if provides_extra_value is not None:
                    provides_extra_set = set(provides_extra_value)
                    if requires_dist_value is not None:
                        for req in requires_dist_value:
                            if req.marker is not None:
                                extra_names = _extract_extra_comparisons(
                                    req.marker._markers
                                )
                                for extra_name in extra_names:
                                    if extra_name not in provides_extra_set:
                                        collector.error(
                                            InvalidMetadata(
                                                "requires-dist",
                                                f"extra {extra_name!r} is not in provides-extra",
                                            )
                                        )

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

        return ins
>>>>>>> REPLACE