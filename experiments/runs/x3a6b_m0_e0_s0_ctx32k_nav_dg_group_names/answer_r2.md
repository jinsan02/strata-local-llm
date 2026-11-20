### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
  from .utils import _validate_regex as _validate_name_re
=======
  from .utils import _validate_regex
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
  def _normalize_group_names(
      dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
      errors: _ErrorCollector,
  ) -> dict[str, Sequence[str | Mapping[str, str]]]:
      original_names: dict[str, list[str]] = {}
      normalized_groups: dict[str, Sequence[str | Mapping[str, str]]] = {}

      for group_name, value in dependency_groups.items():
          normed_group_name = _normalize_name(group_name)
          original_names.setdefault(normed_group_name, []).append(group_name)
          normalized_groups[normed_group_name] = value

      for normed_name, names in original_names.items():
          if len(names) > 1:
              errors.error(
                  DuplicateGroupNames(
                      "Duplicate dependency group names: "
                      f"{normed_name} ({', '.join(names)})"
                  )
              )

      return normalized_groups
=======
  def _normalize_group_names(
      dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
      errors: _ErrorCollector,
  ) -> dict[str, Sequence[str | Mapping[str, str]]]:
      original_names: dict[str, list[str]] = {}
      normalized_groups: dict[str, Sequence[str | Mapping[str, str]]] = {}

      for group_name, value in dependency_groups.items():
          if not _validate_regex.fullmatch(group_name):
              errors.error(InvalidGroupName(f"Invalid dependency group name: {group_name!r}"))
          normed_group_name = _normalize_name(group_name)
          original_names.setdefault(normed_group_name, []).append(group_name)
          normalized_groups[normed_group_name] = value

      for normed_name, names in original_names.items():
          if len(names) > 1:
              errors.error(
                  DuplicateGroupNames(
                      "Duplicate dependency group names: "
                      f"{normed_name} ({', '.join(names)})"
                  )
              )

      return normalized_groups
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
          """
          if not _validate_regex.fullmatch(group):
              raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
          group = _normalize_name(group)
>>>>>>> REPLACE