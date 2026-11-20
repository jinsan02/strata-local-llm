### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
  from . import licenses, requirements, specifiers, utils
=======
  from . import licenses, markers, requirements, specifiers, utils
>>>>>>> REPLACE
<<<<<<< SEARCH
def _parse_project_urls(data: list[str]) -> dict[str, str]:
=======
def _extract_marker_extras(marker_value: list | tuple) -> set[str]:
    """Extract extra names from a parsed marker tree."""
    extras = set()
    if isinstance(marker_value, tuple):
        lhs, op, rhs = marker_value
        if isinstance(lhs, markers.Variable) and lhs.value == "extra":
            extras.add(str(rhs))
        elif isinstance(rhs, markers.Variable) and rhs.value == "extra":
            extras.add(str(lhs))
    elif isinstance(marker_value, list):
        for item in marker_value:
            extras.update(_extract_marker_extras(item))
    return extras

def _parse_project_urls(data: list[str]) -> dict[str, str]:
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
        seen = set()
        try:
            for name in value:
                canon = utils.canonicalize_name(name, validate=True)
                if canon in seen:
                    raise self._invalid_metadata(
                        "provides-extra", f"duplicate extra {name!r} after normalization"
                    )
                seen.add(canon)
                normalized_names.append(canon)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")

        return ins
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in markers if both fields validated successfully
            if "provides_extra" not in ins._raw and "requires_dist" not in ins._raw:
                try:
                    provides = ins.provides_extra
                    dists = ins.requires_dist
                    if provides is not None and dists is not None:
                        valid_extras = set(provides)
                        for req in dists:
                            if req.marker is not None:
                                parsed = markers.Marker(req.marker).value
                                for extra in _extract_marker_extras(parsed):
                                    if extra not in valid_extras:
                                        raise ins._invalid_metadata(
                                            "requires-dist", 
                                            f"extra {extra!r} is not declared by provides-extra"
                                        )
                except InvalidMetadata as e:
                    collector.error(e)

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE