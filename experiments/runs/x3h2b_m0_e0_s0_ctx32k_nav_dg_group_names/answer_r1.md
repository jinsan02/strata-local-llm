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
        except InvalidName:
            raise InvalidGroupName(f"invalid group name: {group!r}") from None

        group = _normalize_name(group)
>>>>>>> REPLACE