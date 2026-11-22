EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _collect_extra_names(marker: list | tuple) -> set[str]:
    result: set[str] = set()
    if isinstance(marker, list):
        for item in marker:
            result.update(_collect_extra_names(item))
    elif isinstance(marker, tuple):
        lhs, op, rhs = marker
        if op.serialize() in ("==", "!="):
            if hasattr(lhs, "value") and lhs.value == "extra" and hasattr(rhs, "value"):
                result.add(utils.canonicalize_name(rhs.value))
            elif hasattr(rhs, "value") and rhs.value == "extra" and hasattr(lhs, "value"):
                result.add(utils.canonicalize_name(lhs.value))
    return result


class Metadata:
>>>>>>> REPLACE
<<<<<<< SEARCH
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
=======
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

            # Check for undeclared extras in requires_dist markers
            extra_field_errors = {
                e.field for e in collector.errors if isinstance(e, InvalidMetadata)
            }
            if "provides-extra" not in extra_field_errors and "requires-dist" not in extra_field_errors:
                prov_extras = set(ins.provides_extra) if ins.provides_extra else set()
                if prov_extras and ins.requires_dist:
                    for req in ins.requires_dist:
                        if req.marker:
                            undeclared = _collect_extra_names(req.marker) - prov_extras
                            for undecl in undeclared:
                                collector.error(InvalidMetadata(
                                    "requires-dist",
                                    f"extra {undecl!r} is not declared in provides_extra"
                                ))

            collector.finalize("invalid metadata")
>>>>>>> REPLACE