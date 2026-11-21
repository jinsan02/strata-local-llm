EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
=======
from . import licenses, markers, requirements, specifiers, utils
from . import version as version_module
from ._parser import Op, Value, Variable
from .errors import ExceptionGroup, _ErrorCollector
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
        seen = set()
        for name in value:
            try:
                canonical = utils.canonicalize_name(name, validate=True)
            except utils.InvalidName as exc:
                raise self._invalid_metadata(
                    f"{name!r} is invalid for {self.raw_name!r}", cause=exc
                ) from exc
            
            if canonical in seen:
                raise self._invalid_metadata(
                    f"{canonical!r} is duplicated in {self.raw_name!r}"
                )
            seen.add(canonical)
            normalized_names.append(canonical)
        return normalized_names
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
            collector.finalize("invalid metadata")

        return ins
=======
            collector.finalize("invalid metadata")

            # Check for undeclared extras in requires_dist markers
            # Skip if provides_extra or requires_dist had validation errors
            has_provides_extra_error = any(
                e.field == "provides-extra" for e in collector.errors
            )
            has_requires_dist_error = any(
                e.field == "requires-dist" for e in collector.errors
            )

            if not has_provides_extra_error and not has_requires_dist_error:
                provides_extras = ins.provides_extra
                requires_dists = ins.requires_dist

                if provides_extras is not None and requires_dists is not None:
                    declared_extras = set(provides_extras)
                    for req in requires_dists:
                        if req.marker is not None:
                            extra_names = _extract_extra_names(req.marker)
                            for extra_name in extra_names:
                                if extra_name not in declared_extras:
                                    collector.error(
                                        InvalidMetadata(
                                            "requires-dist",
                                            f"extra {extra_name!r} is not declared in provides_extra",
                                        )
                                    )

        return ins
>>>>>>> REPLACE

EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names
=======
    _process_import_namespaces = _process_import_names


def _extract_extra_names(marker: markers.Marker) -> set[str]:
    """Extract extra names from a marker's comparisons."""
    extras = set()
    raw = marker._markers

    def _visit(node):
        if isinstance(node, list):
            for item in node:
                _visit(item)
        elif isinstance(node, tuple):
            lhs, op, rhs = node
            extra_name = None

            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    if op.serialize() in ("==", "!="):
                        extra_name = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    if op.serialize() in ("==", "!="):
                        extra_name = lhs.value

            if extra_name is not None:
                extras.add(extra_name)

    _visit(raw)
    return extras
>>>>>>> REPLACE