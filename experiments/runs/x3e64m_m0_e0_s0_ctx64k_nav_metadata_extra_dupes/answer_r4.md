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
class _Validator(Generic[T]):
=======
def _check_extras_in_markers(
    markers: list[Any],
    provided_extras: set[utils.NormalizedName],
) -> None:
    """Check if all extras referenced in markers are declared in provided_extras."""
    for marker in markers:
        if isinstance(marker, list):
            _check_extras_in_markers(marker, provided_extras)
        elif isinstance(marker, tuple):
            # It's a comparison tuple (lhs, op, rhs)
            lhs, op, rhs = marker
            extra_value = None
            
            if isinstance(lhs, Variable) and lhs.value == "extra":
                if isinstance(rhs, Value):
                    extra_value = rhs.value
            elif isinstance(rhs, Variable) and rhs.value == "extra":
                if isinstance(lhs, Value):
                    extra_value = lhs.value
            
            if extra_value is not None:
                canonical_extra = utils.canonicalize_name(extra_value)
                if canonical_extra not in provided_extras:
                    raise InvalidMetadata(
                        "requires-dist",
                        f"extra {extra_value!r} not declared in provides-extra",
                    )


class _Validator(Generic[T]):
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
        seen = set()
        try:
            for name in value:
                canonical = utils.canonicalize_name(name, validate=True)
                if canonical in seen:
                    raise self._invalid_metadata(
                        f"{canonical!r} is a duplicate provides-extra"
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
=======
                except InvalidMetadata as exc:
                    collector.error(exc)

            # Check for undeclared extras in requires_dist markers
            # Only if both provides_extra and requires_dist are valid (no errors collected for them)
            # and provides_extra is not None.
            has_provides_extra_error = any(
                isinstance(e, InvalidMetadata) and e.field == "provides-extra"
                for e in collector.errors
            )
            has_requires_dist_error = any(
                isinstance(e, InvalidMetadata) and e.field == "requires-dist"
                for e in collector.errors
            )

            if not has_provides_extra_error and not has_requires_dist_error:
                provided_extras = ins.provides_extra
                requires_dist = ins.requires_dist

                if provided_extras is not None:
                    if requires_dist is not None:
                        provided_extras_set = set(provided_extras)
                        for req in requires_dist:
                            if req.marker is not None:
                                _check_extras_in_markers(
                                    req.marker._marker,
                                    provided_extras_set,
                                )

            collector.finalize("invalid metadata")
>>>>>>> REPLACE