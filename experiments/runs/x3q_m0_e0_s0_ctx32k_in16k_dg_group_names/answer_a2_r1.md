<<<<<<< SEARCH
        for group_name, value in dependency_groups.items():
            normed_group_name = _normalize_name(group_name)
=======
        for group_name, value in dependency_groups.items():
            if not _validate_regex.fullmatch(group_name):
                errors.error(InvalidGroupName(f"Invalid dependency group name: {group_name!r}"))
            normed_group_name = _normalize_name(group_name)
>>>>>>> REPLACE
<<<<<<< SEARCH
        """
        group = _normalize_name(group)

        with _ErrorCollector().on_exit(
=======
        """
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
        group = _normalize_name(group)

        with _ErrorCollector().on_exit(
>>>>>>> REPLACE
<<<<<<< SEARCH
        """
        group = _normalize_name(group)

        if group not in self._resolve_cache:
=======
        """
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
        group = _normalize_name(group)

        if group not in self._resolve_cache:
>>>>>>> REPLACE