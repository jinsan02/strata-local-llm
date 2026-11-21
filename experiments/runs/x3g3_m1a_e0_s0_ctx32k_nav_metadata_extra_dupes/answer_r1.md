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
from . import licenses, markers, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector

if typing.TYPE_CHECKING:
    from collections.abc import Callable

    from .licenses import NormalizedLicenseExpression
    from .markers import MarkerList, Value, Variable
    from .version import Version
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _check_marker_for_extra(
    marker: MarkerList,
    provides_extra: set[utils.NormalizedName],
    collector: _ErrorCollector,
) -> None:
    for item in marker:
        if isinstance(item, list):
            _check_marker_for_extra(item, provides_extra, collector)
        elif item in ("and", "or"):
            continue
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if op.serialize() in ("==", "!="):
                if isinstance(lhs, Variable) and lhs.value == "extra":
                    if isinstance(rhs, Value):
                        extra_name = utils.canonicalize_name(rhs.value)
                        if extra_name not in provides_extra:
                            collector.error(InvalidMetadata("requires-dist", f"extra {extra_name!r} not in provides-extra"))
                elif isinstance(rhs, Variable) and rhs.value == "extra":
                    if isinstance(lhs, Value):
                        extra_name = utils.canonicalize_name(lhs.value)
                        if extra_name not in provides_extra:
                            collector.error(InvalidMetadata("requires-dist", f"extra {extra_name!r} not in provides-extra"))


class Metadata:
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
        seen_names = set()
        try:
            for name in value:
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in seen_names:
                    raise self._invalid_metadata(
                        f"duplicate {self.raw_name!r} value {name!r}"
                    )
                seen_names.add(normalized)
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
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")

        return ins
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras
            try:
                provides_extra = ins.provides_extra
                requires_dist = ins.requires_dist
                if provides_extra is not None and requires_dist is not None:
                    provides_extra_set = set(provides_extra)
                    for req in requires_dist:
                        if req.marker is not None:
                            _check_marker_for_extra(req.marker._marker, provides_extra_set, collector)
            except InvalidMetadata:
                # If provides_extra or requires_dist validation failed, skip this check
                pass

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE