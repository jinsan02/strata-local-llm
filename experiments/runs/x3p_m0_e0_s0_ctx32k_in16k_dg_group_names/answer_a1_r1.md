### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
import re
from collections.abc import Mapping, Sequence

from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement
=======
import re
from collections.abc import Mapping, Sequence

from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement
from .utils import _validate_regex
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
__all__ = [
    "CyclicDependencyGroup",
    "DuplicateGroupNames",
    "InvalidDependencyGroupObject",
    "DependencyGroupInclude",
    "DependencyGroupResolver",
    "resolve_dependency_groups",
]
=======
__all__ = [
    "CyclicDependencyGroup",
    "DuplicateGroupNames",
    "InvalidDependencyGroupObject",
    "DependencyGroupInclude",
    "DependencyGroupResolver",
    "InvalidGroupName",
    "resolve_dependency_groups",
]
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
class InvalidDependencyGroupObject(ValueError):
    """
    A member of a dependency group was identified as a dict, but was not in a valid
    format.

    .. versionadded:: 26.1
    """


# ------------------------
=======
class InvalidDependencyGroupObject(ValueError):
    """
    A member of a dependency group was identified as a dict, but was not in a valid
    format.

    .. versionadded:: 26.1
    """


class InvalidGroupName(ValueError):
    """
    Raised when a dependency group name does not conform to the core metadata `Name` rules.

    .. versionadded:: 26.1
    """


# ------------------------
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
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

        for key in dependency_groups:
            if not _validate_regex.fullmatch(key):
                errors.error(InvalidGroupName(f"{key!r}"))

        self.dependency_groups = _normalize_group_names(dependency_groups, errors)
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
=======
    def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
        """
        Lookup a group name, returning the parsed dependency data for that group.
        This will not resolve includes.

        :param group: the name of the group to lookup
        """
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"{group!r}")
        group = _normalize_name(group)
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
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
            raise InvalidGroupName(f"{group!r}")
        group = _normalize_name(group)
>>>>>>> REPLACE