<<<<<<< SEARCH
        return new_version

    @property
    def _key(self) -> CmpKey:
        if self._key_cache is None:
            self._key_cache = _cmpkey(
                self._epoch,
                self._release,
                self._pre,
                self._post,
                self._dev,
                self._local,
            )
        return self._key_cache
=======
        return new_version

    def bump(self, part: str) -> Version:
        if part == "major":
            idx = 0
        elif part == "minor":
            idx = 1
        elif part == "micro":
            idx = 2
        else:
            raise ValueError(f"part must be 'major', 'minor', or 'micro', got {part!r}")

        new_release = list(self._release)
        while len(new_release) <= idx:
            new_release.append(0)

        new_release[idx] += 1
        for i in range(idx + 1, len(new_release)):
            new_release[i] = 0

        return self.__replace__(
            release=tuple(new_release),
            pre=None,
            post=None,
            dev=None,
            local=None,
        )

    @property
    def _key(self) -> CmpKey:
        if self._key_cache is None:
            self._key_cache = _cmpkey(
                self._epoch,
                self._release,
                self._pre,
                self._post,
                self._dev,
                self._local,
            )
        return self._key_cache
>>>>>>> REPLACE