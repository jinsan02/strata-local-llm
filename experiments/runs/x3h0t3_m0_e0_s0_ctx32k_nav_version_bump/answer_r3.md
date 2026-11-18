EDIT: src/packaging/version.py
<<<<<<< SEARCH
        return new_version

    @property
    def _key(self) -> CmpKey:
=======
        return new_version

    def bump(self, part: str) -> Version:
        """Return a new version with the specified release component incremented.

        ``part`` must be ``"major"``, ``"minor"``, or ``"micro"``. The corresponding
        element in :attr:`release` is increased by one, and all subsequent elements
        are reset to zero.  Epoch is preserved; pre-release, post-release, dev, and
        local segments are discarded.  If the target position does not yet exist in
        the release segment it is created (zero-filled).

        >>> Version("1.2.3").bump("minor")
        <Version('1.3.0')>
        >>> Version("1").bump("micro")
        <Version('1.0.1')>
        >>> Version("2!1.2.3rc1.post2.dev3+abc").bump("micro")
        <Version('2!1.2.4')>
        >>> Version("1.2.3.4").bump("minor")
        <Version('1.3.0.0')>

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
        
        # Extend release if necessary to reach the target index
        if len(release) <= index:
            release.extend([0] * (index + 1 - len(release)))
            
        release[index] += 1
        
        # Reset subsequent components
        for i in range(index + 1, len(release)):
            release[i] = 0

        return self.__replace__(
            release=tuple(release),
            pre=None, post=None, dev=None, local=None
        )

    @property
    def _key(self) -> CmpKey:
>>>>>>> REPLACE