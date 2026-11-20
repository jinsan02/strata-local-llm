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
=======
    def _process_provides_extra(
        self,
        value: list[str],
    ) -> list[utils.NormalizedName]:
        normalized_names = []
        try:
            for name in value:
                norm = utils.canonicalize_name(name, validate=True)
                if norm in normalized_names:
                    raise InvalidMetadata(
                        self.raw_name, f"Duplicate extra {norm!r}"
                    )
                normalized_names.append(norm)
=======
     @classmethod
    def from_raw(cls, data: RawMetadata, *, validate: bool = True) -> Metadata:
        ins = cls()
        ins._raw = data.copy()

        if validate:
            collector = _ErrorCollector()
            metadata_version = None
            with collector.collect(InvalidMetadata):
                metadata_version = ins.metadata_version
                metadata_age = _VALID_METADATA_VERSIONS.index(metadata_version)

                fields_to_check = frozenset(ins._raw) | _REQUIRED_ATTRS
                fields_to_check -= {"metadata_version"}

                for key in fields_to_check:
                    try:
                        if metadata_version:
                            field_metadata_version = Metadata.__dict__[key].added
                            field_age = _VALID_METADATA_VERSIONS.index(field_metadata_version)
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

                _validate_undeclared_extras(ins, collector)

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    requires: _Validator[list[str] | None] = _Validator(added="1.1")
=======
    requires: _Validator[list[str] | None] = _Validator(added="1.1")


def _validate_undeclared_extras(ins: Metadata, collector: _ErrorCollector) -> None:
    if any(e.field == "provides-extra" for e in collector.errors):
        return
    if any(e.field == "requires-dist" for e in collector.errors):
        return

    raw_provides = ins._raw.get("provides_extra")
    if not raw_provides:
        return

    valid_extras = frozenset(raw_provides)

    requires_dist = ins.requires_dist
    if requires_dist is None:
        return

    for req in requires_dist:
        marker = req.marker
        if not marker:
            continue
        _check_marker_extra_declarations(marker, valid_extras, collector)


def _check_marker_extra_declarations(
    marker: Any, valid_extras: frozenset[str], collector: _ErrorCollector
) -> None:
    from ._parser import Variable, Value

    if isinstance(marker, tuple):
        lhs, op, rhs = marker
        is_extra_lhs = isinstance(lhs, Variable) and lhs.value == "extra"
        is_extra_rhs = isinstance(rhs, Variable) and rhs.value == "extra"

        if is_extra_lhs and isinstance(rhs, Value):
            extra_name = rhs.value
        elif is_extra_rhs and isinstance(lhs, Value):
            extra_name = lhs.value
        else:
            return

        norm_extra = utils.canonicalize_name(extra_name, validate=False)
        if norm_extra not in valid_extras:
            collector.error(InvalidMetadata("requires-dist", f"Extra {norm_extra!r} is not declared in provides-extra"))
    elif isinstance(marker, list):
        for item in marker:
            _check_marker_extra_declarations(item, valid_extras, collector)
>>>>>>> REPLACE