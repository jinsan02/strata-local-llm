EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, markers, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
from .markers import Variable, Value
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
class _Validator(Generic[T]):
=======
def _extract_extra_comparisons(marker_list: list) -> list[str]:
    extras = []
    for item in marker_list:
        if isinstance(item, list):
            extras.extend(_extract_extra_comparisons(item))
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            op_str = op.serialize()
            if op_str in ("==", "!="):
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extras.append(utils.canonicalize_name(rhs.value))
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extras.append(utils.canonicalize_name(lhs.value))
    return extras


class _Validator(Generic[T]):
>>>>>>> REPLACE

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
        try:
            for name in value:
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in normalized_names:
                    raise self._invalid_metadata(
                        f"{self.raw_name!r} contains duplicate extra: {normalized!r}"
                    )
                normalized_names.append(normalized)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist
            has_provides_extra_error = any(
                e.field == "provides-extra" for e in collector.errors
            )
            has_requires_dist_error = any(
                e.field == "requires-dist" for e in collector.errors
            )

            if not has_provides_extra_error and not has_requires_dist_error:
                provides_extra = ins.provides_extra
                requires_dist = ins.requires_dist
                if provides_extra is not None and requires_dist is not None:
                    declared_extras = set(provides_extra)
                    for req in requires_dist:
                        if req.marker is not None:
                            extra_values = _extract_extra_comparisons(req.marker._markers)
                            for extra in extra_values:
                                if extra not in declared_extras:
                                    collector.error(
                                        InvalidMetadata(
                                            "requires-dist",
                                            f"extra {extra!r} in {req.name!r} is not declared in provides_extra"
                                        )
                                    )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE