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
    """
    A dependency group name does not conform to the ``Name`` field rules in
    core metadata.

    .. versionadded:: 26.4
    """


# ------------------------
# Object Model & Interface
# ------------------------
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
def _normalize_name(name: str) -> str:
    return _NORMALIZE_PATTERN.sub("-", name).lower()


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
def _normalize_name(name: str) -> str:
    return _NORMALIZE_PATTERN.sub("-", name).lower()


def _validate_group_name(name: str) -> None:
    """Validate that a group name conforms to the core metadata ``Name`` rules."""
    if not _validate_regex.fullmatch(name):
        raise InvalidGroupName(f"invalid dependency group name: {name!r}")


def _normalize_group_names(
    dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    errors: _ErrorCollector,
) -> dict[str, Sequence[str | Mapping[str, str]]]:
    original_names: dict[str, list[str]] = {}
    normalized_groups: dict[str, Sequence[str | Mapping[str, str]]] = {}

    for group_name, value in dependency_groups.items():
        try:
            _validate_group_name(group_name)
        except InvalidGroupName as e:
            errors.error(e)
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

        with _ErrorCollector().on_exit(
            f"[dependency-groups] data for {group!r} was malformed"
        ) as errors:
            return self._parse_group(group, errors)

    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        group = _normalize_name(group)
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

    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        _validate_group_name(group)
        group = _normalize_name(group)
>>>>>>> REPLACE