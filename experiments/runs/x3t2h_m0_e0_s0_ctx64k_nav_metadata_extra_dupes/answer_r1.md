### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
T = typing.TypeVar("T")


__all__ = [
=======
T = typing.TypeVar("T")


def _extract_extra_names(marker: markers.Marker | None) -> set[str]:
    """Extract all extra names compared against the 'extra' variable in a marker."""
    if marker is None:
        return set()
    
    extra_names: set[str] = set()
    def _walk(nodes: list) -> None:
        for node in nodes:
            if isinstance(node, list):
                _walk(node)
            elif isinstance(node, tuple):
                lhs, op, rhs = node
                if isinstance(lhs, markers.Variable) and lhs.value == "extra" and isinstance(rhs, markers.Value):
                    extra_names.add(rhs.value)
                elif isinstance(rhs, markers.Variable) and rhs.value == "extra" and isinstance(lhs, markers.Value):
                    extra_names.add(lhs.value)
    _walk(marker._markers)
    return extra_names


__all__ = [
>>>>>>> REPLACE
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
        try:
            for name in value:
                normalized_name = utils.canonicalize_name(name, validate=True)
                if normalized_name in normalized_names:
                    raise self._invalid_metadata(
                        "provides-extra",
                        f"duplicate extra name {normalized_name!r}",
                    )
                normalized_names.append(normalized_name)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE
<<<<<<< SEARCH
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            if ins.__dict__.get("provides_extra") is not None and "requires_dist" in ins.__dict__:
                declared = set(ins.__dict__["provides_extra"])
                for req in ins.__dict__["requires_dist"]:
                    if req.marker:
                        for extra_name in _extract_extra_names(req.marker):
                            if extra_name not in declared:
                                collector.error(
                                    InvalidMetadata(
                                        "requires-dist",
                                        f"extra {extra_name!r} in marker is not in provides-extra",
                                    )
                                )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE