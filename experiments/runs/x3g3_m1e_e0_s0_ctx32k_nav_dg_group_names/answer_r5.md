### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
    def lookup(self, group: str) -> tuple[Requirement | DependencyGroupInclude, ...]:
        """
        Lookup a group name, returning the parsed dependency data for that group.
        This will not resolve includes.

        :param group: the name of the group to lookup
        """
        group = _normalize_name(group)

        with _ErrorCollector().on_exit(
            f"[dependency-groups] data for {group!r} was malformed"
        ) as errors:
            return self._parse_group(group, errors)
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
            raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
        group = _normalize_name(group)

        with _ErrorCollector().on_exit(
            f"[dependency-groups] data for {group!r} was malformed"
        ) as errors:
            return self._parse_group(group, errors)
>>>>>>> REPLACE

### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
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
=======
    def resolve(self, group: str) -> tuple[Requirement, ...]:
        """
        Resolve a dependency group to a list of requirements.

        :param group: the name of the group to resolve
        """
        try:
            canonicalize_name(group, validate=True)
        except InvalidName:
            raise InvalidGroupName(f"Invalid dependency group name: {group!r}")
        group = _normalize_name(group)

        if group not in self._resolve_cache:
            with _ErrorCollector().on_exit(
                f"[dependency-groups] data for {group!r} was malformed"
            ) as errors:
                self._validate(group, group, [], set(), errors)

        return self._resolve(group)
>>>>>>> REPLACE

### 요약
- `InvalidGroupName` 예외 클래스를 `ValueError` 하위로 정의하고 `__all__` 에 등록함.
- `_normalize_group_names` 에서 `canonicalize_name(..., validate=True)` 를 사용하여 그룹 키를 검증하고, 실패 시 `_ErrorCollector` 에 `InvalidGroupName` 을 추가하여 기존 오류와 함께 한꺼번에 보고하도록 수정함.
- `lookup()` 과 `resolve()` 메서드 시작 부분에서 그룹 이름 유효성을 즉시 검사하고, 규칙을 위반하면 `InvalidGroupName` 을 단일 예외로 던지도록 수정함.
- `utils` 에서 `InvalidName` 과 `canonicalize_name` 을 임포트하여 재사용함.