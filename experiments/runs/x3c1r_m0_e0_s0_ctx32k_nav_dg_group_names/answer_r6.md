`packaging/dependency_groups.py` 파일을 수정하여 `InvalidGroupName` 예외와 그룹 이름 검사를 구현한다.

### EDIT: src/packaging/dependency_groups.py
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

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
class CyclicDependencyGroup(ValueError):
=======
class InvalidGroupName(ValueError):
    """
    A dependency group name is invalid.

    .. versionadded:: 26.1
    """


class CyclicDependencyGroup(ValueError):
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
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
from . import utils as pkg_utils
from .requirements import InvalidRequirement, Requirement
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    if errors.errors:
        raise ExceptionGroup(msg, errors.errors)


=======
    if errors.errors:
        raise ExceptionGroup(msg, errors.errors)


def _validate_group_name(name: str) -> None:
    """Validate a dependency group name using the same rules as package names."""
    try:
        pkg_utils.canonicalize_name(name, validate=True)
    except pkg_utils.InvalidName as exc:
        raise InvalidGroupName(f"Invalid dependency group name: {name!r}") from exc


>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    def __init__(
        self,
        dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    ) -> None:
        errors = _ErrorCollector()

        self.dependency_groups = _normalize_group_names(dependency_groups, errors)

        # a map of group names to parsed data
=======
    def __init__(
        self,
        dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    ) -> None:
        errors = _ErrorCollector()

        for name in dependency_groups:
            try:
                _validate_group_name(name)
            except InvalidGroupName as exc:
                errors.error(exc)

        self.dependency_groups = _normalize_group_names(dependency_groups, errors)

        # a map of group names to parsed data
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
        """
        Lookup a group name, returning the parsed dependency data for that group.
        This will not resolve includes.

        :param group: the name of the group to lookup
        """
        group = _normalize_name(group)

        with _ErrorCollector().on_exit(
=======
    def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
        """
        Lookup a group name, returning the parsed dependency data for that group.
        This will not resolve includes.

        :param group: the name of the group to lookup
        """
        _validate_group_name(group)
        group = _normalize_name(group)

        with _ErrorCollector().on_exit(
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        group = _normalize_name(group)

        if group not in self._resolve_cache:
=======
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        _validate_group_name(group)
        group = _normalize_name(group)

        if group not in self._resolve_cache:
>>>>>>> REPLACE