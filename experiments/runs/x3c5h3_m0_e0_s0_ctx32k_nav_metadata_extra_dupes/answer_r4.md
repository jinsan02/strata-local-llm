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
        seen = set()
        for name in value:
            try:
                canonical = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            
            if canonical in seen:
                raise InvalidMetadata("provides-extra", f"Duplicate provides_extra entry: {name!r}")
            seen.add(canonical)
            normalized_names.append(canonical)
        return normalized_names
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    def _process_requires_dist(
        self,
        value: list[str],
    ) -> list[requirements.Requirement]:
=======
    def _validate_undeclared_extras(
        self, provides_extra: list[utils.NormalizedName], requires_dist: list[requirements.Requirement]
    ) -> None:
        from packaging.markers import Variable, Value

        def _walk_markers(node):
            extras = set()
            if isinstance(node, list):
                for item in node:
                    extras |= _walk_markers(item)
            elif isinstance(node, tuple) and len(node) == 3:
                lhs, op, rhs = node
                is_extra_lhs = isinstance(lhs, Variable) and lhs.value == "extra"
                is_extra_rhs = isinstance(rhs, Variable) and rhs.value == "extra"
                if (is_extra_lhs and isinstance(rhs, Value)) or (is_extra_rhs and isinstance(lhs, Value)):
                    op_str = op.serialize() if hasattr(op, "serialize") else str(op)
                    if op_str == "==":
                        val = rhs.value if isinstance(rhs, Value) else lhs.value
                        extras.add(utils.canonicalize_name(val))
            return extras

        provided = frozenset(provides_extra)
        for req in requires_dist:
            if req.req.marker is None:
                continue
            declared_extras = _walk_markers(req.req.marker._markers)
            for extra in declared_extras:
                if extra not in provided:
                    raise InvalidMetadata(
                        "requires-dist",
                        f"Extra {extra!r} used in marker but not declared in provides_extra",
                    )

    def _process_requires_dist(
        self,
        value: list[str],
    ) -> list[requirements.Requirement]:
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)
            
            try:
                provides = ins.provides_extra
                requires = ins.requires_dist
                if provides is not None and requires is not None:
                    self._validate_undeclared_extras(provides, requires)
            except InvalidMetadata as exc:
                collector.error(exc)

            collector.finalize("invalid metadata")
>>>>>>> REPLACE