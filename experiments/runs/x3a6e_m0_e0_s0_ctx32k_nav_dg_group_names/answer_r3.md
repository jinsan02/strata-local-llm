### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
def _normalize_group_names(
    dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    errors: _ErrorCollector,
) -> dict[str, Sequence[str | Mapping[str, str]]]:
    original_names: dict[str, list[str]] = {}
    normalized_groups: dict[str, Sequence[str | Mapping[str, str]]] = {}

    for group_name, value in dependency_groups.items():
        normed_group_name = _normalize_name(group_name)
=======
def _normalize_group_names(
    dependency_groups: Mapping[str, Sequence[str | Mapping[str, str]]],
    errors: _ErrorCollector,
) -> dict[str, Sequence[str | Mapping[str, str]]]:
    original_names: dict[str, list[str]] = {}
    normalized_groups: dict[str, Sequence[str | Mapping[str, str]]] = {}

    for group_name, value in dependency_groups.items():
        if not _validate_regex.fullmatch(group_name):
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
        if not _validate_regex.fullmatch(group):
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
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"group name is invalid: {group!r}")
        group = _normalize_name(group)
>>>>>>> REPLACE

---

**변경 내용 요약:**
1. `packaging.utils._validate_regex`를 import 하여 core metadata `Name` 규칙을 재사용함.
2. 공개 예외 `InvalidGroupName(ValueError)` 클래스를 정의하고 `__all__`에 등록함.
3. `_normalize_group_names()`: 그룹 이름 키 매핑 전 유효성 검사 후, 위반 시 `_ErrorCollector`에 수집하여 기존 중복 오류와 동일하게 한꺼번에 보고하도록 수정함.
4. `lookup()` 및 `resolve()`: 입력받은 group 문자열이 규칙을 위반하면 정규화/조회 전에 즉시 `InvalidGroupName` 단일 예외를 던지도록 수정함.
5. 기존 동작(정규화, 중복 검사, include 처리, 순환 검사)은 영향을 받지 않음.