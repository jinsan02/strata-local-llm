<<<<<<< SEARCH
from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement

__all__ = [
    "CyclicDependencyGroup",
    "DependencyGroupInclude",
    "DependencyGroupResolver",
    "DuplicateGroupNames",
    "InvalidDependencyGroupObject",
    "resolve_dependency_groups",
]
=======
from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement
from .utils import _validate_regex

__all__ = [
    "CyclicDependencyGroup",
    "DependencyGroupInclude",
    "DependencyGroupResolver",
    "DuplicateGroupNames",
    "InvalidGroupName",
    "InvalidDependencyGroupObject",
    "resolve_dependency_groups",
]


class InvalidGroupName(ValueError):
    """
    An invalid dependency group name; users should refer to the packaging user guide.

    .. versionadded:: NEXT_VERSION
    """
>>>>>>> REPLACE
<<<<<<< SEARCH
       for group_name, value in dependency_groups.items():
           normed_group_name = _normalize_name(group_name)
           original_names.setdefault(normed_group_name, []).append(group_name)
           normalized_groups[normed_group_name] = value
=======
       for group_name, value in dependency_groups.items():
           if not _validate_regex.fullmatch(group_name):
               errors.error(InvalidGroupName(f"Invalid dependency group name: {group_name!r}"))
           normed_group_name = _normalize_name(group_name)
           original_names.setdefault(normed_group_name, []).append(group_name)
           normalized_groups[normed_group_name] = value
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
               raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
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
               raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
           group = _normalize_name(group)
>>>>>>> REPLACE