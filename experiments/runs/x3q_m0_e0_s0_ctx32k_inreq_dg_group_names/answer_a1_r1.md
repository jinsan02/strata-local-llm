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
    # -----------
    # Error Types
    # -----------


    class DuplicateGroupNames(ValueError):
=======
    # -----------
    # Error Types
    # -----------


    class InvalidGroupName(ValueError):
        """
        A dependency group name did not conform to the naming rules defined
        in the core metadata specification.

        .. versionadded:: 26.1
        """


    class DuplicateGroupNames(ValueError):
>>>>>>> REPLACE
```

```python
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

        for group_name in dependency_groups:
            try:
                canonicalize_name(group_name, validate=True)
            except InvalidName:
                errors.error(InvalidGroupName(f"Invalid dependency group name: {group_name!r}"))

        self.dependency_groups = _normalize_group_names(dependency_groups, errors)
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
        except InvalidName:
            raise InvalidGroupName(f"Invalid dependency group name: {group!r}") from None

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
        except InvalidName:
            raise InvalidGroupName(f"Invalid dependency group name: {group!r}") from None

        group = _normalize_name(group)
>>>>>>> REPLACE
```