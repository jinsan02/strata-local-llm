### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    for group_name, value in dependency_groups.items():
        normed_group_name = _normalize_name(group_name)
=======
    for group_name, value in dependency_groups.items():
        if not _NAME_RE.fullmatch(group_name):
            errors.error(InvalidGroupName(f"group name is invalid: {group_name!r}"))
        
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
        if not _NAME_RE.fullmatch(group):
            raise InvalidGroupName(f"group name is invalid: {group!r}")
        
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
        if not _NAME_RE.fullmatch(group):
            raise InvalidGroupName(f"group name is invalid: {group!r}")
        
        group = _normalize_name(group)
>>>>>>> REPLACE