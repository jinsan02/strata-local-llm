### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
def _parse_project_urls(data: list[str]) -> dict[str, str]:
=======
def _extract_extra_names(
    markers: list[Any], extra_names: set[utils.NormalizedName]
) -> None:
    for marker in markers:
        if isinstance(marker, str):
            continue
        if isinstance(marker, list):
            _extract_extra_names(marker, extra_names)
        elif isinstance(marker, tuple):
            lhs, op, rhs = marker
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extra_names.add(utils.canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extra_names.add(utils.canonicalize_name(lhs.value))


def _parse_project_urls(data: list[str]) -> dict[str, str]:
>>>>>>> REPLACE

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

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            if "provides_extra" in ins.__dict__ and "requires_dist" in ins.__dict__ and ins.__dict__["provides_extra"] is not None:
                declared_extras = set(ins.__dict__["provides_extra"])
                undeclared = set()
                for req in ins.__dict__["requires_dist"]:
                    if req.marker is not None:
                        _extract_extra_names(req.marker._markers, undeclared)
                for extra in undeclared:
                    if extra not in declared_extras:
                        collector.error(
                            InvalidMetadata(
                                "requires-dist",
                                f"extra {extra!r} is not declared in provides-extra",
                            )
                        )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE