`Version` 클래스의 `_trim_release` 메서드 뒤에 `bump` 메서드를 추가했습니다. 이 메서드는 지정한 릴리즈 부분(`major`, `minor`, `micro`)을 1 증가시키고, 이후 부분을 0으로 초기화하며, 전역 번호(epoch)는 유지하고 기타 세그먼트(pre, post, dev, local)는 제거합니다. 유효하지 않은 `part` 값이 입력되면 `ValueError`를 발생시킵니다.

### EDIT: src/packaging/version.py
<<<<<<< SEARCH
        new_version._hash_cache = self._hash_cache
        return new_version


def _parse_letter_version(
=======
        new_version._hash_cache = self._hash_cache
        return new_version

    def bump(self, part: str) -> Version:
        """Return a new version with the release segment incremented.

        Returns a new :class:`Version` with the specified part incremented by 1,
        and all subsequent parts set to 0. Pre-release, post-release, dev, and 
        local segments are discarded.

        :param part: One of ``"major"``, ``"minor"``, or ``"micro"``.
        :raises ValueError: If *part* is not valid.

        .. versionadded:: 26.5
        """
        bump_index = {"major": 0, "minor": 1, "micro": 2}.get(part)
        if bump_index is None:
            raise ValueError(
                f"Invalid bump part {part!r}; must be one of 'major', 'minor', 'micro'"
            )

        release = list(self._release)
        
        # Extend length if needed to accommodate the index
        if len(release) <= bump_index:
            release.extend([0] * (bump_index - len(release) + 1))
            
        release[bump_index] += 1
        
        # Clear all subsequent parts
        for k in range(bump_index + 1, len(release)):
            release[k] = 0
            
        return self.__class__.from_parts(
            epoch=self._epoch,
            release=tuple(release),
        )


def _parse_letter_version(
>>>>>>> REPLACE