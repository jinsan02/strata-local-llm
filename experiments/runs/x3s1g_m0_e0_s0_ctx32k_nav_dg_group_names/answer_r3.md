`packaging.utils.canonicalize_name`를 사용하여 이름 유효성을 검사하고, `InvalidGroupName` 예외 클래스를 추가했습니다. `DependencyGroupResolver.__init__`, `lookup`, `resolve` 메서드를 수정하여 검증 로직을 적용했습니다.

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
from .utils import canonicalize_name, InvalidName

__all__ = [
    "CyclicDependencyGroup",
    "DependencyGroupInclude",
    "DependencyGroupResolver",
    "DuplicateGroupNames",
    "InvalidDependencyGroupObject",
    "InvalidGroupName",
    "resolve_dependency_groups",
]


class InvalidGroupName(ValueError):
    """
    Raised when a dependency group name is invalid.

    Group names must follow the same rules as the ``Name`` field in core metadata
    (i.e. they must match the PEP 503 normalized name pattern).

    .. versionadded:: 26.1
    """
>>>>>>> REPLACE
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

        for name in dependency_groups.keys():
            try:
                canonicalize_name(name, validate=True)
            except InvalidName as exc:
                errors.error(InvalidGroupName(f"Invalid group name {name!r}"))

        self.dependency_groups = _normalize_group_names(dependency_groups, errors)
>>>>>>> REPLACE
<<<<<<< SEARCH
    def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
        """
        Lookup a group name, returning the parsed dependency data for that group.
        This will not resolve includes.

        :param group: the name of the group to lookup
        """
        with _ErrorCollector().on_exit(
=======
    def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
        """
        Lookup a group name, returning the parsed dependency data for that group.
        This will not resolve includes.

        :param group: the name of the group to lookup
        """
        try:
            canonicalize_name(group, validate=True)
        except InvalidName as exc:
            raise InvalidGroupName(f"Invalid group name {group!r}") from exc

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
            with _ErrorCollector().on_exit(
=======
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        try:
            canonicalize_name(group, validate=True)
        except InvalidName as exc:
            raise InvalidGroupName(f"Invalid group name {group!r}") from exc

        group = _normalize_name(group)

        if group not in self._resolve_cache:
            with _ErrorCollector().on_exit(
>>>>>>> REPLACE