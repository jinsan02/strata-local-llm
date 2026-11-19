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
    "InvalidGroupName",
    "InvalidDependencyGroupObject",
    "resolve_dependency_groups",
]
>>>>>>> REPLACE
<<<<<<< SEARCH
class DuplicateGroupNames(ValueError):
    """
    The same dependency groups were defined twice, with different non-normalized names.

    .. versionadded:: 26.1
    """


class CyclicDependencyGroup(ValueError):
=======
class InvalidGroupName(ValueError):
    """
    An invalid dependency group name was found.

    .. versionadded:: 26.1
    """


class DuplicateGroupNames(ValueError):
    """
    The same dependency groups were defined twice, with different non-normalized names.

    .. versionadded:: 26.1
    """


class CyclicDependencyGroup(ValueError):
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
=======
    def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
        """
        Lookup a group name, returning the parsed dependency data for that group.
        This will not resolve includes.

        :param group: the name of the group to lookup
        """
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"name is invalid: {group!r}")
        group = _normalize_name(group)

        with _ErrorCollector().on_exit(
>>>>>>> REPLACE
<<<<<<< SEARCH
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        group = _normalize_name(group)

        if group not in self._resolve_cache:
=======
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"name is invalid: {group!r}")
        group = _normalize_name(group)

        if group not in self._resolve_cache:
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