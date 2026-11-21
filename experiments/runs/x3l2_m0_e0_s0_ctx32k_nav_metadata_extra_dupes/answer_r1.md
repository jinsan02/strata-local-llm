### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import licenses, markers, requirements, specifiers, utils
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
        normalized_names: list[utils.NormalizedName] = []
        seen: set[utils.NormalizedName] = set()
        try:
            for name in value:
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in seen:
                    raise self._invalid_metadata(
                        f"{name!r} is a duplicate for {self.raw_name!r}"
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

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    @classmethod
    def from_raw(cls, data: RawMetadata, *, validate: bool = True) -> Metadata:
=======
    @staticmethod
    def _extract_extra_names(marker_list: list) -> set[str]:
        extras: set[str] = set()
        for item in marker_list:
            if isinstance(item, str):
                continue
            if isinstance(item, tuple):
                lhs, op, rhs = item
                if isinstance(lhs, markers.Variable) and lhs.value == "extra":
                    if isinstance(rhs, markers.Value):
                        extras.add(rhs.value)
                elif isinstance(rhs, markers.Variable) and rhs.value == "extra":
                    if isinstance(lhs, markers.Value):
                        extras.add(lhs.value)
            elif isinstance(item, list):
                extras.update(Metadata._extract_extra_names(item))
        return extras

    @staticmethod
    def _check_undeclared_extras(
        provides_extra_raw: list[str] | None,
        requires_dist_raw: list[str] | None,
        collector: _ErrorCollector,
    ) -> None:
        if provides_extra_raw is None:
            return
        try:
            provided = [utils.canonicalize_name(n, validate=True) for n in provides_extra_raw]
        except utils.InvalidName:
            return
        if requires_dist_raw is None:
            return
        try:
            for req_str in requires_dist_raw:
                req = requirements.Requirement(req_str)
                if req.marker is not None:
                    for ename in Metadata._extract_extra_names(req.marker._markers):
                        if utils.canonicalize_name(ename, validate=True) not in provided:
                            collector.error(
                                InvalidMetadata(
                                    "requires-dist",
                                    f"extra {ename!r} in {req_str!r} is not declared in provides_extra",
                                )
                            )
        except Exception:
            pass

    @classmethod
    def from_raw(cls, data: RawMetadata, *, validate: bool = True) -> Metadata:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
              with collector.collect(InvalidMetadata):
                  metadata_version = ins.metadata_version
                  metadata_age = _VALID_METADATA_VERSIONS.index(metadata_version)

              # Make sure to check for the fields that are present, the required
=======
              with collector.collect(InvalidMetadata):
                  metadata_version = ins.metadata_version
                  metadata_age = _VALID_METADATA_VERSIONS.index(metadata_version)
                  Metadata._check_undeclared_extras(
                      ins._raw.get("provides_extra"),
                      ins._raw.get("requires_dist"),
                      collector,
                  )

              # Make sure to check for the fields that are present, the required
>>>>>>> REPLACE