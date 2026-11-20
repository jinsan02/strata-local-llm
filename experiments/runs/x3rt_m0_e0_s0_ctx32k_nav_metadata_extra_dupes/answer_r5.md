### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
from .markers import Variable, Value
>>>>>>> REPLACE
<<<<<<< SEARCH
class _Validator(Generic[T]):
=======
def _extract_extra_from_marker(marker: Any) -> set[str]:
    if isinstance(marker, tuple):
        lhs, op, rhs = marker
        op_str = op.serialize() if hasattr(op, "serialize") else str(op)
        if op_str in ("==", "!="):
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    return {utils.canonicalize_name(rhs.value)}
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    return {utils.canonicalize_name(lhs.value)}
        return set()
    elif isinstance(marker, list):
        result = set()
        for item in marker:
            result |= _extract_extra_from_marker(item)
        return result
    return set()


class _Validator(Generic[T]):
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
        for name in value:
            try:
                normalized = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            if normalized in seen:
                raise self._invalid_metadata(
                    f"duplicate extra name {normalized!r} in {self.raw_name!r}"
                )
            seen.add(normalized)
            normalized_names.append(normalized)
        return normalized_names
>>>>>>> REPLACE
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check undeclared extras if both fields are present and valid
            if "provides_extra" in ins.__dict__ and "requires_dist" in ins.__dict__:
                provided = ins.__dict__["provides_extra"]
                if provided is not None:
                    declared_set = set(provided)
                    for req in ins.__dict__["requires_dist"]:
                        if req.marker:
                            undeclared = _extract_extra_from_marker(req.marker) - declared_set
                            if undeclared:
                                collector.error(InvalidMetadata(
                                    "requires-dist",
                                    f"extra(s) {', '.join(sorted(undeclared))} not declared in provides-extra"
                                ))

            collector.finalize("invalid metadata")
>>>>>>> REPLACE