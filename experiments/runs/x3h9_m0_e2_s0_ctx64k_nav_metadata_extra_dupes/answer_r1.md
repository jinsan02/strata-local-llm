### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from .errors import ExceptionGroup, _ErrorCollector
=======
from .errors import ExceptionGroup, _ErrorCollector
from ._parser import Variable, Value
from .markers import Marker
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
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in seen:
                    raise self._invalid_metadata(
                        f"duplicate extra: {normalized!r}"
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
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _get_extra_comparisons(marker: Marker | None) -> set[str]:
    """Extract extra names compared with 'extra' variable in a marker."""
    if marker is None:
        return set()
    extras: set[str] = set()
    for item in marker._markers:
        if isinstance(item, tuple) and len(item) == 3:
            lhs, op, rhs = item
            if op.serialize() == "==":
                if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                    extras.add(rhs.value)
                elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                    extras.add(lhs.value)
    return extras


class Metadata:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")

        return ins
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            has_extra_error = any(
                isinstance(e, InvalidMetadata) and e.field == "provides-extra"
                for e in collector.errors
            )
            has_req_error = any(
                isinstance(e, InvalidMetadata) and e.field == "requires-dist"
                for e in collector.errors
            )
            if not has_extra_error and not has_req_error:
                provides_extras = ins.provides_extra
                requires_dists = ins.requires_dist
                if provides_extras is not None and requires_dists is not None:
                    declared_extras = set(provides_extras)
                    for req in requires_dists:
                        if req.marker is not None:
                            for extra_name in _get_extra_comparisons(req.marker):
                                if utils.canonicalize_name(extra_name) not in declared_extras:
                                    collector.error(
                                        InvalidMetadata(
                                            "requires-dist",
                                            f"extra {extra_name!r} is not declared in provides_extra",
                                        )
                                    )

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE