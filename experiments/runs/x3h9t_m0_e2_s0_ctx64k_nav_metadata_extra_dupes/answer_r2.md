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

<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _get_extra_names_from_marker(marker_tree: list) -> set[str]:
    extra_names: set[str] = set()
    for item in marker_tree:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            extra_names.update(_get_extra_names_from_marker(item))
        elif isinstance(item, tuple) and len(item) == 3:
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extra_names.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extra_names.add(lhs.value)
    return extra_names


class Metadata:
>>>>>>> REPLACE

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
                        f"duplicate extra name {canonical!r} in {self.raw_name!r}"
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
            if not any(
                e.field in ("provides-extra", "requires-dist") for e in collector.errors
            ):
                provides_extras = ins.provides_extra
                if provides_extras is not None:
                    requires_dists = ins.requires_dist
                    if requires_dists is not None:
                        for req in requires_dists:
                            if req.marker is not None:
                                declared_extras = set(provides_extras)
                                for extra_name in _get_extra_names_from_marker(
                                    req.marker._markers
                                ):
                                    if extra_name not in declared_extras:
                                        collector.error(
                                            InvalidMetadata(
                                                "requires-dist",
                                                f"extra {extra_name!r} in marker is not declared in provides-extra",
                                            )
                                        )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE