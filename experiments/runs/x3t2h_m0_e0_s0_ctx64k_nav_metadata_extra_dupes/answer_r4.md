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
        for name in value:
            try:
                normalized = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            if normalized in normalized_names:
                raise self._invalid_metadata(
                    f"{normalized!r} is a duplicate for {self.raw_name!r}"
                )
            normalized_names.append(normalized)
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
            if "provides_extra" in ins.__dict__ and "requires_dist" in ins.__dict__:
                provides_extra_set = set(ins.__dict__["provides_extra"])
                from packaging._parser import Variable, Value

                def check_marker_tree(marker_tree):
                    for item in marker_tree:
                        if isinstance(item, list):
                            check_marker_tree(item)
                        elif isinstance(item, tuple):
                            lhs, op, rhs = item
                            extra_name = None
                            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                                extra_name = rhs.value
                            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                                extra_name = lhs.value

                            if extra_name is not None and extra_name not in provides_extra_set:
                                collector.error(
                                    InvalidMetadata("requires-dist", f"extra {extra_name!r} is not declared in Provides-Extra")
                                )

                for req in ins.__dict__["requires_dist"]:
                    if req.marker is not None:
                        check_marker_tree(req.marker._markers)

            collector.finalize("invalid metadata")
>>>>>>> REPLACE