### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
  import re
  from collections.abc import Mapping, Sequence
  
  from .errors import _ErrorCollector
  from .requirements import InvalidRequirement, Requirement
=======
  import re
  from collections.abc import Iterable, Mapping, Sequence
  
  from .errors import _ErrorCollector
  from .requirements import InvalidRequirement, Requirement
  from .utils import _validate_regex
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

          _validate_group_names(dependency_groups.keys(), errors)
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
          _validate_single_group_name(group)
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
          _validate_single_group_name(group)
          group = _normalize_name(group)
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
      return normalized_groups


# ----------------
# internal helpers
# ----------------


_NORMALIZE_PATTERN = re.compile(r"[-_.]+")
=======
      return normalized_groups


def _validate_single_group_name(group: str) -> None:
    """Raise InvalidGroupName if group name is invalid."""
    if not _validate_regex.fullmatch(group):
        raise InvalidGroupName(f"group name is invalid: {group!r}")


def _validate_group_names(
    group_names: Iterable[str], errors: _ErrorCollector
) -> None:
    """Validate group names and collect InvalidGroupName errors for each invalid one."""
    for group_name in group_names:
        if not _validate_regex.fullmatch(group_name):
            errors.error(InvalidGroupName(f"group name is invalid: {group_name!r}"))


# ----------------
# internal helpers
# ----------------


_NORMALIZE_PATTERN = re.compile(r"[-_.]+")
>>>>>>> REPLACE