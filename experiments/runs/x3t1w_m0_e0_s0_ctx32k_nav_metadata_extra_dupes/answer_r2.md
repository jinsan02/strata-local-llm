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
                normalized_name = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc

            if normalized_name in normalized_names:
                raise InvalidMetadata(
                    self.raw_name, f"{normalized_name!r} is a duplicate provides-extra"
                )

            normalized_names.append(normalized_name)
        return normalized_names
>>>>>>> REPLACE
<<<<<<< SEARCH
            collector.finalize("invalid metadata")

        return ins
=======
            # Check consistency of extras between requires-dist and provides-extra
            try:
                Metadata._check_extra_consistency(ins, collector)
            except InvalidMetadata as exc:
                collector.error(exc)

            collector.finalize("invalid metadata")

        return ins

    @staticmethod
    def _check_extra_consistency(
        ins: "Metadata", collector: typing.Any  # _ErrorCollector
    ) -> None:
        """Validate that extras referenced in requires_dist markers are declared in provides_extra."""
        from packaging.markers import Variable, Value
        
        # Skip check if either field is missing or failed validation (still present in _raw)
        if "provides_extra" in ins._raw or "requires_dist" in ins._raw:
            return

        provided_extras = set(ins.provides_extra)
        requires_dists = ins.requires_dist or []

        for req in requires_dists:
            marker = req.marker
            if not marker:
                continue
            
            _check_marker_extra_refs(marker._markers, provided_extras, collector)

def _check_marker_extra_refs(markers, provided_extras, collector):
    """Recursively check extra references in marker structure."""
    from packaging.markers import Variable, Value
    
    for node in markers:
        if isinstance(node, tuple):
            lhs, op, rhs = node
            op_str = op.serialize()
            
            # Check only equality/inequality comparisons (e.g., extra == "foo")
            # "in" / "not in" compare against the extras set itself and are excluded.
            if op_str not in ("==", "!="):
                continue
            
            canonical_extra = None
            
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    canonical_extra = utils.canonicalize_name(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    canonical_extra = utils.canonicalize_name(lhs.value)
            
            if canonical_extra is not None and canonical_extra not in provided_extras:
                collector.error(InvalidMetadata("requires-dist", f"Extra {canonical_extra!r} in requires_dist marker is not declared in provides_extra"))
        elif isinstance(node, list):
            # Traverse nested logical groups (and/or) or parentheses
            _check_marker_extra_refs(node, provided_extras, collector)
>>>>>>> REPLACE