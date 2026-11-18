<<<<<<< SEARCH
        return new_version


   def _parse_letter_version(
=======
        return new_version

    def bump(self, part: str) -> Version:
        """Bump a specific version segment and reset subsequent segments."""
        if part == "major":
            idx = 0
        elif part == "minor":
            idx = 1
        elif part == "micro":
            idx = 2
        else:
            raise ValueError(
                f"part must be 'major', 'minor', or 'micro', got {part!r}"
            )

        new_release = list(self._release)
        while len(new_release) <= idx:
            new_release.append(0)
        new_release[idx] += 1
        for i in range(idx + 1, len(new_release)):
            new_release[i] = 0

        return self.__replace__(
            epoch=self._epoch,
            release=tuple(new_release),
            pre=None,
            post=None,
            dev=None,
            local=None,
        )


   def _parse_letter_version(
>>>>>>> REPLACE