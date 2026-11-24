### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector

if typing.TYPE_CHECKING:
    from collections.abc import Callable

    from .licenses import NormalizedLicenseExpression
    from .version import Version
=======
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from ._parser import MarkerAtom, MarkerLogical, Value, Variable
from .errors import ExceptionGroup, _ErrorCollector

if typing.TYPE_CHECKING:
    from collections.abc import Callable

    from .licenses import NormalizedLicenseExpression
    from .version import Version
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
                normalized_name = utils.canonicalize_name(name, validate=True)
                if normalized_name in normalized_names:
                    raise self._invalid_metadata(
                        f"duplicate {self.raw_name!r}: {normalized_name!r}"
                    )
                normalized_names.append(normalized_name)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE
<<<<<<< SEARCH
class Metadata:
=======
def _check_undeclared_extras(
    marker: MarkerAtom | MarkerLogical,
    provides_extra: list[utils.NormalizedName],
    collector: _ErrorCollector,
) -> None:
    if isinstance(marker, str):
        # Logical operator ("and" or "or"), recurse into children
        return
    if isinstance(marker, list):
        for item in marker:
            _check_undeclared_extras(item, provides_extra, collector)
        return
    if isinstance(marker, tuple):
        lhs, op, rhs = marker
        # Check if this is a comparison involving the "extra" variable
        if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
            normalized_extra = utils.canonicalize_name(rhs.value)
            if normalized_extra not in provides_extra:
                collector.error(
                    InvalidMetadata(
                        "requires-dist",
                        f"extra {rhs.value!r} in marker is not in provides_extra",
                    )
                )
        elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
            normalized_extra = utils.canonicalize_name(lhs.value)
            if normalized_extra not in provides_extra:
                collector.error(
                    InvalidMetadata(
                        "requires-dist",
                        f"extra {lhs.value!r} in marker is not in provides_extra",
                    )
                )


class Metadata:
>>>>>>> REPLACE
<<<<<<< SEARCH
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")

        return ins
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check if provides_extra and requires_dist are valid
            provides_extra_valid = not any(
                isinstance(e, InvalidMetadata) and e.field == "provides-extra"
                for e in collector.errors
            )
            requires_dist_valid = not any(
                isinstance(e, InvalidMetadata) and e.field == "requires-dist"
                for e in collector.errors
            )

            # If both are valid, check for undeclared extras
            if provides_extra_valid and requires_dist_valid:
                provides_extra = ins.provides_extra
                requires_dist = ins.requires_dist
                if provides_extra is not None:
                    for req in requires_dist:
                        if req.marker is not None:
                            _check_undeclared_extras(
                                req.marker._markers, provides_extra, collector
                            )

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE