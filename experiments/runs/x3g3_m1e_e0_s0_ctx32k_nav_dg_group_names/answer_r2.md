### EDIT: src/packaging/dependency_groups.py
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
      A dependency group name is invalid.

      .. versionadded:: 26.1
      """


  class CyclicDependencyGroup(ValueError):
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
          :raises InvalidGroupName: If the group name is invalid.
          """
          if not _validate_regex.fullmatch(group):
              raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
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
          :raises InvalidGroupName: If the group name is invalid.
          """
          if not _validate_regex.fullmatch(group):
              raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
          group = _normalize_name(group)
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    for group_name, value in dependency_groups.items():
        normed_group_name = _normalize_name(group_name)
        original_names.setdefault(normed_group_name, []).append(group_name)
        normalized_groups[normed_group_name] = value
=======
    for group_name, value in dependency_groups.items():
        if not _validate_regex.fullmatch(group_name):
            errors.error(InvalidGroupName(f"Invalid dependency group name: {group_name!r}"))
            continue

        normed_group_name = _normalize_name(group_name)
        original_names.setdefault(normed_group_name, []).append(group_name)
        normalized_groups[normed_group_name] = value
>>>>>>> REPLACE