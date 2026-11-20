### EDIT: src/packaging/version.py
<<<<<<< SEARCH
        return new_version


def _parse_letter_version(
=======
        return new_version

    def bump(self, part: str) -> Version:
        """
        Return a new version with the specified part incremented by 1,
        and all subsequent parts set to 0.

        >>> Version("1.2.3").bump("major")
        <Version('2.0.0')>
        >>> Version("1.2.3").bump("minor")
        <Version('1.3.0')>
        >>> Version("1.2.3").bump("micro")
        <Version('1.2.4')>
        >>> Version("1").bump("micro")
        <Version('1.0.1')>
        >>> Version("1.2.3.4").bump("minor")
        <Version('1.3.0.0')>
        >>> Version("1.2.3a1").bump("micro")
        <Version('1.2.4')>
        >>> Version("1.2.3").bump("invalid")
        Traceback (most recent call last):
            ...
        ValueError: Invalid part: 'invalid'
        """
        if part == "major":
            index = 0
        elif part == "minor":
            index = 1
        elif part == "micro":
            index = 2
        else:
            raise ValueError(f"Invalid part: {part!r}")

        release = list(self._release)
        while len(release) <= index:
            release.append(0)

        release[index] += 1
        for i in range(index + 1, len(release)):
            release[i] = 0

        return self.__replace__(
            release=tuple(release), pre=None, post=None, dev=None, local=None
        )


def _parse_letter_version(
>>>>>>> REPLACE