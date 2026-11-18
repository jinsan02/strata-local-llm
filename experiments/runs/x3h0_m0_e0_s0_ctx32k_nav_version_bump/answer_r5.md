src/packaging/version.py 파일의 `Version` 클래스 내 `__replace__` 메서드 뒤에 `bump` 메서드를 추가합니다. 이 메서드는 지정된 부분(`major`, `minor`, `micro`)의 릴리스 번호를 1 증가시키고, 뒤의 번호들을 0으로 초기화하며, 다른 세그먼트는 삭제하는 새 버전을 반환합니다.

### EDIT: src/packaging/version.py
<<<<<<< SEARCH
        return new_version

    @property
    def _key(self) -> CmpKey:
=======
        return new_version

    def bump(self, part: str) -> Version:
        """Return a new version with the specified release component incremented by 1.

        >>> Version("1.2.3").bump("major")
        <Version('2.0.0')>
        >>> Version("1.2.3").bump("minor")
        <Version('1.3.0')>
        >>> Version("1").bump("micro")
        <Version('1.0.1')>
        >>> Version("2!1.2.3rc1.post2.dev3+abc").bump("micro")
        <Version('2!1.2.4')>

        :param part: One of ``"major"``, ``"minor"``, or ``"micro"``.
        :raises ValueError: If *part* is not one of the recognised keywords.
        """
        if part == "major":
            index = 0
        elif part == "minor":
            index = 1
        elif part == "micro":
            index = 2
        else:
            raise ValueError(f"Invalid bump part {part!r}")

        release = list(self._release)

        # Ensure the release tuple is long enough to contain the target index
        if len(release) <= index:
            release.extend([0] * (index + 1 - len(release)))

        release[index] += 1

        # Reset all subsequent components to zero
        for i in range(index + 1, len(release)):
            release[i] = 0

        return self.__replace__(
            release=tuple(release),
            pre=None, post=None, dev=None, local=None
        )

    @property
    def _key(self) -> CmpKey:
>>>>>>> REPLACE