### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . _parser import Value, Variable
=======
from ._parser import Value, Variable
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
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
        fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
        # Remove fields that have already been checked.
        fields_to_check -= {"metadata_version"}

        failed_keys: set[str] = set()
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
                failed_keys.add(key)

        # Check for undeclared extras in requires_dist markers
        if (
            "provides_extra" not in failed_keys
            and "requires_dist" not in failed_keys
        ):
            provides = ins.provides_extra
            if provides is not None and ins.requires_dist is not None:
                provides_set = set(provides)
                for req in ins.requires_dist:
                    if req.marker is not None:
                        declared = _extract_extras_from_markers(req.marker._markers)
                        undeclared = declared - provides_set
                        if undeclared:
                            collector.error(InvalidMetadata(
                                "requires-dist",
                                f"extra(s) {sorted(undeclared)} not declared in provides-extra",
                            ))

        collector.finalize("invalid metadata")
>>>>>>> REPLACE