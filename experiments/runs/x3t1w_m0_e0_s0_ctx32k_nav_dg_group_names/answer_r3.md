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
      """
      An invalid dependency group name; the name does not conform to the
      core metadata ``Name`` field rules.

      .. versionadded:: 26.1
      """


  # ------------------------
>>>>>>> REPLACE
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
            errors.error(InvalidGroupName(f"name is invalid: {group_name!r}"))
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
<<<<<<< SEARCH
      def __init__(
          self,
          dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
      ) -> None:
          errors = _ErrorCollector()

          self.dependency_groups = _normalize_group_names(dependency_groups, errors)

          # a map of group names to parsed data
          self._parsed_groups: dict[
              str, tuple[Requirement | DependencyGroupInclude, ...]
          ] = {}
          # a cache of completed resolutions to Requirement lists
          self._resolve_cache: dict[str, tuple[Requirement, ...]] = {}

          errors.finalize("[dependency-groups] data was invalid")
=======
      def __init__(
          self,
          dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
      ) -> None:
          errors = _ErrorCollector()

          self.dependency_groups = _normalize_group_names(dependency_groups, errors)

          # a map of group names to parsed data
          self._parsed_groups: dict[
              str, tuple[Requirement | DependencyGroupInclude, ...]
          ] = {}
          # a cache of completed resolutions to Requirement lists
          self._resolve_cache: dict[str, tuple[Requirement, ...]] = {}

          errors.finalize("[dependency-groups] data was invalid")

      def _validate_group_name(self, name: str) -> None:
          if not _validate_regex.fullmatch(name):
              raise InvalidGroupName(f"name is invalid: {name!r}")
>>>>>>> REPLACE
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
          self._validate_group_name(group)
          group = _normalize_name(group)

          with _ErrorCollector().on_exit(
              f"[dependency-groups] data for {group!r} was malformed"
          ) as errors:
              return self._parse_group(group, errors)
>>>>>>> REPLACE
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
          self._validate_group_name(group)
          group = _normalize_name(group)

          if group not in self._resolve_cache:
              with _ErrorCollector().on_exit(
                  f"[dependency-groups] data for {group!r} was malformed"
              ) as errors:
                  self._validate(group, group, [], set(), errors)

          return self._resolve(group)
>>>>>>> REPLACE