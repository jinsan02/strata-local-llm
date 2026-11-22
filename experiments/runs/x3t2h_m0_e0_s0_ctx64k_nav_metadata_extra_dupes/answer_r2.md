### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
=======
from . import _parser, licenses, requirements, specifiers, utils
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

<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names
=======
    _process_import_namespaces = _process_import_names


def _check_undeclared_extras(
    provides_extra: list[utils.NormalizedName],
    requires_dist: list[requirements.Requirement] | None,
) -> None:
    if requires_dist is None:
        return
    declared = set(provides_extra)
    for req in requires_dist:
        if req.marker is None:
            continue
        _check_marker_extras(req.marker._markers, declared)


def _check_marker_extras(markers: list, declared: set) -> None:
    for marker in markers:
        if isinstance(marker, list):
            _check_marker_extras(marker, declared)
        elif isinstance(marker, tuple):
            lhs, op, rhs = marker
            if isinstance(lhs, _parser.Variable) and lhs.value == "extra" and isinstance(rhs, _parser.Value):
                if rhs.value not in declared:
                    raise InvalidMetadata("requires-dist", f"extra {rhs.value!r} is not declared in provides-extra")
            elif isinstance(rhs, _parser.Variable) and rhs.value == "extra" and isinstance(lhs, _parser.Value):
                if lhs.value not in declared:
                    raise InvalidMetadata("requires-dist", f"extra {lhs.value!r} is not declared in provides-extra")
>>>>>>> REPLACE

<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires-dist
            try:
                provides_extra_val = ins.provides_extra
                requires_dist_val = ins.requires_dist
            except InvalidMetadata:
                provides_extra_val = None
                requires_dist_val = None

            if provides_extra_val is not None:
                try:
                    _check_undeclared_extras(provides_extra_val, requires_dist_val)
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
>>>>>>> REPLACE