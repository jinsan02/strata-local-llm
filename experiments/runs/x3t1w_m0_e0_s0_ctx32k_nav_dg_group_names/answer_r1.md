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


def __dir__() -> list[str]:
    return __all__


# -----------
# Error Types
# -----------


class DuplicateGroupNames(ValueError):
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


def __dir__() -> list[str]:
    return __all__


# -----------
# Error Types
# -----------


class InvalidGroupName(ValueError):
    """
    The dependency group name does not follow the core metadata Name rules.

    .. versionadded:: 26.4
    """


class DuplicateGroupNames(ValueError):
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
            errors.error(InvalidGroupName(f"invalid dependency group name: {group_name!r}"))
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
            raise InvalidGroupName(f"invalid dependency group name: {group!r}")
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
            raise InvalidGroupName(f"invalid dependency group name: {group!r}")
        group = _normalize_name(group)
>>>>>>> REPLACE