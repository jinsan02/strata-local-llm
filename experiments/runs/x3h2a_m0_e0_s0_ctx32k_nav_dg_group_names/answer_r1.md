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
      An invalid dependency group name.

      .. versionadded:: 26.1
      """

      def __init__(self, name: str) -> None:
          super().__init__(f"name is invalid: {name!r}")


  # ------------------------
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
  def _normalize_group_names(
      dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
      errors: _ErrorCollector,
  ) -> dict[str, Sequence[str | Mapping[str, str]]]:
      original_names: dict[str, list[str]] = {}
      normalized_groups: dict[str, Sequence[str | Mapping[str, str]]] = {}

      for group_name, value in dependency_groups.items():
          normed_group_name = _normalize_name(group_name)
=======
  def _normalize_group_names(
      dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
      errors: _ErrorCollector,
  ) -> dict[str, Sequence[str | Mapping[str, str]]]:
      original_names: dict[str, list[str]] = {}
      normalized_groups: dict[str, Sequence[str | Mapping[str, str]]] = {}

      for group_name, value in dependency_groups.items():
          if not _validate_regex.fullmatch(group_name):
              errors.error(InvalidGroupName(group_name))

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
              raise InvalidGroupName(group)

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
              raise InvalidGroupName(group)

          group = _normalize_name(group)
>>>>>>> REPLACE