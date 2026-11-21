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
        seen: set[utils.NormalizedName] = set()
        try:
            for name in value:
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in seen:
                    raise self._invalid_metadata(
                        f"{name!r} is a duplicate of a previously seen extra "
                        f"for {self.raw_name!r}"
                    )
                seen.add(normalized)
                normalized_names.append(normalized)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE
<<<<<<< SEARCH
        for name, validator in cls.__dict__.items():
            if isinstance(validator, _Validator):
                if name not in raw:
                    if validate:
                        collector.error(
                            InvalidMetadata(
                                _EMAIL_TO_RAW_MAPPING[name],
                                f"{_EMAIL_TO_RAW_MAPPING[name]!r} is a required field",
                            )
                        )
                    continue
                value = raw[name]
                try:
                    processed = validator._process(value)
                except Exception as exc:
                    if validate:
                        collector.error(exc)
                    else:
                        raise exc
                else:
                    object.__setattr__(validated, name, processed)
=======
        for name, validator in cls.__dict__.items():
            if isinstance(validator, _Validator):
                if name not in raw:
                    if validate:
                        collector.error(
                            InvalidMetadata(
                                _EMAIL_TO_RAW_MAPPING[name],
                                f"{_EMAIL_TO_RAW_MAPPING[name]!r} is a required field",
                            )
                        )
                    continue
                value = raw[name]
                try:
                    processed = validator._process(value)
                except Exception as exc:
                    if validate:
                        collector.error(exc)
                    else:
                        raise exc
                else:
                    object.__setattr__(validated, name, processed)
        
        if validate:
            validated._check_extra_references(collector)
>>>>>>> REPLACE
<<<<<<< SEARCH
    def as_rfc822(self) -> RFC822Message:
=======
    def _check_extra_references(self, collector: _ErrorCollector) -> None:
        """Check that extra references in requires_dist markers are declared in provides_extra."""
        provides_extra = self.provides_extra
        requires_dist = self.requires_dist
        if provides_extra is None or requires_dist is None:
            return

        valid_extras = set(provides_extra)
        for req in requires_dist:
            if req.marker is not None:
                for extra_name in _extract_extra_names(req.marker._markers):
                    if extra_name not in valid_extras:
                        collector.error(
                            InvalidMetadata(
                                "requires-dist",
                                f"{extra_name!r} is not declared in provides-extra",
                            )
                        )

    def as_rfc822(self) -> RFC822Message:
>>>>>>> REPLACE