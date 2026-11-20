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
        try:
            for name in value:
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(
                        f"duplicate extra name {canonical!r}",
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

<<<<<<< SEARCH
    requires: _Validator[list[str] | None] = _Validator(added="1.1")
    """``Requires`` (deprecated)"""
=======
    requires: _Validator[list[str] | None] = _Validator(added="1.1")
    """``Requires`` (deprecated)"""


def _check_undeclared_extras(
    provides_extra: list[utils.NormalizedName],
    requires_dist: list[requirements.Requirement],
    collector: _ErrorCollector,
) -> None:
    from packaging._parser import Variable, Value

    provides_set = set(provides_extra)
    for req in requires_dist:
        if req.marker is None:
            continue
        _check_marker_extras(req.marker, provides_set, collector)


def _check_marker_extras(
    marker_list: list[Any], provides_set: set[str], collector: _ErrorCollector
) -> None:
    for item in marker_list:
        if isinstance(item, tuple) and len(item) == 3:
            lhs, op, rhs = item
            op_str = op.serialize()
            if op_str in ("==", "!="):
                if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                    extra_name = utils.canonicalize_name(rhs.value)
                    if extra_name not in provides_set:
                        collector.error(
                            InvalidMetadata(
                                "requires-dist",
                                f"extra {rhs.value!r} is not defined in provides-extra",
                            )
                        )
                elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                    extra_name = utils.canonicalize_name(lhs.value)
                    if extra_name not in provides_set:
                        collector.error(
                            InvalidMetadata(
                                "requires-dist",
                                f"extra {lhs.value!r} is not defined in provides-extra",
                            )
                        )
        elif isinstance(item, list):
            _check_marker_extras(item, provides_set, collector)
>>>>>>> REPLACE

<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check undeclared extras if both fields are valid
            try:
                provides_extra = ins.provides_extra
                requires_dist = ins.requires_dist
                if provides_extra is not None and requires_dist is not None:
                    _check_undeclared_extras(provides_extra, requires_dist, collector)
            except InvalidMetadata:
                pass

            collector.finalize("invalid metadata")
>>>>>>> REPLACE