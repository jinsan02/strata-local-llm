`src/packaging/dependency_groups.py` 파일에서 다음 사항을 수정했습니다:

1. `InvalidGroupName` 예외 클래스 추가 (`ValueError` 하위)
2. `__all__`에 `InvalidGroupName` 등록
3. `_normalize_group_names()`에서 각 그룹 이름의 유효성을 검사하고, 규칙을 위반하면 기존 오류(중복 등)와 같은 방식으로 `_ErrorCollector`에 추가
4. `lookup()`, `resolve()` 메서드에서 group 파라미터 검증 후 즉시 `InvalidGroupName` 예외 던지기 (이전 동작 유지)

```python
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
from .utils import InvalidName, canonicalize_name

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
```

```python
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
    A dependency group name is not a valid core metadata Name.

    .. versionadded:: 26.1
    """


class CyclicDependencyGroup(ValueError):
>>>>>>> REPLACE
```

```python
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
        try:
            canonicalize_name(group, validate=True)
        except InvalidName as exc:
            raise InvalidGroupName(str(exc)) from exc

        group = _normalize_name(group)
>>>>>>> REPLACE
```

```python
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
        try:
            canonicalize_name(group, validate=True)
        except InvalidName as exc:
            raise InvalidGroupName(str(exc)) from exc

        group = _normalize_name(group)
>>>>>>> REPLACE
```

```python
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
        try:
            canonicalize_name(group_name, validate=True)
        except InvalidName as exc:
            errors.error(InvalidGroupName(str(exc)))
            continue
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
```