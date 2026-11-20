### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement
from .utils import canonicalize_name
=======
from .errors import _ErrorCollector
from .requirements import InvalidRequirement, Requirement
from .utils import InvalidName, canonicalize_name
>>>>>>> REPLACE

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
    A group name is not a valid PEP 735 dependency group name (must follow the
    core metadata ``Name`` field rules).

    .. versionadded:: 26.1
    """


class CyclicDependencyGroup(ValueError):
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    for group_name, value in dependency_groups.items():
        normed_group_name = _normalize_name(group_name)
        original_names.setdefault(normed_group_name, []).append(group_name)
        normalized_groups[normed_group_name] = value
=======
    for group_name, value in dependency_groups.items():
        try:
            canonicalize_name(group_name, validate=True)
        except InvalidName:
            errors.error(InvalidGroupName(f"{group_name!r} is not a valid dependency group name"))

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
        try:
            canonicalize_name(group, validate=True)
        except InvalidName as e:
            raise InvalidGroupName(f"{group!r} is not a valid dependency group name") from e

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
        try:
            canonicalize_name(group, validate=True)
        except InvalidName as e:
            raise InvalidGroupName(f"{group!r} is not a valid dependency group name") from e

        group = _normalize_name(group)
>>>>>>> REPLACE

---

`packaging.utils.canonicalize_name(..., validate=True)` 함수를 재사용하여 그룹 이름 유효성 검사 로직을 추가했습니다. 
- `__all__`에 `InvalidGroupName(ValueError)` 하위 클래스를 등록하고 예외 정의를 도입했습니다.
- `_normalize_group_names`에서 각 키에 대해 검증 후 실패 시 기존 `_ErrorCollector` 패턴대로 에러 리스트에 누적합니다.
- `lookup()`과 `resolve()`에서는 다른 처리(정규화/캐시 조회) 전에 유효성 검사를 수행하여 단일 `InvalidGroupName` 예외를 즉시 발생시킵니다. 메시지에는 이름의 `repr` 형태가 포함됩니다. 기존 정규화 및 중복 검사 동작은 영향을 받지 않습니다.