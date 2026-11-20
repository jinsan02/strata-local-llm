### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from .errors import ExceptionGroup, _ErrorCollector
=======
from .errors import ExceptionGroup, _ErrorCollector
from ._parser import Variable, Value, Op
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
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in normalized_names:
                    raise self._invalid_metadata(
                        f"{name!r} is a duplicate for {self.raw_name!r}"
                    )
                normalized_names.append(canonical)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _get_extra_values_from_marker(marker: list | None) -> set[str]:
    if marker is None:
        return set()
    extras: set[str] = set()
    for item in marker:
        if isinstance(item, str):
            continue
        if isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                if op.serialize() in ("==", "!="):
                    extras.add(utils.canonicalize_name(rhs.value))
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                if op.serialize() in ("==", "!="):
                    extras.add(utils.canonicalize_name(lhs.value))
        elif isinstance(item, list):
            extras.update(_get_extra_values_from_marker(item))
    return extras


class Metadata:
>>>>>>> REPLACE

<<<<<<< SEARCH
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")

        return ins
=======
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            if not any(
                exc.field in ("provides-extra", "requires-dist")
                for exc in collector.errors
            ):
                try:
                    prov_extra = ins.provides_extra
                    req_dist = ins.requires_dist
                    if prov_extra is not None and req_dist is not None:
                        declared = set(prov_extra)
                        for req in req_dist:
                            if req.marker is not None:
                                for extra in _get_extra_values_from_marker(req.marker):
                                    if extra not in declared:
                                        collector.error(
                                            InvalidMetadata(
                                                "requires-dist",
                                                f"extra {extra!r} not declared in provides-extra"
                                            )
                                        )
                except InvalidMetadata:
                    pass

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE