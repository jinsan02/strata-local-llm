EDIT: src/packaging/metadata.py
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
        seen: set[utils.NormalizedName] = set()
        try:
            for name in value:
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(
                        f"duplicate {self.raw_name!r} value: {name!r}"
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

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
def _parse_keywords(data: str) -> list[str]:
=======
def _parse_keywords(data: str) -> list[str]:
    """Split a string of comma-separated keywords into a list of keywords."""
    return [k.strip() for k in data.split(",")]


def _collect_extra_literals(marker_data: Any) -> set[str]:
    """Recursively collect extra literal values from marker comparison tuples."""
    result: set[str] = set()
    if isinstance(marker_data, list):
        for item in marker_data:
            result |= _collect_extra_literals(item)
    elif isinstance(marker_data, tuple):
        lhs, op, rhs = marker_data
        # Only consider equality/inequality checks involving the 'extra' variable
        if getattr(op, 'value', None) in ("==", "!="):
            extra_value: str | None = None
            if getattr(lhs, 'value', None) == 'extra' and hasattr(rhs, 'value'):
                extra_value = rhs.value
            elif getattr(rhs, 'value', None) == 'extra' and hasattr(lhs, 'value'):
                extra_value = lhs.value
            
            if extra_value is not None:
                result.add(extra_value)
    return result


def _check_undeclared_extras(
    instance: Metadata,
    collector: _ErrorCollector,
) -> None:
    """Validate that extras referenced in requires_dist markers are declared."""
    provides_extra_raw = instance._raw.get("provides_extra")
    if provides_extra_raw is None:
        return

    declared = set(instance.provides_extra)  # Already processed/normalized
    requires_dist_raw = instance._raw.get("requires_dist")
    if requires_dist_raw is None:
        return

    for req_str in requires_dist_raw:
        try:
            req = requirements.Requirement(req_str)
        except requirements.InvalidRequirement:
            continue  # Skip malformed requirement strings entirely
        
        if req.marker is None:
            continue

        try:
            marker_list = req.marker._marker_list
        except AttributeError:
            marker_list = getattr(req.marker, "markers", [])

        for extra_name in _collect_extra_literals(marker_list):
            if utils.canonicalize_name(extra_name) not in declared:
                collector.error(InvalidMetadata(
                    "requires-dist",
                    f"extra(s) '{extra_name}' is required but not declared in provides-extra"
                ))


def _parse_keywords(data: str) -> list[str]:
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
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
                            errored_fields.add(key)
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
                            errored_fields.add(key)
                            continue
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)
                    errored_fields.add(key)

            if "provides_extra" not in errored_fields and "requires_dist" not in errored_fields:
                _check_undeclared_extras(ins, collector)

            collector.finalize("invalid metadata")
>>>>>>> REPLACE