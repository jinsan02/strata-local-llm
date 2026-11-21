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
      The dependency group name is invalid.

      .. versionadded:: 26.2
      """


  # ------------------------
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
  from .errors import _ErrorCollector
  from .requirements import InvalidRequirement, Requirement
=======
  from .errors import _ErrorCollector
  from .requirements import InvalidRequirement, Requirement
  from .utils import _validate_regex
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
          normed_group_name = _normalize_name(group_name)
          original_names.setdefault(normed_group_name, []).append(group_name)
          normalized_groups[normed_group_name] = value
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
          :param group: the name of the group to lookup
          """
          group = _normalize_name(group)
=======
          :param group: the name of the group to lookup
          """
          if not _validate_regex.fullmatch(group):
              raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
          group = _normalize_name(group)
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
          :param group: the name of the group to resolve
          """
          group = _normalize_name(group)
=======
          :param group: the name of the group to resolve
          """
          if not _validate_regex.fullmatch(group):
              raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
          group = _normalize_name(group)
>>>>>>> REPLACE