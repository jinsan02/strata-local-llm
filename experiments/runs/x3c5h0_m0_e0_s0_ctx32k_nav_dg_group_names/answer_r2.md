### EDIT: src/packaging/dependency_groups.py
<<<<<<< SEARCH
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"invalid group name: {group!r}")
        group = _normalize_name(group)
        """
        group = _normalize_name(group)

        if group not in self._resolve_cache:
=======
        if not _validate_regex.fullmatch(group):
            raise InvalidGroupName(f"invalid group name: {group!r}")
        group = _normalize_name(group)

        if group not in self._resolve_cache:
>>>>>>> REPLACE

이전 편집 과정에서 `resolve()` 메서드에 남아있는 중복 줄과 이상한 docstring 문자열(`"""`)를 제거하여 문법 오류를 수정했습니다. 나머지 요구사항(`InvalidGroupName` 추가, `__all__` 반영, `_normalize_group_names` 및 `lookup/resolve` 검사의 정규화)은 이미 적용되어 있습니다.