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
  # in the PEP 735 spec, the tables in dependency group lists were described as
  # "Dependency Object Specifiers", but the only defined type of object was a
  # "Dependency Group Include" -- hence the naming of this error as "Object"
  class InvalidDependencyGroupObject(ValueError):
      """
      A member of a dependency group was identified as a dict, but was not in a valid
      format.

      .. versionadded:: 26.1
      """


  # ------------------------
  # Object Model & Interface
  # ------------------------
=======
  # in the PEP 735 spec, the tables in dependency group lists were described as
  # "Dependency Object Specifiers", but the only defined type of object was a
  # "Dependency Group Include" -- hence the naming of this error as "Object"
  class InvalidDependencyGroupObject(ValueError):
      """
      A member of a dependency group was identified as a dict, but was not in a valid
      format.

      .. versionadded:: 26.1
      """


  class InvalidGroupName(ValueError):
      """A dependency group name is invalid."""


  # ------------------------
  # Object Model & Interface
  # ------------------------
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
      for group_name, value in dependency_groups.items():
          normed_group_name = _normalize_name(group_name)
=======
      for group_name, value in dependency_groups.items():
          if not _validate_regex.fullmatch(group_name):
              errors.error(InvalidGroupName(f"group name is invalid: {group_name!r}"))
          
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
=======
      def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
          """
          Lookup a group name, returning the parsed dependency data for that group.
          This will not resolve includes.

          :param group: the name of the group to lookup
          """
          if not _validate_regex.fullmatch(group):
              raise InvalidGroupName(f"group name is invalid: {group!r}")
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
              raise InvalidGroupName(f"group name is invalid: {group!r}")
          group = _normalize_name(group)
>>>>>>> REPLACE