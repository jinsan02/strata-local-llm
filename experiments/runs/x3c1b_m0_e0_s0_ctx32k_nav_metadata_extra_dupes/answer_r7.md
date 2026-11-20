### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
from __future__ import annotations

__lazy_modules__ = {
    "email.header",
    "email.parser",
    "keyword",
    "pathlib",
    f"{__spec__.parent}",
    f"{__spec__.parent}.errors",
}

import email.header
import email.message
import email.parser
import email.policy
import keyword
import pathlib
import re
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
from __future__ import annotations

__lazy_modules__ = {
    "email.header",
    "email.parser",
    "keyword",
    "pathlib",
    f"{__spec__.parent}",
    f"{__spec__.parent}.errors",
}

import email.header
import email.message
import email.parser
import email.policy
import keyword
import pathlib
import re
import typing
from typing import (
    Any,
    Generic,
    Literal,
    TypedDict,
    cast,
)

from ._parser import Value
from . import licenses, requirements, specifiers, utils
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
                canon = utils.canonicalize_name(name, validate=True)
                if canon in seen:
                    raise self._invalid_metadata(
                        f"{name!r} is a duplicate provides-extra", cause=None
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

### EDIT: src/packaging/metadata.py
<<<<<<< SEARCH
    _process_import_namespaces = _process_import_names


class Metadata:
=======
    _process_import_namespaces = _process_import_names


def _get_undefined_extras(
    marker_tree: Any, provided_extras: set[utils.NormalizedName]
) -> set[utils.NormalizedName]:
    """Walk a parsed marker tree and find extra values not in provided_extras."""
    undefined = set()

    if isinstance(marker_tree, tuple):
        lhs, op, rhs = marker_tree
        extra_value = None
        
        # Check for extra == "value" or "value" == extra
        # We only check Value (literal) against Variable("extra")
        if hasattr(lhs, 'value') and getattr(lhs, 'value', None) == "extra" and isinstance(rhs, Value):
            extra_value = rhs.value
        elif hasattr(rhs, 'value') and getattr(rhs, 'value', None) == "extra" and isinstance(lhs, Value):
            extra_value = lhs.value
            
        if extra_value is not None:
            canon = utils.canonicalize_name(extra_value)
            if canon not in provided_extras:
                undefined.add(canon)
    elif isinstance(marker_tree, list):
        for item in marker_tree:
            undefined.update(_get_undefined_extras(item, provided_extras))
            
    return undefined


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

            # 2. Check for undefined extras in requires_dist markers
            # Only if validation passed for provides_extra and requires_dist fields
            fields_with_errors = {exc.field for exc in collector.errors}
            
            if "provides-extra" not in fields_with_errors and \
               "requires-dist" not in fields_with_errors:
               
                provided_extras = set(ins.provides_extra) if ins.provides_extra else None

                if provided_extras is not None:
                    for req in ins.requires_dist:
                        # Access internal marker structure to inspect variable comparisons
                        m_obj = req.marker
                        if m_obj:
                            try:
                                tree = m_obj._marker
                            except AttributeError:
                                continue 
                            
                            undefined = _get_undefined_extras(tree, provided_extras)
                            for extra_name in undefined:
                                collector.error(InvalidMetadata("requires-dist", f"Extra '{extra_name}' is not defined in provides_extra."))

            collector.finalize("invalid metadata")

        return ins
>>>>>>> REPLACE