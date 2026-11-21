### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    for group_name, value in dependency_groups.items():
        normed_group_name = _normalize_name(group_name)
        original_names.setdefault(normed_group_name, []).append(group_name)
        normalized_groups[normed_group_name] = value
=======
    for group_name, value in dependency_groups.items():
        try:
            _validate_group_name(group_name)
        except InvalidGroupName as e:
            errors.error(e)
        normed_group_name = _normalize_name(group_name)
        original_names.setdefault(normed_group_name, []).append(group_name)
        normalized_groups[normed_group_name] = value
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
        _validate_group_name(group)
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
        _validate_group_name(group)
        group = _normalize_name(group)

        if group not in self._resolve_cache:
>>>>>>> REPLACE