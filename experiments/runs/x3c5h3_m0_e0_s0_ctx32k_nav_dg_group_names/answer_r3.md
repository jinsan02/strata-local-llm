### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement
=======
from .utils import _validate_regex

from .requirements import InvalidRequirement, Requirement
>>>>>>> REPLACE

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
class DuplicateGroupNames(ValueError):
    """
    The same dependency groups were defined twice, with different non-normalized names.

    .. versionadded:: 26.1
    """


class CyclicDependencyGroup(ValueError):
=======
class DuplicateGroupNames(ValueError):
    """
    The same dependency groups were defined twice, with different non-normalized names.

    .. versionadded:: 26.1
    """


class InvalidGroupName(ValueError):
    """
    The dependency group name is not a valid Name field value according to
    the core metadata specification.

    .. versionadded:: 26.1
    """


class CyclicDependencyGroup(ValueError):
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    for group_name, value in dependency_groups.items():
        normed_group_name = _normalize_name(group_name)
=======
    for group_name, value in dependency_groups.items():
        if not _validate_regex.fullmatch(group_name):
            errors.error(InvalidGroupName(repr(group_name)))
        
        normed_group_name = _normalize_name(group_name)
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
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(repr(group))
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
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(repr(group))
        group = _normalize_name(group)

        if group not in self._resolve_cache:
>>>>>>> REPLACE