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
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector
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
from collections.abc import Set as AbstractSet
from typing import (
    Any,
    Generic,
    Literal,
    TypeAlias,
    TypedDict,
    cast,
)

from ._parser import Variable, Value
from . import licenses, requirements, specifiers, utils
from . import version as version_module
from .errors import ExceptionGroup, _ErrorCollector

MarkerList: TypeAlias = "list[Any]"
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
        seen = set()
        try:
            for name in value:
                normalized_name = utils.canonicalize_name(name, validate=True)
                if normalized_name in seen:
                    raise self._invalid_metadata(
                        f"Duplicate provides-extra {normalized_name!r}"
                    )
                seen.add(normalized_name)
                normalized_names.append(normalized_name)
        except utils.InvalidName as exc:
            raise self._invalid_metadata(
                f"{name!r} is invalid for {self.raw_name!r}", cause=exc
            ) from exc
        else:
            return normalized_names
>>>>>>> REPLACE
<<<<<<< SEARCH
    def _process_license_files(self, value: list[str]) -> list[str]:
        paths = []
        for path in value:
=======
def _find_extra_markers_in_node(node: Any) -> set[utils.NormalizedName]:
    extras: set[utils.NormalizedName] = set()
    if isinstance(node, list):
        for item in node:
            extras.update(_find_extra_markers_in_node(item))
    elif isinstance(node, tuple):
        lhs, op, rhs = node
        if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
            extras.add(rhs.value)
        elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
            extras.add(lhs.value)
    return extras


def _get_extra_markers(marker_list: MarkerList | None) -> set[utils.NormalizedName]:
    if marker_list is None:
        return set()
    extras = set()
    for atom in marker_list:
        extras.update(_find_extra_markers_in_node(atom))
    return extras


class _Validator(Generic[T]):
    # ... (Rest of the class remains, but we need to insert this before Metadata class or keep it as a standalone function)
    # Actually, based on file structure, let's place it just before _Validator class definition
    pass 

# We need to replace the existing _Validator class definition area with the function added.
# However, finding exact match for search is hard if we don't know where _Validator starts exactly in the text snippet.
# Let's find the start of _Validator class and add the helper function right before it.

class _Validator(Generic[T]):
<<<<<<< SEARCH
    def _process_license_files(self, value: list[str]) -> list[str]:
        paths = []
        for path in value:
=======
def _find_extra_markers_in_node(node: Any) -> set[utils.NormalizedName]:
    extras: set[utils.NormalizedName] = set()
    if isinstance(node, list):
        for item in node:
            extras.update(_find_extra_markers_in_node(item))
    elif isinstance(node, tuple):
        lhs, op, rhs = node
        if isinstance(lhs, Variable) and lhs.value == "extra" and isinstance(rhs, Value):
            extras.add(rhs.value)
        elif isinstance(rhs, Variable) and rhs.value == "extra" and isinstance(lhs, Value):
            extras.add(lhs.value)
    return extras


def _get_extra_markers(marker_list: MarkerList | None) -> set[utils.NormalizedName]:
    if marker_list is None:
        return set()
    extras = set()
    for atom in marker_list:
        extras.update(_find_extra_markers_in_node(atom))
    return extras

# We must also update the _Validator class start. The file snippet had it after _process_import_names.
# But let's just put the function before _Validator class definition if we can find that block.
# Wait, I see `class _Validator(Generic[T]):` appears twice in my thought process logic vs actual file structure.
# In the provided file:
# Line 566: class _Validator(Generic[T]):
# We should insert the helper functions right before line 566.

    def _process_license_files(self, value: list[str]) -> list[str]:
        paths = []
        for path in value:
>>>>>>> REPLACE