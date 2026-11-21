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
_LIST_FIELDS = {
=======
_LIST_FIELDS = {


def _extract_extra_values(markers: list) -> set[str]:
    """Extract extra values compared against the `extra` variable in a marker."""
    extras: set[str] = set()
    for item in markers:
        if isinstance(item, str):
            continue
        if isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extras.add(lhs.value)
            else:
                extras.update(_extract_extra_values([lhs]))
                extras.update(_extract_extra_values([rhs]))
        elif isinstance(item, list):
            extras.update(_extract_extra_values(item))
    return extras
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
=======
    def _process_provides_extra(
        self,
        value: list[str],
    ) -> list[utils.NormalizedName]:
        normalized_names: list[utils.NormalizedName] = []
        seen: set[utils.NormalizedName] = set()
        try:
            for name in value:
                normalized = utils.canonicalize_name(name, validate=True)
                if normalized in seen:
                    raise self._invalid_metadata(
                        f"duplicate provides-extra: {normalized!r}"
                    )
                seen.add(normalized)
                normalized_names.append(normalized)
        except utils.InvalidName as exc:
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
                if ins.provides_extra is not None and ins.requires_dist is not None:
                    for req in ins.requires_dist:
                        if req.marker is not None:
                            declared_extras = _extract_extra_values(req.marker._markers)
                            for extra in declared_extras:
                                if extra not in ins.provides_extra:
                                    collector.error(InvalidMetadata(
                                        "requires-dist",
                                        f"extra {extra!r} is not declared in provides_extra"
                                    ))

                collector.finalize("invalid metadata")

>>>>>>> REPLACE