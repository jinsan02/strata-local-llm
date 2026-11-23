### EDIT: src/packaging/metadata.py
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
_RAW_TO_EMAIL_MAPPING = {raw: email for email, raw in _EMAIL_TO_RAW_MAPPING.items()}
=======
_RAW_TO_EMAIL_MAPPING = {raw: email for email, raw in _EMAIL_TO_RAW_MAPPING.items()}


def _check_undeclared_extras(
    marker: Any, declared_extras: set[str]
) -> set[str]:
    """Extract extra names from marker comparisons that are not in declared_extras."""
    undeclared: set[str] = set()
    if isinstance(marker, tuple):
        lhs, op, rhs = marker
        op_str = str(op)
        if op_str in ("==", "!="):
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                if rhs.value not in declared_extras:
                    undeclared.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                if lhs.value not in declared_extras:
                    undeclared.add(lhs.value)
    elif isinstance(marker, list):
        for item in marker:
            undeclared |= _check_undeclared_extras(item, declared_extras)
    return undeclared
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
                        f"duplicate extra: {name!r}"
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

            # Check for undeclared extras in requires_dist markers
            if not collector.errors:
                provides_extra_set = set(ins.provides_extra) if ins.provides_extra else None
                if (
                    provides_extra_set is not None
                    and "requires_dist" in ins.__dict__
                    and ins.requires_dist is not None
                ):
                    for req in ins.requires_dist:
                        if req.marker is not None:
                            for extra in _check_undeclared_extras(req.marker, provides_extra_set):
                                collector.error(
                                    InvalidMetadata(
                                        "requires-dist",
                                        f"extra {extra!r} in marker is not declared in provides-extra",
                                    )
                                )

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE