### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    @property
    def provides_extra(self) -> list[utils.NormalizedName] | None:
        if self._provides_extra is None:
            return None
        return [utils.canonicalize_name(n) for n in self._provides_extra]
=======
    @property
    def provides_extra(self) -> list[utils.NormalizedName] | None:
        if self._provides_extra is None:
            return None
        seen: set[str] = set()
        result: list[str] = []
        for raw in self._provides_extra:
            name = utils.canonicalize_name(raw)
            if name in seen:
                raise InvalidMetadata(
                    f"duplicate provides_extra {raw!r}",
                    field="provides-extra",
                )
            seen.add(name)
            result.append(name)
        return result
>>>>>>> REPLACE
<<<<<<< SEARCH
        if errors:
            raise ExceptionGroup("invalid or unparsed metadata", errors)
        return instance

    metadata_version: _Validator[_MetadataVersion] = _Validator()
=======
        if errors:
            raise ExceptionGroup("invalid or unparsed metadata", errors)
        return instance

    def _collect_extra_names(marker_list: markers_module.MarkerList) -> set[str]:
        extras: set[str] = set()
        for m in marker_list.markers:
            if m.lhs.value == "extra" and isinstance(m.rhs, markers_module.MarkerValue):
                extras.add(m.rhs.value)
            elif m.rhs.value == "extra" and isinstance(m.lhs, markers_module.MarkerValue):
                extras.add(m.lhs.value)
        return extras

    metadata_version: _Validator[_MetadataVersion] = _Validator()
>>>>>>> REPLACE
<<<<<<< SEARCH
        try:
            validated = cls.from_raw(raw, validate=validate)
        except ExceptionGroup as exc_group:
            # The no-branch pragmas cover arcs only seen by Python 3.9.
            for exc in exc_group.exceptions:  # pragma: no branch
                # A required field reported above as unparsed is absent
                # from `raw`, so skip from_raw's duplicate "missing"
                # complaint.
                if not (
                    isinstance(exc, InvalidMetadata)
                    and exc.field in unparsed
                    and _EMAIL_TO_RAW_MAPPING.get(exc.field) not in raw
                ):
                    collector.error(exc)
        else:
            if not collector.errors:  # pragma: no branch
                return validated

        return cls.from_raw(raw, validate=validate)
=======
        try:
            validated = cls.from_raw(raw, validate=validate)
        except ExceptionGroup as exc_group:
            # The no-branch pragmas cover arcs only seen by Python 3.9.
            for exc in exc_group.exceptions:  # pragma: no branch
                # A required field reported above as unparsed is absent
                # from `raw`, so skip from_raw's duplicate "missing"
                # complaint.
                if not (
                    isinstance(exc, InvalidMetadata)
                    and exc.field in unparsed
                    and _EMAIL_TO_RAW_MAPPING.get(exc.field) not in raw
                ):
                    collector.error(exc)
        else:
            if validate:
                if validated.provides_extra is not None:
                    declared_extras = set(validated.provides_extra)
                    if validated.requires_dist is not None:
                        for req in validated.requires_dist:
                            if req.marker is not None:
                                for extra in cls._collect_extra_names(req.marker):
                                    if utils.canonicalize_name(extra) not in declared_extras:
                                        collector.error(
                                            InvalidMetadata(
                                                "requires-dist",
                                                f"extra {extra!r} is not declared in provides_extra",
                                            )
                                        )
            if not collector.errors:  # pragma: no branch
                return validated

        return cls.from_raw(raw, validate=validate)
>>>>>>> REPLACE