### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
from packaging._parser import Variable, Value
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
        return value

    _process_import_namespaces = _process_import_names


class Metadata:
=======
        return value

    _process_import_namespaces = _process_import_names


def _collect_extra_names(marker_list: list) -> set[str]:
    """Extract extra names from a marker list."""
    extras: set[str] = set()
    for item in marker_list:
        if isinstance(item, str):
            continue
        if isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extras.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extras.add(lhs.value)
        elif isinstance(item, list):
            extras.update(_collect_extra_names(item))
    return extras


class Metadata:
>>>>>>> REPLACE

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
                    collector.error(exc)

            collector.finalize("invalid metadata")

        return ins
=======
                    collector.error(exc)

            # Check undeclared extras in requires_dist markers
            if "provides_extra" in ins._raw and "requires_dist" in ins._raw:
                try:
                    prov_extras = ins.provides_extra
                    reqs = ins.requires_dist
                    if prov_extras is not None and reqs is not None:
                        undeclared = set()
                        for req in reqs:
                            if req.marker is not None:
                                extra_names = _collect_extra_names(req.marker._markers)
                                for extra in extra_names:
                                    if utils.canonicalize_name(extra) not in set(prov_extras):
                                        undeclared.add(extra)
                        for extra in undeclared:
                            collector.error(
                                InvalidMetadata(
                                    "requires-dist",
                                    f"extra {extra!r} is not declared in provides_extra",
                                )
                            )
                except InvalidMetadata:
                    # Skip if provides_extra or requires_dist itself is invalid
                    pass

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE