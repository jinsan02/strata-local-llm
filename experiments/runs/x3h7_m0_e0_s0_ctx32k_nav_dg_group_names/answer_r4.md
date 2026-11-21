<tool_call>
<function=edit_file>
<parameter=new_string>
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"{group!r} is not a valid name")
        group = _normalize_name(group)

        if group not in self._resolve_cache:
            with _ErrorCollector().on_exit(
                f"[dependency-groups] data for {group!r} was malformed"
            ) as errors:
                self._validate(group, group, [], set(), errors)

        return self._resolve(group)
</parameter>
<parameter=old_string>
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        group = _normalize_name(group)

        if group not in self._resolve_cache:
            with _ErrorCollector().on_exit(
                f"[dependency-groups] data for {group!r} was malformed"
            ) as errors:
                self._validate(group, group, [], set(), errors)

        return self._resolve(group)
</parameter>
<parameter=path>
src/packaging/dependency_groups.py
</parameter>
</function>
</tool_call>