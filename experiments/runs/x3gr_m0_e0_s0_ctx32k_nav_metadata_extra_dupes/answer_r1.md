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
        try:
            for name in value:
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in normalized_names:
                    raise self._invalid_metadata(
                        f"duplicate extra name {normalized!r} in {self.raw_name!r}"
                    )
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
class Metadata:
=======
def _extract_extra_markers(marker_list: list) -> list[str]:
    """Extract canonicalized extra names from a marker list."""
    extras: list[str] = []
    for item in marker_list:
        if isinstance(item, str):
            continue
        if isinstance(item, list):
            extras.extend(_extract_extra_markers(item))
        elif isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                if op.serialize() in ("==", "!="):
                    extras.append(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                if op.serialize() in ("==", "!="):
                    extras.append(lhs.value)
    return extras


class Metadata:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
=======
                    getattr(ins, key)
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            if "provides_extra" in ins._raw and ins._raw["provides_extra"] is not None:
                try:
                    provided_extras = ins.provides_extra
                    required_reqs = ins.requires_dist
                    if provided_extras is not None and required_reqs is not None:
                        for req in required_reqs:
                            if req.marker is not None:
                                for extra in _extract_extra_markers(req.marker._markers):
                                    if extra not in provided_extras:
                                        raise InvalidMetadata(
                                            "requires-dist",
                                            f"extra {extra!r} in {req.name!r} is not declared in provides-extra"
                                        )
                except InvalidMetadata as exc:
                    collector.error(exc)

            collector.finalize("invalid metadata")
>>>>>>> REPLACE