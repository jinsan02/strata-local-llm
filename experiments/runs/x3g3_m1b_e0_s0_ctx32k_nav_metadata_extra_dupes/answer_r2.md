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
        seen = set()
        for name in value:
            try:
                canonical_name = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            if canonical_name in seen:
                raise self._invalid_metadata(
                    f"Duplicate extra name {canonical_name!r} in {self.raw_name!r}"
                )
            seen.add(canonical_name)
            normalized_names.append(canonical_name)
        return normalized_names
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    requires_external: _Validator[list[str] | None] = _Validator(added="1.2")
=======
    requires_external: _Validator[list[str] | None] = _Validator(added="1.2")

    def _extract_extra_names(self, marker: MarkerList) -> set[str]:
        """Extract extra names from a marker list."""
        extra_names: set[str] = set()
        self._extract_extra_names_recursive(marker, extra_names)
        return extra_names

    def _extract_extra_names_recursive(
        self, node: MarkerAtom | MarkerLogical, extra_names: set[str]
    ) -> None:
        if isinstance(node, list):
            for item in node:
                self._extract_extra_names_recursive(item, extra_names)
        elif isinstance(node, str):
            # "and" or "or"
            pass
        elif isinstance(node, tuple):
            lhs, op, rhs = node
            if op.serialize() in ("==", "!="):
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extra_names.add(rhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extra_names.add(lhs.value)
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    requires: _Validator[list[str] | None] = _Validator(added="1.1")
=======
    requires: _Validator[list[str] | None] = _Validator(added="1.1")

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

            # Check provides_extra and requires_dist first to determine if we should
            # check for undeclared extras.
            provides_extra_valid = True
            requires_dist_valid = True
            provides_extra_value = None
            requires_dist_value = None

            if "provides_extra" in fields_to_check or "provides_extra" in _REQUIRED_ATTRS:
                try:
                    provides_extra_value = ins.provides_extra
                except InvalidMetadata:
                    provides_extra_valid = False

            if "requires_dist" in fields_to_check or "requires_dist" in _REQUIRED_ATTRS:
                try:
                    requires_dist_value = ins.requires_dist
                except InvalidMetadata:
                    requires_dist_valid = False

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

            # Check for undeclared extras
            if (
                provides_extra_valid
                and requires_dist_valid
                and provides_extra_value is not None
            ):
                declared_extras = set(provides_extra_value)
                for req in requires_dist_value:
                    if req.marker:
                        # Parse marker and check for extra comparisons
                        # We need to extract extra names from the marker
                        extra_names = cls._extract_extra_names(cls, req.marker._marker)
                        for extra_name in extra_names:
                            if extra_name not in declared_extras:
                                collector.error(
                                    InvalidMetadata(
                                        "requires-dist",
                                        f"Extra {extra_name!r} in {req.name!r} is not defined in provides-extra"
                                    )
                                )

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE