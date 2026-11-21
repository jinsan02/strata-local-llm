### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
import typing
from typing import (
    Any,
    Generic,
    Literal,
    TypedDict,
    cast,
)

from . import licenses, requirements, specifiers, utils
=======
import typing
from typing import (
    Any,
    Generic,
    Literal,
    TypedDict,
    cast,
)

from . import _parser, licenses, requirements, specifiers, utils
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
                        f"duplicate extra name: {canonical!r}"
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
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _check_marker_for_undeclared_extras(
    marker: Any,
    valid_extras: set[utils.NormalizedName],
    collector: _ErrorCollector,
    req_name: str,
) -> None:
    """Check if an extra in a marker is declared in provides_extra."""
    if isinstance(marker, list):
        for item in marker:
            _check_marker_for_undeclared_extras(item, valid_extras, collector, req_name)
    elif isinstance(marker, tuple):
        lhs, op, rhs = marker
        op_str = op.serialize()
        if op_str not in ("==", "!="):
            return

        # Check for extra == value or value == extra
        if isinstance(lhs, _parser.Variable) and lhs.value == "extra" and isinstance(rhs, _parser.Value):
            extra_name = utils.canonicalize_name(rhs.value)
            if extra_name not in valid_extras:
                collector.error(InvalidMetadata("requires-dist", f"extra {extra_name!r} in requirement {req_name!r} is not provided"))
        elif isinstance(rhs, _parser.Variable) and rhs.value == "extra" and isinstance(lhs, _parser.Value):
            extra_name = utils.canonicalize_name(lhs.value)
            if extra_name not in valid_extras:
                collector.error(InvalidMetadata("requires-dist", f"extra {extra_name!r} in requirement {req_name!r} is not provided"))


class Metadata:
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
            if "provides_extra" in ins._raw and "requires_dist" in ins._raw:
                try:
                    provides_extra = ins.provides_extra
                except InvalidMetadata:
                    provides_extra = None

                if provides_extra is not None:
                    try:
                        requires_dist = ins.requires_dist
                    except InvalidMetadata:
                        requires_dist = None

                    if requires_dist is not None:
                        for req in requires_dist:
                            marker = req.marker
                            if marker is not None:
                                _check_marker_for_undeclared_extras(
                                    marker, set(provides_extra), collector, req.name
                                )

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE