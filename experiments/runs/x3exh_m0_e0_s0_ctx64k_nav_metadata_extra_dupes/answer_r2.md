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

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
def _parse_project_urls(data: list[str]) -> dict[str, str]:
=======
def _extract_extra_names(markers: list) -> set[str]:
    """Extract extra names from a marker tree."""
    extra_names: set[str] = set()
    for item in markers:
        if isinstance(item, tuple):
            lhs, op, rhs = item
            if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
                extra_names.add(rhs.value)
            elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
                extra_names.add(lhs.value)
        elif isinstance(item, list):
            extra_names.update(_extract_extra_names(item))
    return extra_names


def _parse_project_urls(data: list[str]) -> dict[str, str]:
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
        normalized_names: list[utils.NormalizedName] = []
        seen: set[utils.NormalizedName] = set()
        try:
            for name in value:
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(
                        f"duplicate {self.raw_name!r} value {name!r}"
                    )
                seen.add(canonical)
                normalized_names.append(canonical)
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

            # Check for undeclared extras in requires_dist markers
            if not any(
                isinstance(e, InvalidMetadata)
                and e.field in {"provides-extra", "requires-dist"}
                for e in collector.errors
            ):
                provides_extra_value = ins.__dict__.get("provides_extra")
                requires_dist_value = ins.__dict__.get("requires_dist")

                if provides_extra_value is not None and requires_dist_value is not None:
                    declared_extras = set(provides_extra_value)
                    for req in requires_dist_value:
                        if req.marker is not None:
                            extra_names = _extract_extra_names(req.marker._markers)
                            for extra_name in extra_names:
                                if extra_name not in declared_extras:
                                    collector.error(
                                        InvalidMetadata(
                                            "requires-dist",
                                            f"extra {extra_name!r} not found in provides-extra"
                                        )
                                    )

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE