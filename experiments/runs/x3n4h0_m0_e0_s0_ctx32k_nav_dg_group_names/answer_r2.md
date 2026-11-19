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
# in the PEP 735 spec, the tables in dependency group lists were described as
# "Dependency Object Specifiers", but the only defined type of object was a
# "Dependency Group Include" -- hence the naming of this error as "Object"
class InvalidDependencyGroupObject(ValueError):
=======
# Core metadata spec for `Name` (reused for dependency group names)
_GROUP_NAME_VALIDATION_RE = re.compile(
    r"[a-z0-9]|[a-z0-9][a-z0-9._-]*[a-z0-9]", re.IGNORECASE | re.ASCII
)


class InvalidGroupName(ValueError):
    """
    The dependency group name is invalid according to the PEP 508 rules.

    .. versionadded:: 26.1
    """


def _validate_group_name(name: str) -> None:
    if not _GROUP_NAME_VALIDATION_RE.fullmatch(name):
        raise InvalidGroupName(f"name is invalid: {name!r}")


# in the PEP 735 spec, the tables in dependency group lists were described as
# "Dependency Object Specifiers", but the only defined type of object was a
# "Dependency Group Include" -- hence the naming of this error as "Object"
class InvalidDependencyGroupObject(ValueError):
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
      for group_name, value in dependency_groups.items():
          normed_group_name = _normalize_name(group_name)
          original_names.setdefault(normed_group_name, []).append(group_name)
          normalized_groups[normed_group_name] = value
=======
      for group_name, value in dependency_groups.items():
          if not _GROUP_NAME_VALIDATION_RE.fullmatch(group_name):
              errors.error(InvalidGroupName(f"name is invalid: {group_name!r}"))
          normed_group_name = _normalize_name(group_name)
          original_names.setdefault(normed_group_name, []).append(group_name)
          normalized_groups[normed_group_name] = value
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
              f"[dependency-groups] data for {group!r} was malformed"
          ) as errors:
              return self._parse_group(group, errors)
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
              f"[dependency-groups] data for {group!r} was malformed"
          ) as errors:
              return self._parse_group(group, errors)
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
              with _ErrorCollector().on_exit(
                  f"[dependency-groups] data for {group!r} was malformed"
              ) as errors:
                  self._validate(group, group, [], set(), errors)

          return self._resolve(group)
=======
      def resolve(self, group: str) -> tuple[Requirement, ...]:
          """
          Resolve a dependency group to a list of requirements.

          :param group: the name of the group to resolve
          """
          _validate_group_name(group)
          group = _normalize_name(group)

          if group not in self._resolve_cache:
              with _ErrorCollector().on_exit(
                  f"[dependency-groups] data for {group!r} was malformed"
              ) as errors:
                  self._validate(group, group, [], set(), errors)

          return self._resolve(group)
>>>>>>> REPLACE