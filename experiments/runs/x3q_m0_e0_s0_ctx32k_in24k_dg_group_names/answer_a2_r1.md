<<<<<<< SEARCH
__lazy_modules__ = {
    "collections.abc",
    f"{__spec__.parent}.errors",
    f"{__spec__.parent}.requirements",
}

import re
from collections.abc import Mapping, Sequence

from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement
=======
__lazy_modules__ = {
    "collections.abc",
    f"{__spec__.parent}.errors",
    f"{__spec__.parent}.requirements",
    f"{__spec__.parent}.utils",
}

import re
from collections.abc import Mapping, Sequence

from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement
from .utils import _validate_regex
>>>>>>> REPLACE
<<<<<<< SEARCH
__all__ = [
    "CyclicDependencyGroup",
    "DependencyGroupInclude",
    "DependencyGroupResolver",
    "DuplicateGroupNames",
    "InvalidDependencyGroupObject",
    "resolve_dependency_groups",
]
=======
__all__ = [
    "CyclicDependencyGroup",
    "DependencyGroupInclude",
    "DependencyGroupResolver",
    "DuplicateGroupNames",
    "InvalidDependencyGroupObject",
    "InvalidGroupName",
    "resolve_dependency_groups",
]
>>>>>>> REPLACE
<<<<<<< SEARCH
class DuplicateGroupNames(ValueError):
    """
    The same dependency groups were defined twice, with different non-normalized names.

    .. versionadded:: 26.1
    """


# in the PEP 735 spec...
=======
class DuplicateGroupNames(ValueError):
    """
    The same dependency groups were defined twice, with different non-normalized names.

    .. versionadded:: 26.1
    """


class InvalidGroupName(ValueError):
    """
    A dependency group name does not follow the core metadata Name rules.

    .. versionadded:: 26.1
    """


# in the PEP 735 spec...
>>>>>>> REPLACE
<<<<<<< SEARCH
    def __init__(
        self,
        dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    ) -> None:
        errors = _ErrorCollector()

        self.dependency_groups = _normalize_group_names(dependency_groups, errors)
=======
    def __init__(
        self,
        dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    ) -> None:
        errors = _ErrorCollector()

        for group_name in dependency_groups:
            if not _validate_regex.fullmatch(group_name):
                errors.error(InvalidGroupName(f"Invalid group name: {group_name!r}"))

        self.dependency_groups = _normalize_group_names(dependency_groups, errors)
>>>>>>> REPLACE
<<<<<<< SEARCH
    def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
        """
        Lookup a group name, returning the parsed dependency data for that group.
        This will not resolve includes.

        :param group: the name of the group to lookup
        """
        group = _normalize_name(group)
=======
    def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
        """
        Lookup a group name, returning the parsed dependency data for that group.
        This will not resolve includes.

        :param group: the name of the group to lookup
        """
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"Invalid group name: {group!r}")
        group = _normalize_name(group)
>>>>>>> REPLACE
<<<<<<< SEARCH
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        group = _normalize_name(group)
=======
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"Invalid group name: {group!r}")
        group = _normalize_name(group)
>>>>>>> REPLACE