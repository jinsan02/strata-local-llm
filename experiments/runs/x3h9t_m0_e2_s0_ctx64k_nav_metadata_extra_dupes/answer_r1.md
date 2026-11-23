<tool_call>
<function=edit_file>
<parameter=new_string>
    @classmethod
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

            # Check for undeclared extras in requires_dist markers
            try:
                provides_extra = ins.provides_extra
                requires_dist = ins.requires_dist
            except InvalidMetadata:
                # If provides_extra or requires_dist failed to parse, skip this check
                provides_extra = None
                requires_dist = None

            if provides_extra is not None and requires_dist is not None:
                declared_extras = set(provides_extra)
                for req in requires_dist:
                    if req.marker is not None:
                        declared_in_marker = _extract_extras_from_marker(
                            req.marker._markers
                        )
                        undeclared = declared_in_marker - declared_extras
                        for extra in undeclared:
                            collector.error(
                                InvalidMetadata(
                                    "requires-dist",
                                    f"extra {extra!r} in requires_dist is not declared "
                                    f"in provides_extra",
                                )
                            )

            collector.finalize("invalid metadata")

        return ins
</parameter>
<parameter=old_string>
    @classmethod
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
</parameter>
<parameter=path>
src/packaging/metadata.py
</parameter>
</function>
</tool_call>