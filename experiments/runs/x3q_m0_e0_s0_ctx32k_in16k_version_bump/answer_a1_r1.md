### EDIT: src/packaging/version.py
<<<<<<< SEARCH
        return self.release[2] if len(self.release) >= 3 else 0

    def _trim_release(self) -> Version:
=======
    def bump(self, part: str) -> Self:
        if part not in ("major", "minor", "micro"):
            raise ValueError(f"part must be one of 'major', 'minor', 'micro', got {part!r}")

        idx = {"major": 0, "minor": 1, "micro": 2}[part]
        release = list(self._release)

        while len(release) <= idx:
            release.append(0)

        release[idx] += 1
        for i in range(idx + 1, len(release)):
            release[i] = 0

        return self.__replace__(release=tuple(release), pre=None, post=None, dev=None, local=None)

    def _trim_release(self) -> Version:
>>>>>>> REPLACE