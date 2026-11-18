src/packaging/dependency_groups.py 파일에 다음 수정을 가했다:
1. `utils._validate_regex`를 import하고 `InvalidGroupName` 예외 클래스와 `__all__` 항목을 추가했다.
2. `_normalize_group_names` 함수에서 모든 그룹 키가 규칙을 따르는지 검사하여 오류가 있으면 `_ErrorCollector`에 `InvalidGroupName` 예외를 누적한다.
3. `lookup()`과 `resolve()` 메서드 시작 부분에서 인자로 받은 이름이 규칙을 따르지 않으면 즉시 `InvalidGroupName`을 던진다.

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
    A dependency group name does not conform to the core metadata ``Name`` field rules.

    .. versionadded:: NEXT.VERSION
    """


class CyclicDependencyGroup(ValueError):
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
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
    for group_name, value in dependency_groups.items():
        if not _validate_regex.fullmatch(group_name):
            errors.error(
                InvalidGroupName(f"dependency group name is invalid: {group_name!r}")
            )

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
        :param group: the name of the group to lookup
        """
        group = _normalize_name(group)

        with _ErrorCollector().on_exit(
=======
        :param group: the name of the group to lookup
        """
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"dependency group name is invalid: {group!r}")

        group = _normalize_name(group)

        with _ErrorCollector().on_exit(
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
        :param group: the name of the group to resolve
        """
        group = _normalize_name(group)

        if group not in self._resolve_cache:
=======
        :param group: the name of the group to resolve
        """
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"dependency group name is invalid: {group!r}")

        group = _normalize_name(group)

        if group not in self._resolve_cache:
>>>>>>> REPLACE