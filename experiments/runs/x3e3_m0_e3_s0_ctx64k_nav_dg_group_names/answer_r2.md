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
        except InvalidName as e:
            errors.error(InvalidGroupName(str(e)))
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
            raise InvalidGroupName(str(e)) from e
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
        try:
            canonicalize_name(group, validate=True)
        except InvalidName as e:
            raise InvalidGroupName(str(e)) from e
        group = _normalize_name(group)
>>>>>>> REPLACE

### 요약
1. `InvalidGroupName` 예외 클래스를 추가하고 `__all__`에 등록했습니다.
2. `packaging.utils`에서 `canonicalize_name`과 `InvalidName`을 가져와 그룹 이름 검증에 사용했습니다.
3. `_normalize_group_names`에서 그룹 이름을 검증하여 `InvalidGroupName` 오류를 수집합니다.
4. `DependencyGroupResolver`의 `lookup`과 `resolve` 메서드에서 그룹 이름을 즉시 검증하고, 유효하지 않으면 `InvalidGroupName`을 즉시 던집니다.