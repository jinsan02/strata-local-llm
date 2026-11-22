<tool_call>
<function=edit_file>
<parameter=new_string>
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
            if "provides_extra" in fields_to_check and "requires_dist" in fields_to_check:
                try:
                    provides_extra = ins.provides_extra
                    requires_dist = ins.requires_dist
                    if provides_extra is not None and requires_dist is not None:
                        declared_extras = set(provides_extra)
                        for req in requires_dist:
                            if req.marker is not None:
                                raw_marker = req.marker._markers
                                extra_names = _get_extra_names_from_marker(raw_marker)
                                for extra in extra_names:
                                    if utils.canonicalize_name(extra) not in declared_extras:
                                        raise InvalidMetadata(
                                            "requires-dist",
                                            f"extra {extra!r} in requirement marker is not declared in provides_extra",
                                        )
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
</parameter>
<parameter=old_string>
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
</parameter>
<parameter=path>
src/packaging/metadata.py
</parameter>
</function>
</tool_call>