<tool_call>
<function=edit_file>
<parameter=new_string>
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        _validate_group_name(group)
        group = _normalize_name(group)

        if group not in self._resolve_cache:
            with _ErrorCollector().on_exit(
                f"[dependency-groups] data for {group!r} was malformed"
            ) as errors:
                self._validate(group, group, [], set(), errors)

        return self._resolve_cache[group]
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

        return self._resolve_cache[group]
</parameter>
<parameter=path>
src/packaging/dependency_groups.py
</parameter>
</function>
</tool_call>