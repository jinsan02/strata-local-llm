EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from ._parser import Variable, Value
from .errors import ExceptionGroup, _ErrorCollector
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
                    f"duplicate {self.raw_name!r} value {normalized!r}"
                )
            seen.add(normalized)
            normalized_names.append(normalized)
        return normalized_names
>>>>>>> REPLACE

<<<<<<< SEARCH
class Metadata:
=======
def _validate_extra_markers(
    requires_dist: list[requirements.Requirement] | None,
    provides_extra: list[utils.NormalizedName] | None,
    errors: list[Exception],
) -> None:
    if provides_extra is None or requires_dist is None:
        return

    declared_extras = set(provides_extra)

    for req in requires_dist:
        if req.marker is None:
            continue
        _check_extra_in_list(req.marker.markers, declared_extras, errors)


def _check_extra_in_list(
    markers: list, declared_extras: set[utils.NormalizedName], errors: list[Exception]
) -> None:
    for item in markers:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            _check_extra_in_list(item, declared_extras, errors)
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            extra_val = None
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extra_val = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extra_val = lhs.value

            if extra_val is not None and op.serialize() in ("==", "!="):
                norm_extra = utils.canonicalize_name(extra_val)
                if norm_extra not in declared_extras:
                    errors.append(InvalidMetadata("requires-dist", f"extra {extra_val!r} not declared in provides-extra"))


class Metadata:
>>>>>>> REPLACE

<<<<<<< SEARCH
            collector.finalize("invalid metadata")

        return ins
=======
            # Check for undeclared extras in requires_dist if both fields are valid
            if "provides-extra" not in [e.field for e in collector.errors] and \
               "requires-dist" not in [e.field for e in collector.errors]:
                _validate_extra_markers(ins.requires_dist, ins.provides_extra, collector.errors)

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE